from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

import config

engine = create_engine(
    url=config.DB_URL,
    echo=config.BD_ECHO
)

Base = declarative_base()
