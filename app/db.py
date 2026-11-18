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

    # Safe column additions on existing parcels and plants tables
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            if settings.DATABASE_URL.startswith("postgresql"):
                conn.execute(text("ALTER TABLE parcels ADD COLUMN IF NOT EXISTS region_natural VARCHAR(100);"))
                conn.execute(text("ALTER TABLE parcels ADD COLUMN IF NOT EXISTS canton VARCHAR(100);"))
                conn.execute(text("ALTER TABLE parcels ADD COLUMN IF NOT EXISTS elevation_m FLOAT DEFAULT 250.0;"))
                conn.execute(text("ALTER TABLE parcels ADD COLUMN IF NOT EXISTS slope_pct FLOAT DEFAULT 2.0;"))
                conn.execute(text("ALTER TABLE plants ADD COLUMN IF NOT EXISTS yield_t_ha FLOAT DEFAULT 4.0;"))
                conn.execute(text("ALTER TABLE plants ADD COLUMN IF NOT EXISTS price_eur_t FLOAT DEFAULT 250.0;"))
                conn.execute(text("ALTER TABLE plants ADD COLUMN IF NOT EXISTS input_cost_eur_ha FLOAT DEFAULT 600.0;"))
                conn.commit()
            else:
                # SQLite PRAGMA check on parcels
                res_p = conn.execute(text("PRAGMA table_info(parcels);")).fetchall()
                col_names_p = [r[1] for r in res_p]
                if "region_natural" not in col_names_p:
                    conn.execute(text("ALTER TABLE parcels ADD COLUMN region_natural VARCHAR(100);"))
                if "canton" not in col_names_p:
                    conn.execute(text("ALTER TABLE parcels ADD COLUMN canton VARCHAR(100);"))
                if "elevation_m" not in col_names_p:
                    conn.execute(text("ALTER TABLE parcels ADD COLUMN elevation_m FLOAT DEFAULT 250.0;"))
                if "slope_pct" not in col_names_p:
                    conn.execute(text("ALTER TABLE parcels ADD COLUMN slope_pct FLOAT DEFAULT 2.0;"))

                # SQLite PRAGMA check on plants
                res_pl = conn.execute(text("PRAGMA table_info(plants);")).fetchall()
                col_names_pl = [r[1] for r in res_pl]
                if "yield_t_ha" not in col_names_pl:
                    conn.execute(text("ALTER TABLE plants ADD COLUMN yield_t_ha FLOAT DEFAULT 4.0;"))
                if "price_eur_t" not in col_names_pl:
                    conn.execute(text("ALTER TABLE plants ADD COLUMN price_eur_t FLOAT DEFAULT 250.0;"))
                if "input_cost_eur_ha" not in col_names_pl:
                    conn.execute(text("ALTER TABLE plants ADD COLUMN input_cost_eur_ha FLOAT DEFAULT 600.0;"))
                conn.commit()
    except Exception:
        pass
