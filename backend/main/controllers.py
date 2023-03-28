from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta, timezone
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from os import getenv
import json

from . import models
# from backend.utils import


class RecipeController:
    __model = models.Recipe

    def create_recipe(self, recipe_data: dict, user_id: int) -> __model:
        new_recipe = self.__model(
            user_id=user_id,
            title=recipe_data['title'],
            description=recipe_data['description'],
            complexity=recipe_data['complexity'],
            cooking_time=recipe_data['cooking_time'],
            instruction=recipe_data['instruction'],
        )
        return new_recipe

    @staticmethod
    def change_recipe_field(recipe_data: dict, recipe: __model) -> __model:
        if recipe_data['title'] != '':
            recipe.title = recipe_data['title']
        if recipe_data['description'] != '':
            recipe.description = recipe_data['description']
        if recipe_data['complexity'] != '':
            recipe.set_complexity(recipe_data['complexity'])
        if recipe_data['cooking_time'] != '':
            recipe.cooking_time = recipe_data['cooking_time']
        if recipe_data['instruction'] != '':
            recipe.instruction = recipe_data['instruction']
        recipe.update()
        return recipe

    def get_recipe(self, recipe_id: int) -> __model:
        return self.__model.find_by_id(recipe_id)

    def get_all_recipes(self) -> dict:
        recipes = list()
        for recipe in self.__model.find_all():
            recipes.append(recipe.info)
        return {'recipes': recipes}
