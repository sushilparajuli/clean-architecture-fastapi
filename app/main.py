from fastapi import FastAPI

from app.core.http_errors import register_http_error_handler
from app.features.admin.country import admin_country_v1_router

app = FastAPI()

app.include_router(admin_country_v1_router, tags=["v1 Admin Country"])
register_http_error_handler(app)
