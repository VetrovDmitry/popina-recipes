from flask import current_app, after_this_request, request
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from . import controllers
from . import schemas
from backend.utils import (UserError, TokenError, DeviceError, AdminError, MailError, MailController,
                           error_handler, ep_responses, device_header, user_header)

api_required = controllers.DeviceController.api_required
user_required = controllers.TokenController.user_required
moder_required = controllers.AdminController.moder_required
admin_required = controllers.AdminController.admin_required


ADMIN = 'Admin operations'


class AddDeviceApi(MethodResource):
    __controller = controllers.DeviceController()
    __schemas = {
        'request': schemas.NewDeviceSchema,
        'contribution': schemas.SetDeviceSchema,
        'response': schemas.DeviceSchema,
        'output': schemas.OutputSchema
    }
    decorators = [
        admin_required,
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[ADMIN],
         summary='creates Device entity',
         description='Receives Device info',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current admin has now permission"),
                                 (404, "user not found"),
                                 (409, "device-name exists")]))
    @use_kwargs(__schemas['request'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def post(self, **device_data) -> tuple:

        current_user = device_data['current_user']

        if current_user.role != 'admin':
            raise UserError(f"user: {current_user.id} has no permission", 403)

        admin_checking = self.__controller.check_admin_exists(device_data['admin_id'])
        if not admin_checking['status']:
            raise UserError(admin_checking['output'], 404)

        device_checking = self.__controller.check_device_name_exists(device_data['name'])
        if device_checking['status']:
            raise DeviceError(device_checking['output'], 409)

        result = self.__controller.create_device(device_data['admin_id'], device_data['name'])
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"{current_user} created device: {result['id']}:{result['name']}")

        return response, 201

    @doc(tags=[ADMIN],
         summary='updates Device details',
         description='Receives changed Device info',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current admin has no permissions"),
                                 (404, "device does not exist"),
                                 (409, "device is already enable/disable")]))
    @use_kwargs(__schemas['contribution'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def put(self, **device_data):

        current_user = device_data['current_user']

        device = self.__controller.get_device(device_data['id'])
        if not device:
            raise DeviceError(f"device: {device_data['id']} not found", 404)

        if current_user.role != 'admin':
            raise DeviceError(f"user: {current_user.id} has no permissions for device: {device.id}", 403)

        if device_data['status'] == device.status.value:
            raise DeviceError(f"device: {device.id} is already {device_data['status']}", 409)

        result = self.__controller.change_device_fields(device, device_data)
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"{current_user} updated {device}")

        return response, 201


class DeviceApi(MethodResource):
    __controller = controllers.DeviceController()
    __schemas = {
        'response': schemas.DeviceSchema,
        'output': schemas.OutputSchema
    }
    decorators = [
        admin_required,
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[ADMIN],
         summary='returns Device entity',
         description='receives device_id',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current admin has no permission"),
                                 (404, "device not found")]))
    @marshal_with(__schemas['response'], code=200)
    def get(self, device_id, **kwargs):

        current_user = kwargs['current_user']

        device = self.__controller.get_device(device_id)
        if not device:
            raise DeviceError(f"device: {device_id} not found", 404)

        if device.admin_id != current_user.id and current_user.role != 'admin':
            raise DeviceError(f"admin: {current_user.id} has no permission for device: {device_id}", 403)

        response = self.__schemas['response']().load(device.info)
        current_app.logger.info(f"sent to {current_user} {device} info")
        return response, 200

    @doc(tags=[ADMIN],
         summary='refreshes Device`s key',
         description='Receives device_id',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current admin has now permission"),
                                 (404, "device not found"),
                                 (409, "device is not enable")]))
    @marshal_with(__schemas['response'], code=201)
    def patch(self, device_id, **kwargs):

        current_user = kwargs['current_user']

        device = self.__controller.get_device(device_id)
        if not device:
            raise DeviceError(f"device: {device_id} not found", 404)

        if device.admin_id != current_user.id and current_user.role != 'admin':
            raise DeviceError(f"admin: {current_user.id} has no permission for device: {device.id}", 403)

        if device.status.value != 'enable':
            raise DeviceError(f"device: {device_id} is not enable", 409)

        device.refresh_key()
        response = self.__schemas['response']().load(device.info)

        current_app.logger.info(f"{current_user} refreshed key of {device}")

        return response, 201

    @doc(tags=[ADMIN],
         summary='deletes Device entity and chained tokens',
         description='Receives  admin_id',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current admin has no permissions"),
                                 (404, "device not found")]))
    @marshal_with(__schemas['output'], code=204)
    def delete(self, device_id, **kwargs):

        current_user = kwargs['current_user']

        device = self.__controller.get_device(device_id)
        if not device:
            raise DeviceError(f"device: {device_id} not found", 404)

        if device.admin_id != current_user.id and current_user.role != 'admin':
            raise DeviceError(f"user: {current_user.id} has no permission for device: {device.id}", 403)

        result = self.__controller.delete_device(device)
        output = self.__schemas['output']().load(result)

        current_app.logger.info(f"{current_user} deleted {device} successfully")

        return output, 204


class AddAdminApi(MethodResource):
    __controller = controllers.AdminController()
    __schemas = {
        'request': schemas.SetAdminSchema,
        'response': schemas.FullAdminSchema,
        'output': schemas.OutputSchema
    }
    decorators = [
        api_required,
        user_required,
        admin_required,
        error_handler
    ]

    @doc(tags=[ADMIN],
         summary='updates User role',
         description='Receives user_id and role',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current user has no permissions"),
                                 (404, "sent user or user-status not found")]))
    @use_kwargs(__schemas['request'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def post(self, **user_data):

        current_user = user_data['current_user']

        if current_user.role != 'admin':
            raise UserError(f"admin: {current_user.id} has no permission", 403)

        user_checking = self.__controller.check_user_exists(user_data['user_id'])
        if not user_checking['status']:
            raise UserError(user_checking['output'], 404)

        result = self.__controller.create_admin(user_data['user_id'], user_data['status'])
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"{current_user} upgraded user: {user_data['user_id']} to {user_data['status']}")

        return response, 201


class AdminApi(MethodResource):
    __controller = controllers.DeviceController()
    __schemas = {
        'response': schemas.AdminSchema,
        'output': schemas.OutputSchema
    }
    decorators = [
        admin_required,
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[ADMIN],
         summary='returns Admin info',
         description='Receives admin_id',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current admin has no permissions"),
                                 (404, "admin not found")]))
    @marshal_with(__schemas['response'], code=200)
    def get(self, admin_id, **kwargs):

        current_user = kwargs['current_user']

        admin = self.__controller.get_admin(admin_id)
        if not admin:
            raise AdminError(f"admin: {current_user.id} not found", 404)

        if admin.id != current_user.id and current_user.role != 'admin':
            raise AdminError(f"admin: {current_user.id} has no permission for admin: {admin.id}", 403)

        response = self.__schemas['response']().load(admin.info)
        current_app.logger.info(f"sent to {current_user} info of {admin}")

        return response, 200

    @doc(tags=[ADMIN],
         summary='deletes Admin entity and chained devices',
         description='Receives  admin_id',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current admin has no permissions"),
                                 (404, "admin not found")]))
    @marshal_with(__schemas['output'], code=204)
    def delete(self, admin_id, **kwargs):

        current_user = kwargs['current_user']

        admin = self.__controller.get_admin(admin_id)
        if not admin:
            raise AdminError(f"admin: {admin_id} not found", 404)

        if admin.id != current_user.id and current_user.role != 'admin':
            raise AdminError(f"admin: {current_user.id} has no permission for admin: {admin.id}", 403)

        if admin.devices:
            self.__controller.delete_devices(admin.devices)

        result = self.__controller.delete_admin(admin)
        output = self.__schemas['output']().load(result)

        current_app.logger.info(f"{current_user} deleted {admin}")

        return output, 204


class AdminsApi(MethodResource):
    __controller = controllers.AdminController()
    __schemas = {
        'response': schemas.AdminsSchema
    }
    decorators = [
        admin_required,
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[ADMIN],
         summary='returns list of Admin entities',
         description='receives admin name',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current user has no permission")]))
    @marshal_with(__schemas['response'], code=200)
    def get(self, **kwargs):

        current_user = kwargs['current_user']

        if current_user.role != 'admin':
            raise AdminError(f"admin: {current_user.id} has no permission for admins", 403)

        result = self.__controller.get_admins_info()
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"sent to {current_user} all admins info")

        return response, 200


AUTH = 'Auth operations'


class AddUserApi(MethodResource):
    __controller = controllers.UserController()
    __mail_controller = MailController()
    __schemas = {
        'request': schemas.NewUserSchema,
        'response': schemas.PublicUserSchema
    }
    decorators = [
        api_required,
        error_handler
    ]

    @doc(tags=[AUTH],
         summary='uploads new user',
         description='receives new user info',
         security=[device_header],
         responses=ep_responses([(409, "username or email exists")]))
    @use_kwargs(__schemas['request'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def post(self, **user_data):

        username_checking = self.__controller.check_username_exists(user_data['username'])
        if username_checking['status']:
            raise UserError(username_checking['output'], 409)

        email_checking = self.__controller.check_email_exists(user_data['email'])
        if email_checking['status']:
            raise UserError(email_checking['output'], 409)

        result = self.__controller.signup_user(user_data)
        # confirm_token = self.__controller.generate_confirm_token(result['email'])
        # self.__mail_controller.send_confirmation(result['email'], result['fullname'], confirm_token)
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"user: {result['id']} signed up")

        return response, 201


class ConfirmUserApi(MethodResource):
    __controller = controllers.UserController()
    __mail_controller = MailController()
    __schemas = {
        'output': schemas.OutputSchema
    }
    decorators = [
        api_required,
        error_handler
    ]

    @doc(tags=[AUTH],
         summary='confirms User entity after registration',
         description='receives confirm token',
         security=[device_header],
         responses=ep_responses([(404, "token or email is not valid"),
                                 (409, "user status is not unconfirmed")]))
    @marshal_with(__schemas['output'], code=204)
    def patch(self, confirm_token, **user_data):

        email = self.__controller.check_token(confirm_token)
        if email == '':
            raise MailError('sent confirm_token is not valid', 404)

        user = self.__controller.get_user_by_email(email)
        if not user:
            raise UserError('User with such email doesn`t exist', 404)

        if user.status.value != 'unconfirmed':
            raise UserError(f'user: {user.id} is not unconfirmed', 409)

        result = self.__controller.confirm_user(user)
        output = self.__schemas['output']().load(result)

        current_app.logger.info(f"user: {user.id} has confirmed itself")

        return output, 204


class TokenApi(MethodResource):
    __controller = controllers.TokenController()
    __schemas = {
        'request': schemas.LoginSchema,
        'response': schemas.TokenSchema
    }
    decorators = [
        api_required,
        error_handler
    ]

    @doc(tags=[AUTH],
         summary='creates auth token',
         description='Receives User login data',
         security=[device_header],
         responses=ep_responses([(401, "wrong password"),
                                 (403, "current user is not confirmed"),
                                 (404, "username not found")]))
    @use_kwargs(__schemas['request'], location='form')
    @marshal_with(__schemas['response'], code=202)
    def post(self, **user_data):

        user = self.__controller.get_user_by_username(user_data['username'])
        if not user and not user.admin:
            raise TokenError(f"user: {user_data['username']} not found", 404)

        if not user.verify_password(user_data['password']):
            raise TokenError(f"wrong password", 401)

        if user.status.value != 'confirmed':
            raise TokenError(f"user: {user.username} is not confirmed", 403)

        result, cookie = self.__controller.create_token(user, user_data['current_device_id'])
        response = self.__schemas['response']().load(result)

        @after_this_request
        def set_refresh_cookie(resp):
            resp.set_cookie(
                key='refresh_token',
                value=cookie,
                httponly=True,
                max_age=self.__controller.refresh_delta.seconds
            )
            return resp

        current_app.logger.info(f"{user} logged in ")

        return response, 202


class RefreshTokenApi(MethodResource):
    __controller = controllers.TokenController()
    __schemas = {
        'response': schemas.TokenSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[AUTH],
         summary='refreshes auth token',
         description='Receives refresh_token',
         security=[device_header, user_header],
         responses=ep_responses([(400, "have not refresh-token in sent cookie"),
                                 (401, "refresh-token is not valid")]))
    @marshal_with(__schemas['response'], code=202)
    def patch(self, **user_data):

        current_user = user_data['current_user']

        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            raise TokenError('there is no refresh token in cookies', 400)

        token_checking = self.__controller.check_refresh_token(current_user.id, refresh_token)
        if not token_checking['status']:
            raise TokenError(token_checking['output'], 401)

        result = self.__controller.refresh_access(refresh_token)
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"{current_user} refreshed access")

        return response, 202


class UserApi(MethodResource):
    __controller = controllers.UserController()
    __schemas = {
        'response': schemas.PublicUserSchema,
        'output': schemas.OutputSchema,
        'request': schemas.DetailUserSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[AUTH],
         summary='returns User entity by id',
         description='Sends User public info dictionary',
         security=[device_header, user_header],
         responses=ep_responses([(404, "user does not exist")]))
    @marshal_with(__schemas['response'], code=200)
    def get(self, user_id, **kwargs):

        current_user = kwargs['current_user']

        user = self.__controller.get_user(user_id)

        if not user:
            raise UserError(f"user: {user_id} not found", 404)

        response = self.__schemas['response']().load(user.public_info)

        current_app.logger.info(f"sends to {current_user} public info of {user}")

        return response, 200

    @doc(tags=[AUTH],
         summary='updates User details',
         description='Receives changed User info',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current user has no permissions"),
                                 (404, "user_id does not exist"),
                                 (409, "passwords do not match")]))
    @use_kwargs(__schemas['request'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def put(self, user_id, **user_data):

        current_user = user_data['current_user']
        if current_user.id != user_id and current_user.role.value != 'Admin':
            raise UserError('current user has no permissions', 403)

        user_checking = self.__controller.check_user_exists(user_id)
        if not user_checking['status']:
            raise UserError(user_checking['output'], 404)

        repeat_checking = self.__controller.check_user_signup(user_data)
        if not repeat_checking['status']:
            raise UserError(repeat_checking['output'], 409)

        result = self.__controller.change_user_details(user_id, user_data)
        response = self.__schemas['response']().load(data=result)

        current_app.logger.info(f"{current_user} updated details of user: {user_id}")

        return response, 201

    @doc(tags=[AUTH],
         summary='deletes User and Member entity',
         description='Receives User id',
         security=[device_header, user_header],
         responses=ep_responses([(403, "current user has no permissions"),
                                 (404, "user_id does not exist")]))
    @marshal_with(__schemas['output'], code=204)
    def delete(self, user_id, **kwargs):

        current_user = kwargs['current_user']

        user = self.__controller.get_user(user_id)
        if not user:
            raise UserError(f"user: {user_id} not found", 404)

        if user.id != current_user.id and current_user.role != 'admin':
            raise UserError(f"user: {current_user.id} has no permission for user: {user_id}", 403)

        result = self.__controller.delete_user(user)
        output = self.__schemas['output']().load(result)

        current_app.logger.info(f"{current_user} deleted user: {user_id}")

        return output, 204


class UsersApi(MethodResource):
    __controller = controllers.UserController()
    __schemas = {
        'response': schemas.UsersSchema,
        'output': schemas.OutputSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[AUTH],
         summary='returns User entities',
         description='Sends list of User public info',
         security=[device_header, user_header])
    @marshal_with(__schemas['response'], code=200)
    def get(self, **kwargs):
        current_user = kwargs['current_user']

        users = self.__controller.get_users_public_info()
        response = self.__schemas['response']().load(users)

        current_app.logger.info(f"sends to {current_user} all users public info")

        return response, 200
