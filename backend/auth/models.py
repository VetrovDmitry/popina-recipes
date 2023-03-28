from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from uuid import uuid4
import enum
import datetime

from backend.database import db, Base


class HumanGender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'

    @classmethod
    def values(cls) -> list:
        return [cls.MALE.value, cls.FEMALE.value]


class UserStatus(enum.Enum):
    UNCONFIRMED = 'unconfirmed'
    CONFIRMED = 'confirmed'
    FROZEN = 'frozen'
    DELETED = 'deleted'

    @classmethod
    def values(cls) -> list:
        return [cls.UNCONFIRMED.value, cls.CONFIRMED.value, cls.FROZEN.value, cls.DELETED.value]


class User(db.Model, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    sex = Column(Enum(HumanGender))
    birth_date = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hash = Column(String(255), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus('confirmed'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    admin = relationship('Admin', back_populates='user', uselist=False, lazy=True)
    tokens = relationship('Token', back_populates='user', uselist=True)

    def __init__(self, first_name: str, last_name: str, username: str, sex: str, birth_date: datetime.date,
                 email: str, password: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.sex = HumanGender(sex)
        self.birth_date = birth_date
        self.email = email
        self.hash = self.create_hash(password)
        self.upload()

    def __repr__(self):
        return f"user: {self.fullname}"

    @property
    def role(self) -> str:
        if not self.admin:
            return 'user'
        return self.admin.status.value

    @property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def public_info(self) -> dict:
        return {
            'id': self.id,
            'fullname': self.fullname,
            'username': self.username,
            'email': self.email,
            'time_created': self.time_created.isoformat()
        }

    @property
    def entity(self) -> dict:
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @staticmethod
    def create_hash(password: str) -> str:
        return generate_password_hash(password).decode('UTF-8')

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.hash, password)

    def set_status(self, new_status: str) -> None:
        self.status = UserStatus(new_status)
        self.update()
        return


class AdminStatus(enum.Enum):
    ADMIN = 'admin'
    MODER = 'moder'

    @classmethod
    def values(cls) -> list:
        return [cls.ADMIN.value, cls.MODER.value]


class Admin(db.Model, Base):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    status = Column(Enum(AdminStatus))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', back_populates='admin', uselist=False, lazy=True)
    devices = relationship('Device', back_populates='admin', uselist=True)

    def __init__(self, user_id: int, status: str):
        self.id = user_id
        self.status = AdminStatus(status.lower())
        self.upload()

    def __repr__(self):
        return f"admin: {self.id}"

    @property
    def devices_info(self) -> list:
        info = list()
        for device in self.devices:
            info.append(device.info)
        return info

    @property
    def info(self) -> dict:
        return {
            'id': self.id,
            'status': self.status.value,
            'fullname': self.user.fullname,
            'username': self.user.username,
            'devices': len(self.devices),
            'time_created': self.time_created.isoformat()
        }

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


class DeviceStatus(enum.Enum):
    ENABLE = 'enable'
    DISABLE = 'disable'

    @classmethod
    def values(cls) -> list:
        return [cls.ENABLE.value, cls.DISABLE.value]


class Device(db.Model, Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey('admins.id'))
    name = Column(String(80), nullable=False, unique=True)
    key = Column(String(80), nullable=False)
    status = Column(Enum(DeviceStatus), default=DeviceStatus('enable'), nullable=False)
    requests = Column(Integer, default=0, nullable=False)

    admin = relationship('Admin', back_populates='devices', uselist=False)
    tokens = relationship('Token', back_populates='device', uselist=True)

    def __init__(self, admin_id: int, name: str):
        self.admin_id = admin_id
        self.name = name
        self.key = uuid4().hex
        self.upload()

    def __repr__(self):
        return f"device: {self.id}"

    def refresh_key(self) -> None:
        self.key = uuid4().hex
        self.update()

    def add_request(self) -> None:
        self.requests += 1
        self.update()

    def set_status(self, status: str) -> None:
        self.status = DeviceStatus(status)
        self.update()

    @property
    def info(self) -> dict:
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'name': self.name,
            'status': self.status.value,
            'key': self.key
        }

    @classmethod
    def find_by_name(cls, name: str) -> db.Model:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all_by_name(cls, name: str) -> list:
        return cls.query.filter(cls.name.ilike(f"%{name}%")).all()

    @classmethod
    def find_by_id(cls, _id: int) -> db.Model:
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_key(cls, key: str) -> db.Model:
        return cls.query.filter_by(key=key).first()


class TokenStatus(enum.Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'

    @classmethod
    def values(cls) -> list:
        return [cls.ACTIVE.value, cls.EXPIRED.value]


class Token(db.Model, Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(Text, unique=True, nullable=False)
    refresh_token = Column(Text, unique=True, nullable=False)
    expires = db.Column(DateTime(timezone=True))
    status = db.Column(Enum(TokenStatus), default=TokenStatus('active'), nullable=False)

    user = relationship('User', back_populates='tokens', uselist=False)
    device = relationship('Device', back_populates='tokens', uselist=False)

    def __init__(self, device_id: int, user_id: int, access_token: str, refresh_token: str, expires: datetime.datetime):
        self.device_id = device_id
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires = expires
        self.upload()

    def __repr__(self):
        return f"token: {self.id}"

    def update_data(self, access_token: str, refresh_token: str, expires: datetime.datetime):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires = expires
        self.status = TokenStatus('active')
        self.update()

    def update_access(self, access_token: str, expires: datetime.datetime):
        self.access_token = access_token
        self.expires = expires
        self.update()

    @property
    def user_entity(self) -> dict:
        return self.user.entity

    @classmethod
    def find_by_access_token(cls, access_token: str) -> db.Model:
        return cls.query.filter_by(access_token=access_token).first()

    @classmethod
    def find_by_refresh_token(cls, refresh_token: str) -> db.Model:
        return cls.query.filter_by(refresh_token=refresh_token).first()

    @classmethod
    def find_by_user_and_device(cls, user_id: int, device_id: int) -> db.Model:
        return cls.query.filter_by(user_id=user_id, device_id=device_id).first()

    def set_expired(self) -> None:
        self.status = TokenStatus('expired')
        self.update()
