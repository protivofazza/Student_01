from marshmallow import Schema, fields, ValidationError, validate


class TagSchema(Schema):
    id = fields.String(dump_only=True)
    tag_name = fields.String(required=True, validate=validate.Length(min=2, max=64))


class AuthorSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=128))
    surname = fields.String(required=True, validate=validate.Length(min=1, max=128))
    num_of_publications = fields.Integer(validate=validate.Range(min=0))


class PostSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=2, max=256))
    body = fields.String(required=True, validate=validate.Length(min=2, max=4096))
    publication_date = fields.DateTime()
    author = fields.String(required=True)
    tag = fields.List(fields.String(), required=True)
    number_of_views = fields.Int(validate=validate.Range(min=0))
