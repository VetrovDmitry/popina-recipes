from flask import current_app, after_this_request, request
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from . import controllers
from . import schemas
from backend.auth import controllers as auth_controllers
from backend.utils import (UserError, TokenError, DeviceError, AdminError, RecipeError, MailController,
                           error_handler, ep_responses, device_header, user_header)


api_required = auth_controllers.DeviceController.api_required
user_required = auth_controllers.TokenController.user_required
moder_required = auth_controllers.AdminController.moder_required
admin_required = auth_controllers.AdminController.admin_required


MAIN = 'Main operations'


class AddRecipeApi(MethodResource):
    __controller = controllers.RecipeController()
    __schemas = {
        'request': schemas.NewRecipeSchema,
        'contribution': schemas.DetailRecipeSchema,
        'response': schemas.RecipeSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[MAIN],
         summary='creates new recipe',
         description='Receives recipe info',
         security=[device_header, user_header],
         responses=ep_responses([(422, "not valid schema")]))
    @use_kwargs(__schemas['request'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def post(self, **recipe_data):
        current_user = recipe_data['current_user']

        new_recipe = self.__controller.create_recipe(recipe_data, current_user.id)

        response = self.__schemas['response']().load(new_recipe.info)

        current_app.logger.info(f"{current_user} created {new_recipe}")

        return response, 201

    @doc(tags=[MAIN],
         summary='updates Recipe details',
         description='Receives changed User info',
         security=[device_header, user_header],
         responses=ep_responses([(404, "recipe_id does not exist")]))
    @use_kwargs(__schemas['contribution'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def put(self, **recipe_data):
        current_user = recipe_data['current_user']

        recipe = self.__controller.get_recipe(recipe_data['id'])
        if not recipe:
            raise RecipeError(f"recipe: {recipe_data['id']} not found")

        updated_recipe = self.__controller.change_recipe_field(recipe_data, recipe)
        response = self.__schemas['response']().load(updated_recipe.info)

        current_app.logger.info(f"{current_user} updated {recipe}")

        return response, 201





class RecipeApi(MethodResource):
    __controller = controllers.RecipeController()
    __schemas = {
        'response': schemas.RecipeSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[MAIN],
         summary='returns Recipe info',
         description='Receives recipe_id',
         security=[device_header, user_header],
         responses=ep_responses([(404, "recipe not found")]))
    @marshal_with(__schemas['response'], code=200)
    def get(self, recipe_id, **kwargs):
        current_user = kwargs['current_user']

        recipe = self.__controller.get_recipe(recipe_id)
        if not recipe:
            raise RecipeError(f"recipe: {recipe_id} not found", 404)

        response = self.__schemas['response']().load(recipe.info)
        current_app.logger.info(f"sent to {current_user} info of {recipe}")

        return response, 200


class RecipesApi(MethodResource):
    __controller = controllers.RecipeController()
    __schemas = {
        'response': schemas.RecipesSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[MAIN],
         summary='returns Recipes info',
         description='sends list of recipe entities',
         security=[device_header, user_header])
    @marshal_with(__schemas['response'], code=200)
    def get(self, **kwargs):
        current_user = kwargs['current_user']

        result = self.__controller.get_all_recipes()
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"sent to {current_user} all recipes info")

        return response, 200


