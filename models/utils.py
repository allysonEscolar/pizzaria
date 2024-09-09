from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import LoginManager

db = SQLAlchemy()
lm = LoginManager()