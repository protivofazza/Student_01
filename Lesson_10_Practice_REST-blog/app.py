from flask import Flask
from flask_restful import Api
from resources import TagResource, AuthorResource, PostResource


app = Flask(__name__)
api = Api(app)
api.add_resource(TagResource, '/tags', '/tags/<tag_id>')
api.add_resource(AuthorResource, '/authors', '/authors/<author_id>')
api.add_resource(PostResource, '/posts', '/posts/<post_id>')


if __name__ == '__main__':
    app.run(debug=True)
