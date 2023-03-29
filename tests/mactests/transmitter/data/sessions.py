import sqlalchemy
from .db_session import SqlAlchemyBase


class Sessions(SqlAlchemyBase):
    __tablename__ = "sessions"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    state = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    prev_move = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    dice = sqlalchemy.Column(sqlalchemy.String, nullable=True)