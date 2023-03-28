from marshmallow import Schema, fields, post_load, validate
from .models import HumanGender, UserStatus, AdminStatus, DeviceStatus
from backend.utils import UnprocessableEntity


class NewDeviceSchema(Schema):
    admin_id = fields.Int(required=True)
    name = fields.Str(validate=[validate.Length(2, 80), validate.Regexp(r"^[a-z0-9-]+$")], required=True)


class SetDeviceSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(validate=[validate.Length(2, 80), validate.Regexp(r"^[a-z0-9-]+$")])
    status = fields.Str(validate=validate.OneOf(DeviceStatus.values()))
    refresh_key = fields.Bool()

    @post_load
    def prepare_data(self, in_data, **kwargs):
        in_data['name'] = in_data.get('name', '').lower()
        in_data['status'] = in_data.get('status', '')
        in_data['refresh_key'] = in_data.get('refresh_key', '')
        if in_data['name'] == in_data['status'] == in_data['refresh_key'] == '':
            raise UnprocessableEntity
        return in_data


class DeviceSchema(Schema):
    id = fields.Int()
    admin_id = fields.Int()
    name = fields.Str()
    status = fields.Str()
    key = fields.Str()


class DevicesSchema(Schema):
    devices = fields.List(fields.Nested(DeviceSchema))


class SetAdminSchema(Schema):
    user_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(AdminStatus.values()))


class AdminSchema(Schema):
    id = fields.Int()
    status = fields.Str(validate=validate.OneOf(AdminStatus.values()))
    fullname = fields.Str()
    username = fields.Str()
    devices = fields.Int()
    time_created = fields.DateTime()


class AdminsSchema(Schema):
    admins = fields.List(fields.Nested(AdminSchema))


class FullAdminSchema(Schema):
    id = fields.Int()
    status = fields.Str()
    fullname = fields.Str()
    username = fields.Str()
    devices = fields.List(fields.Nested(DeviceSchema))
    time_created = fields.DateTime()


class NewUserSchema(Schema):
    first_name = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z]+$")], required=True)
    last_name = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z]+$")], required=True)
    username = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z0-9_]+$")], required=True)
    sex = fields.Str(validate=[validate.OneOf(HumanGender.values())], required=True)
    birth_date = fields.Date(required=True)
    email = fields.Email(validate=[validate.Length(1, 100)], required=True)
    password = fields.Str(validate=[validate.Length(7, 50), validate.Regexp(r"^[a-zA-Z0-9]+$")], required=True)

    @post_load
    def prepare_data(self, in_data, **kwargs):
        in_data['first_name'] = in_data.get('first_name').lower().capitalize()
        in_data['last_name'] = in_data.get('last_name').lower().capitalize()
        in_data['username'] = in_data.get('username').lower()
        in_data['sex'] = in_data.get('sex')
        in_data['birth_date'] = in_data.get('birth_date')
        in_data['email'] = in_data.get('email').lower()
        in_data['password'] = in_data.get('password')
        return in_data


class PublicUserSchema(Schema):
    id = fields.Int()
    fullname = fields.Str()
    username = fields.Str()
    email = fields.Email()
    time_created = fields.DateTime()


class UsersSchema(Schema):
    users = fields.List(fields.Nested(PublicUserSchema))


class NewUsersSchema(Schema):
    users = fields.List(fields.Nested(NewUserSchema))


class DetailUserSchema(Schema):
    username = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z0-9_]+$")])
    email = fields.Email(validate=validate.Length(0, 100))
    password = fields.Str(validate=[validate.Length(7, 50), validate.Regexp(r"^[a-zA-Z0-9]+$")])

    @post_load
    def prepare_data(self, in_data, **kwargs):
        in_data['username'] = in_data.get('username', '').lower()
        in_data['email'] = in_data.get('email', '').lower()
        in_data['password'] = in_data.get('password', '')
        if in_data['username'] == in_data['email'] == in_data['password'] == '':
            raise UnprocessableEntity
        return in_data


class LoginSchema(Schema):
    username = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z0-9_]+$")], required=True)
    password = fields.Str(validate=[validate.Length(7, 50), validate.Regexp(r"^[a-zA-Z0-9]+$")], required=True)

    @post_load
    def prepare_data(self, in_data, **kwargs):
        in_data['username'] = in_data.get('username').lower()
        in_data['password'] = in_data.get('password')
        return in_data


class TokenSchema(Schema):
    access_token = fields.Str()


class OutputSchema(Schema):
    message = fields.Str()

