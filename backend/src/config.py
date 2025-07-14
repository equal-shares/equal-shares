# Configuration for the server, initialized from environment variables

import os
from uuid import UUID, uuid4

from src.exceptions import CriticalException


class Config:
    """Configuration for the server, initialized from environment variables"""

    pg_database: str = ""
    pg_user: str = ""
    pg_password: str = ""
    pg_host: str = ""
    pg_port: int = 5432

    admin_key: UUID = uuid4()

    api_rsa_public_key: str = ""
    api_rsa_private_key: str = ""

    without_auth_mode: bool = False

    logger_level: str = "DEBUG"  # Level for logging


config = Config()


def _get_envioment_variable(variable_name: str) -> str:
    """Get an environment variable or raise an exception if it is not set"""

    variable = os.environ.get(variable_name)
    if variable is None:
        raise CriticalException(f"Environment variable {variable_name} not set")
    return variable


def init_config() -> None:
    """Initialize configuration from environment variables"""
    from dotenv import load_dotenv

    if os.path.exists(".env"):
        load_dotenv(override=False)

    config.pg_database = _get_envioment_variable("PG_DATABASE")
    config.pg_user = _get_envioment_variable("PG_USER")
    config.pg_password = _get_envioment_variable("PG_PASSWORD")
    config.pg_host = _get_envioment_variable("PG_HOST")

    pg_port = os.environ.get("PG_PORT")
    if pg_port is not None:
        config.pg_port = int(pg_port)

    config.admin_key = UUID(_get_envioment_variable("ADMIN_KEY"))
    config.api_rsa_public_key = _get_envioment_variable("API_RSA_PUBLIC_KEY")
    config.api_rsa_private_key = _get_envioment_variable("API_RSA_PRIVATE_KEY")

    without_auth_mode = os.environ.get("WITHOUT_AUTH_MODE")
    if without_auth_mode is not None:
        config.without_auth_mode = without_auth_mode.lower() == "true"

    print("config.without_auth_mode", config.without_auth_mode)
