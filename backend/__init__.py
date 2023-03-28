from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from os import getenv
import logging

from .database import db, migrate
from .utils import read_api_config
from .config import CONFIGS
from .utils import read_api_config, api_key_scheme, jwt_scheme, mail


API_CONFIG = read_api_config()


def add_security(app):

    JWTManager(app)
    Bcrypt(app)
    CORS(app)

    return app


def create_spec_and_doc(app):
    spec = APISpec(
        title=API_CONFIG["TITLE"],
        version=API_CONFIG["API_VERSION"],
        plugins=[MarshmallowPlugin()],
        openapi_version=API_CONFIG["OPENAPI_VERSION"]
    )
    spec.components.security_scheme('apiKeyAuth', api_key_scheme)
    spec.components.security_scheme('JWT', jwt_scheme)
    app.config.update({
        "APISPEC_SPEC": spec,
        "APISPEC_SWAGGER_URL": API_CONFIG["SWAGGER_URL"],
        "APISPEC_SWAGGER_UI_URL": API_CONFIG["SWAGGER_UI_URL"]
    })

    api = Api(app, prefix='/api')
    docs = FlaskApiSpec(app)

    def add_component(component, component_route):
        api.add_resource(component, component_route)
        docs.register(component)

    from .auth import endpoints as auth_endpoints
    add_component(auth_endpoints.AddAdminApi, '/admin')
    add_component(auth_endpoints.AdminApi, '/admin/<int:admin_id>')
    add_component(auth_endpoints.AdminsApi, '/admins')
    add_component(auth_endpoints.AddDeviceApi, '/device')
    add_component(auth_endpoints.DeviceApi, '/device/<int:device_id>')
    add_component(auth_endpoints.AddUserApi, '/user')
    add_component(auth_endpoints.UserApi, '/user/<int:user_id>')
    add_component(auth_endpoints.UsersApi, '/users')
    # add_component(auth_endpoints.ConfirmUserApi, '/confirm-user/<string:confirm_token>')
    add_component(auth_endpoints.TokenApi, '/token')
    add_component(auth_endpoints.RefreshTokenApi, '/refresh-token')

    from .main import endpoints as main_endpoints
    add_component(main_endpoints.AddRecipeApi, '/recipe')
    add_component(main_endpoints.RecipeApi, '/recipe/<int:recipe_id>')
    add_component(main_endpoints.RecipesApi, '/recipes')

    return app


def create_app():
    app_config = CONFIGS.get(getenv('APP_MODE'), 'dev')

    flask_app = Flask(__name__)
    flask_app.config.from_object(app_config)

    flask_app = add_security(flask_app)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    # mail.init_app(flask_app)

    flask_app = create_spec_and_doc(flask_app)

    logging.basicConfig(
        filename='record.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s : %(message)s'
    )

    return flask_app

