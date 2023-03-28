from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta, timezone
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from os import getenv
import json

from . import models
from backend.utils import UserError, ModerError, AdminError, DeviceError, TokenError


class UserController:
    __model = models.User
    __salt = getenv('SERIALIZER_SALT', '')
    __serializer = URLSafeTimedSerializer(getenv('SECRET_KEY', ''))

    #  Checks

    @classmethod
    def check_user_exists(cls, user_id: int) -> dict:
        if cls.__model.find_by_id(user_id):
            return {'status': True, 'output': 'user_id: %s exists' % user_id}
        return {'status': False, 'output': 'user_id: %s does not exist' % user_id}

    @classmethod
    def check_username_exists(cls, username) -> dict:
        user = cls.__model.find_by_username(username)
        if user:
            return {'status': True, 'output': 'username: %s exists' % username, 'user_id': user.id}
        return {'status': False, 'output': 'username: %s does not exist' % username}

    @classmethod
    def check_email_exists(cls, email: str) -> dict:
        user = cls.__model.find_by_email(email)
        if user:
            return {'status': True, 'output': 'e-mail: %s exists' % email}
        return {'status': False, 'output': 'e-mail: %s does not exist' % email}

    def check_user_signup(self, user_data: dict) -> dict:
        username_checking = self.check_username_exists(user_data['username'])
        if username_checking['status']:
            return {'status': False, 'output': username_checking['output']}

        email_checking = self.check_email_exists(user_data['email'])
        if email_checking['status']:
            return {'status': False, 'output': email_checking['output']}

        return {'status': True, 'output': 'everything is correct'}

    def check_email_with_passcode(self, email: str, passcode: str) -> dict:
        user = self.__model.find_by_email(email)
        if not user:
            return {'status': False, 'output': f"user: {email} does not exist"}

        if not user.member:
            return {'status': False, 'output': f"user: {user.username} is not memberized"}

        if not user.verify_passcode(passcode):
            return {'status': False, 'output': f"e-mail: {email} and passcode do not matches"}

        return {'status': True, 'output': user.username}

    #  Creates

    def signup_user(self, user_info: dict) -> dict:
        new_user = self.__model(
            first_name=user_info['first_name'],
            last_name=user_info['last_name'],
            username=user_info['username'],
            sex=user_info['sex'],
            birth_date=user_info['birth_date'],
            email=user_info['email'],
            password=user_info['password']
        )
        return new_user.public_info

    def generate_confirm_token(self, email: str) -> str:
        return self.__serializer.dumps(email, salt=self.__salt)

    def check_token(self, token: str) -> str:
        try:
            return self.__serializer.loads(token, salt=self.__salt, max_age=3600)
        except Exception:
            return ''

    def create_users(self, users_data: dict) -> dict:
        uploaded_users = 0
        for user in users_data['users']:

            username_checking = self.check_username_exists(user['username'])
            if username_checking['status']:
                continue

            email_checking = self.check_email_exists(user['email'])
            if email_checking['status']:
                continue

            self.create_user(user)
            uploaded_users += 1

        return {'message': '%s users were uploaded' % uploaded_users}

    #  Changes

    @staticmethod
    def confirm_user(user: __model) -> dict:
        user.change_status('confirmed')
        return {'message': f"user: {user.email} has been confirmed"}

    def freeze_account(self, email: str) -> dict:
        user = self.__model.find_by_email(email)
        user.change_status('frozen')
        return {
            'message': f"account: {user.email} has been frozen, check mailbox to access recovering"
        }

    def recover_account(self, email: str, new_password: str) -> dict:
        user = self.__model.find_by_email(email)
        user.change_password(new_password)
        user.change_status('confirmed')
        return {
            'message': f"account: {user.email} has been recovered with a new password"
        }

    def __change_user_fields(self, user_id: int, username: str, email: str, password: str) -> list:
        updated_fields = list()
        user = self.__model.find_by_id(user_id)
        if username != '':
            user.username = username
            updated_fields.append('username')
        if email != '':
            user.email = email
            updated_fields.append('email')
        if password != '':
            user.change_password(password)
            updated_fields.append('password')
        user.update()
        return user.public_info

    def change_user_details(self, user_id: int, user_details: dict) -> dict:
        result = self.__change_user_fields(
            user_id=user_id,
            username=user_details['username'],
            email=user_details['email'],
            password=user_details['password']
        )
        return result

    #  Deletes

    @staticmethod
    def delete_user(user: __model) -> dict:
        user.delete()
        return {'message': 'user %s was deleted' % user.username}

    #  Getting some info

    def get_user_public_info(self, user_id: int) -> dict:
        return self.__model.find_by_id(user_id).info

    def get_users_public_info(self) -> dict:
        users_info = list()
        for user in self.__model.find_all():
            users_info.append(user.public_info)
        return {'users': users_info}

    def get_user_status_by_email(self, email: str) -> enumerate:
        user = self.__model.find_by_email(email)
        return user.status.value

    @classmethod
    def get_user(cls, user_id: int) -> __model:
        return cls.__model.find_by_id(user_id)

    @classmethod
    def get_user_by_email(cls, email: str) -> __model:
        return cls.__model.find_by_email(email)

    @classmethod
    def get_user_by_username(cls, username: str):
        return cls.__model.find_by_username(username)

    def get_status_by_username(self, username: str) -> str:
        return self.__model.find_by_username(username).status.value


class AdminController(UserController):
    __model = models.Admin

    @classmethod
    def check_admin_status(cls, status: str) -> dict:
        if status in models.AdminStatus.values():
            return {'status': True, 'output': f'{status} is valid'}
        return {'status': False, 'output': f'{status} is not valid'}

    def check_admin_exists(self, user_id: int) -> dict:
        admin = self.__model.find_by_id(user_id)
        if admin:
            return {'status': True, 'output': f"admin: {user_id} exists"}
        return {'status': False, 'output': f"admin: {user_id} does not exist"}

    def create_admin(self, user_id: int, status: enumerate) -> dict:
        admin_checking = self.check_admin_exists(user_id)
        if admin_checking['status']:
            admin = self.__model.find_by_id(user_id)
            admin.change_status(status)
        else:
            admin = self.__model(user_id, status).upload()
        return admin.info

    @staticmethod
    def delete_admin(admin: __model) -> dict:
        admin_id = admin.id
        admin.delete()
        return {'message': f"admin: {admin_id} was deleted successfully"}

    def get_admin(self, admin_id: int) -> __model:
        return self.__model.find_by_id(admin_id)

    def get_admins_info(self) -> dict:
        admins_info = list()
        for admin in self.__model.find_all():
            admins_info.append(admin.info)
        return {'admins': admins_info}

    @classmethod
    def moder_required(cls, func):
        @wraps(func)
        def decorator(*args, **kwargs):

            current_user = kwargs.get('current_user', None)
            if not current_user:
                UserError('current user is not logged in', 401)

            if not current_user.admin:
                raise UserError(f'user: {current_user.id} has no permissions', 403)

            kwargs['current_moder'] = current_user.admin

            return func(*args, **kwargs)

        return decorator

    @classmethod
    def admin_required(cls, func):
        @wraps(func)
        def decorator(*args, **kwargs):

            current_user = kwargs.get('current_user', None)
            if not current_user:
                UserError('current user is not logged in', 401)

            if not current_user.admin or current_user.role != 'admin':
                raise UserError(f'user: {current_user.id} has no permissions', 403)

            kwargs['current_admin'] = current_user.admin

            return func(*args, **kwargs)

        return decorator


class DeviceController(AdminController):
    __model = models.Device

    #  Checks

    def check_device_name_exists(self, name: str) -> dict:
        device = self.__model.find_by_name(name)
        if not device:
            return {'status': False, 'output': f'device_name: {name} does not exist'}

        return {'status': True, 'output': f'device_name: {name} already exists'}

    @classmethod
    def check_device_key(cls, device) -> dict:
        if not device or device.status.value == 'disable':
            return {'status': False, 'output': f'api_key: ...{device.key[-10:]} is not valid'}
        device.add_request()
        return {'status': True, 'output': f'api_key: ...{device.key[-10:]} is valid'}

    #  Creates

    @classmethod
    def create_device(cls, user_id: int, name: str) -> dict:
        device = cls.__model(user_id, name)
        return device.info

    @classmethod
    def add_device_request(cls, device_key: str):
        device = cls.__model.find_by_key(device_key)
        device.add_request()

    @staticmethod
    def change_device_fields(device: __model, device_data: dict) -> dict:
        updated_fields = list()
        if device_data['name'] != '':
            device.name = device_data['name']
            updated_fields.append('name')
        if device_data['status'] != '':
            device.set_status(device_data['status'])
            updated_fields.append('status')
        if device_data['refresh_key'] is True:
            device.refresh_key()
            updated_fields.append('key')
        return device.info

    #  Deletes

    @staticmethod
    def __delete_device_tokens(tokens: list) -> None:
        for token in tokens:
            token.delete()
        return

    def delete_device(self, device: __model) -> dict:
        device_id = device.id
        if device.tokens:
            self.__delete_device_tokens(device.tokens)
        device.delete()
        return {'message': f"device: {device_id} was deleted successfully"}

    def delete_devices(self, devices: list) -> None:
        for device in devices:
            self.delete_device(device)
        return

    #  Gets

    @classmethod
    def get_device(cls, device_id: int) -> __model:
        return cls.__model.find_by_id(device_id)

    @classmethod
    def get_devices_by_name(cls, name: str) -> dict:
        devices_info = list()
        for device in cls.__model.find_all_by_name(name):
            devices_info.append(device.info)
        return {'devices': devices_info}

    @classmethod
    def get_device_by_key(cls, device_key: str) -> __model:
        return cls.__model.find_by_key(device_key)

    @classmethod
    def api_required(cls, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            headers = request.headers

            api_key = headers.get('X-Api-Key')
            if not api_key:
                raise DeviceError('there is no api-key', 400)

            device = cls.get_device_by_key(api_key)
            if not device:
                raise DeviceError('api-key is not valid', 401)

            key_checking = cls.check_device_key(device)
            if not key_checking['status']:
                raise DeviceError(key_checking['output'], 403)

            kwargs['current_device_id'] = device.id

            return func(*args, **kwargs)

        return decorator


class TokenController(UserController):
    __model = models.Token
    tz = timezone(timedelta(0))
    access_delta = timedelta(minutes=30)
    refresh_delta = timedelta(hours=3)

    #  Gets

    @classmethod
    def now(cls) -> datetime:
        return datetime.now(cls.tz)

    #  Checks

    def check_user_sessions(self, user_id: int, device_id: int) -> dict:
        pass

    @classmethod
    def check_password(cls, user_id, password: str) -> dict:
        user = cls.get_user(user_id)
        if not user.verify_password(password):
            return {'status': False, 'output': 'password is not correct'}
        return {'status': True, 'output': 'welcome'}

    @classmethod
    def check_user_login(cls, user_data: dict) -> dict:
        username_checking = cls.check_username_exists(user_data['username'])
        if not username_checking['status']:
            return {'status': False, 'output': username_checking['output']}

        user_id = username_checking['user_id']
        password_checking = cls.check_password(user_id, user_data['password'])
        if not password_checking['status']:
            return {'status': False, 'output': password_checking['output']}

        return {'status': True, 'output': f'right secrets for {user_id} user'}

    @classmethod
    def check_validity(cls, expires: datetime) -> dict:
        if cls.now() >= expires:
            return {'status': False, 'output': 'expired'}
        return {'status': True, 'output': 'is valid'}

    @classmethod
    def check_user_token_exists(cls, user_id: int, device_id: int) -> dict:
        token = cls.get_token_by_user_and_device(user_id, device_id)
        if token:
            return {'status': True, 'output': f'user_id: {user_id} already has token'}
        return {'status': False, 'output': f'user_id: {user_id} has no token'}

    @classmethod
    def check_access_token(cls, token: __model) -> dict:
        if token.status == 'expires':
            time_ago = cls.now() - token.expires
            return {
                'status': False,
                'output': f'access_token: ...{token.access_token[-10:]} expired {time_ago.timestamp()//60} minutes ago'
            }

        validity_checking = cls.check_validity(token.expires)
        if not validity_checking['status']:
            token.set_expired()
            return {'status': False, 'output': f'access_token: ...{token.access_token[-10:]} is expired'}

        return {'status': True, 'output': f'access_token: ...{token.access_token[-10:]} is valid'}

    @classmethod
    def check_refresh_token(cls, user_id: int, refresh_token: str) -> dict:

        token = cls.__model.find_by_refresh_token(refresh_token)
        if not token:
            return {'status': False, 'output': f"refresh_token: ...{refresh_token[-10:]} is not valid"}

        if token.user_id != user_id:
            return {'status': False,
                    'output': f"refresh_token: ...{refresh_token[-10:]} does not belongs to user: {user_id}"}

        refresh_entity = decode_token(refresh_token)['sub'].replace("'", "\"")
        token_validity = json.loads(refresh_entity)['expires_at']
        token_validity = datetime.fromisoformat(token_validity)

        validity_checking = cls.check_validity(token_validity)
        if not validity_checking['status']:
            token.delete()
            return {'status': False, 'output': f"refresh_token: ...{refresh_token[-10:]} is expired"}

        return {'status': True, 'output': f"refresh_token: ...{refresh_token[-10:]} is valid"}

    #  Creates

    @classmethod
    def create_token(cls, user, device_id: int) -> dict:
        time_now = datetime.now(cls.tz)
        expires_date = time_now + cls.access_delta

        refresh_entity = {'id': user.id, 'expires_at': (time_now + cls.refresh_delta).isoformat()}
        access_token = create_access_token(identity=str(user.entity), expires_delta=cls.access_delta)
        refresh_token = create_refresh_token(identity=str(refresh_entity), expires_delta=cls.refresh_delta)

        old_token = cls.get_token_by_user_and_device(user.id, device_id)
        if old_token:
            old_token.update_data(
                access_token=access_token,
                refresh_token=refresh_token,
                expires=expires_date
            )
            return {'access_token': access_token}, refresh_token

        cls.__model(
            device_id=device_id,
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires=expires_date
        ).upload()

        return {'access_token': access_token}, refresh_token

    @classmethod
    def refresh_access(cls, refresh_token: str) -> dict:
        token = cls.__model.find_by_refresh_token(refresh_token)
        access_token = create_access_token(identity=str(token.user_entity), expires_delta=cls.access_delta)
        token.update_access(access_token, datetime.now() + cls.access_delta)
        return {'access_token': access_token}

    #  Gets

    @classmethod
    def get_token_by_user_and_device(cls, user_id: int, device_id: int):
        return cls.__model.find_by_user_and_device(user_id, device_id)

    @classmethod
    def user_required(cls, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            access_token = request.headers.get('X-Auth-Key', None)
            if not access_token:
                raise UserError('there is no Auth-Key', 400)

            token = cls.__model.find_by_access_token(access_token)
            if not token:
                raise UserError('Auth-Key is not valid', 401)

            if token.device_id != kwargs['current_device_id']:
                raise UserError(f"user: {token.user_id} logged in from another device", 403)

            token_checking = cls.check_access_token(token)
            if not token_checking['status']:
                raise UserError(token_checking['output'], 401)

            user = token.user
            if not user:
                raise UserError(f"user: {token.user_id} not found", 404)

            if user.status.value != 'confirmed':
                raise UserError(f"{user} is not confirmed", 409)

            kwargs['current_user'] = user

            return func(*args, **kwargs)

        return decorator
