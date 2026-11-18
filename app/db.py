import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Engine configuration with sqlite thread safety if needed
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes database tables and ensures schema migrations."""
    # When connecting to PostgreSQL, attempt to create PostGIS extension if superuser
    if settings.DATABASE_URL.startswith("postgresql"):
        try:
            with engine.connect() as conn:
                from sqlalchemy import text
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
                conn.commit()
        except Exception:
            pass
    Base.metadata.create_all(bind=engine)

    # Safe column additions on existing parcels table
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            if settings.DATABASE_URL.startswith("postgresql"):
                conn.execute(text("ALTER TABLE parcels ADD COLUMN IF NOT EXISTS region_natural VARCHAR(100);"))
                conn.execute(text("ALTER TABLE parcels ADD COLUMN IF NOT EXISTS canton VARCHAR(100);"))
                conn.commit()
            else:
                # SQLite PRAGMA check
                res = conn.execute(text("PRAGMA table_info(parcels);")).fetchall()
                col_names = [r[1] for r in res]
                if "region_natural" not in col_names:
                    conn.execute(text("ALTER TABLE parcels ADD COLUMN region_natural VARCHAR(100);"))
                if "canton" not in col_names:
                    conn.execute(text("ALTER TABLE parcels ADD COLUMN canton VARCHAR(100);"))
                conn.commit()
    except Exception:
        pass
