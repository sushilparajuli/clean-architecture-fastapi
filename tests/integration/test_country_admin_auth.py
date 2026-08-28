from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.features.auth.infrastructure.models.audit_log_model import AuditLogModel


def get_token(client: TestClient, email: str, role: str) -> str:
    client.post(
        "/v1/auth/register",
        json={"email": email, "password": "Password123!", "role": role},
    )
    res = client.post(
        "/v1/auth/login",
        json={"email": email, "password": "Password123!"},
    )
    return res.json()["access_token"]


def test_public_country_get_endpoints(client: TestClient, db_session: Session):
    # Public list
    res = client.get("/v1/admin/countries")
    assert res.status_code == 200

    # Create one via admin first
    admin_token = get_token(client, "admin1@test.com", "admin")
    create_res = client.post(
        "/v1/admin/countries",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "France", "country_code": "FR", "currency_code": "EUR"},
    )
    assert create_res.status_code == 201
    c_id = create_res.json()["data"]["id"]

    # Public get by id
    res_id = client.get(f"/v1/admin/countries/{c_id}")
    assert res_id.status_code == 200
    assert res_id.json()["data"]["name"] == "France"


def test_country_mutation_unauthenticated(client: TestClient):
    # POST without auth
    res = client.post(
        "/v1/admin/countries",
        json={"name": "Spain", "country_code": "ES", "currency_code": "EUR"},
    )
    assert res.status_code == 401
    assert res.json()["code"] == "UNAUTHORIZED"


def test_country_mutation_regular_user_forbidden(client: TestClient):
    user_token = get_token(client, "user1@test.com", "user")

    # POST with user token
    res = client.post(
        "/v1/admin/countries",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Germany", "country_code": "DE", "currency_code": "EUR"},
    )
    assert res.status_code == 403
    assert res.json()["code"] == "FORBIDDEN"


def test_country_mutation_admin_e2e_with_audit_logs(
    client: TestClient, db_session: Session
):
    admin_token = get_token(client, "superadmin@test.com", "admin")
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Create Country (POST)
    create_res = client.post(
        "/v1/admin/countries",
        headers=headers,
        json={"name": "Japan", "country_code": "JP", "currency_code": "JPY"},
    )
    assert create_res.status_code == 201
    country_data = create_res.json()["data"]
    country_id = country_data["id"]
    assert country_data["name"] == "Japan"

    # Verify Audit Log in DB
    create_log = (
        db_session.query(AuditLogModel)
        .filter(AuditLogModel.action == "COUNTRY_CREATE")
        .first()
    )
    assert create_log is not None
    assert create_log.resource_type == "country"
    assert create_log.resource_id == str(country_id)
    assert create_log.user_id is not None
    assert create_log.log_metadata["name"] == "Japan"

    # 2. Update Country (PUT)
    update_res = client.put(
        f"/v1/admin/countries/{country_id}",
        headers=headers,
        json={"currency_code": "USD"},
    )
    assert update_res.status_code == 200

    # Verify Update Audit Log in DB
    update_log = (
        db_session.query(AuditLogModel)
        .filter(AuditLogModel.action == "COUNTRY_UPDATE")
        .first()
    )
    assert update_log is not None
    assert update_log.resource_id == str(country_id)

    # 3. Delete Country (DELETE)
    delete_res = client.delete(
        f"/v1/admin/countries/{country_id}",
        headers=headers,
    )
    assert delete_res.status_code == 204

    # Verify Delete Audit Log in DB
    delete_log = (
        db_session.query(AuditLogModel)
        .filter(AuditLogModel.action == "COUNTRY_DELETE")
        .first()
    )
    assert delete_log is not None
    assert delete_log.resource_id == str(country_id)
