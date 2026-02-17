from sqlalchemy import create_engine
import os

# ============================
# 🔐 DATABASE CONFIG
# ============================
DB_USER = "root"
DB_PASSWORD = "root"        # change if needed
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "smart_pricing"

from sqlalchemy import create_engine

DATABASE_URL = (
    "mysql+pymysql://ai_user:ai_password@localhost:3306/smart_pricing"
)

from sqlalchemy import create_engine

DATABASE_URL = (
    "mysql+pymysql://ai_user:ai_password@localhost:3306/smart_pricing"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


engine = create_engine(DATABASE_URL)
