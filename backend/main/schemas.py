from marshmallow import Schema, fields, post_load, validate
from .models import RecipeComplexity
from backend.utils import UnprocessableEntity


class NewRecipeSchema(Schema):
    title = fields.Str(validate=[validate.Length(1, 80), validate.Regexp(r"^[a-zA-Z- ]+$")], required=True)
    description = fields.Str(validate=[validate.Regexp(r"^[a-zA-Z0-9- ]+$")], required=True)
    complexity = fields.Str(validate=validate.OneOf(RecipeComplexity.values()), required=True)
    cooking_time = fields.Int(required=True)
    instruction = fields.Str(required=True)


class DetailRecipeSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(validate=[validate.Length(1, 80), validate.Regexp(r"^[a-zA-Z- ]+$")])
    description = fields.Str(validate=[validate.Regexp(r"^[a-zA-Z- ]+$")])
    complexity = fields.Str(validate=validate.OneOf(RecipeComplexity.values()))
    cooking_time = fields.Int()
    instruction = fields.Str(validate=[validate.Regexp(r"^[a-zA-Z0-9- ]+$")])

    @post_load
    def prepare_data(self, in_data, **kwargs):
        in_data['title'] = in_data.get('title', '')
        in_data['description'] = in_data.get('description', '')
        in_data['complexity'] = in_data.get('complexity', '')
        in_data['cooking_time'] = in_data.get('cooking_time', '')
        in_data['instruction'] = in_data.get('instruction', '')
        if in_data['title'] == in_data['description'] == in_data['complexity'] \
                == in_data['cooking_time'] == in_data['instruction'] == '':
            raise UnprocessableEntity
        return in_data


class RecipeSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    complexity = fields.Str()
    cooking_time = fields.Int()
    instruction = fields.Str()
    time_created = fields.DateTime()


class RecipesSchema(Schema):
    recipes = fields.List(fields.Nested(RecipeSchema))
