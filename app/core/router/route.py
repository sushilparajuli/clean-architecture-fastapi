from fastapi import APIRouter


def get_versioned_router(version: str):
    """
    Get router with version
    :param version
    :return: Router with version
    """
    return APIRouter(prefix=f'/{version}')