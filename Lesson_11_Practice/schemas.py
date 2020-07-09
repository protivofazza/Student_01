from marshmallow import Schema, ValidationError, validate, fields


class PersonSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=128))
    surname = fields.String(validate=validate.Length(min=1, max=128))
    phone_number = fields.String(validate=validate.Length(min=13, max=13))
    email = fields.Email()
    address = fields.String(validate=validate.Length(min=2, max=512))
    info = fields.String(validate=validate.Length(min=2, max=4096))


class StatusSchema(Schema):
    status = fields.Int()
    person_id = fields.Nested(PersonSchema)
