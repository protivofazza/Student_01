from marshmallow import Schema, fields, ValidationError, validate


class CategorySchema(Schema):
    id = fields.String(required=True, dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=256))
    description = fields.String(required=True, validate=validate.Length(min=1, max=4096))
    parent_category = fields.String()


class ProductsSchema(Schema):
    id = fields.String(required=True, dump_only=True)
    category = fields.String(required=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=256))
    model = fields.String(required=True, validate=validate.Length(min=1, max=512))
    price = fields.Integer(required=True, validate=validate.Range(min=0, min_inclusive=True))
    in_stock = fields.Integer(required=True, validate=validate.Range(min=0, min_inclusive=True))
    number_of_views = fields.Integer(default=0, dump_only=True, validate=validate.Range(min=0, min_inclusive=True))
