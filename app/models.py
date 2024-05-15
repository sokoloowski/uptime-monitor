import datetime

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, relationship

from app.app import db


class Host(db.Model):
    __tablename__ = 'host'
    id = mapped_column(sa.Integer, primary_key=True)
    ipaddress = mapped_column(sa.String(39), nullable=False)
    name = mapped_column(sa.String(255), nullable=True)
    up = mapped_column(sa.Boolean, nullable=False, server_default=sa.false())
    history = relationship('HostHistory', back_populates='host', lazy=True, cascade='all, delete-orphan')


class HostHistory(db.Model):
    __tablename__ = 'host_history'
    id = mapped_column(sa.Integer, primary_key=True)
    host_id = mapped_column(sa.Integer, sa.ForeignKey('host.id'), nullable=False)
    up = mapped_column(sa.Boolean, nullable=False)
    created_at = mapped_column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    host = relationship('Host', back_populates='history', lazy=False)
