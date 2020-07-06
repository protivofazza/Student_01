from flask_restful import Resource
from flask import request, jsonify
from models import Tag, Author, Post
from schemas import TagSchema, AuthorSchema, PostSchema, ValidationError
import json
from mongoengine import DoesNotExist, ValidationError as Val_error


class TagResource(Resource):

    def get(self, tag_id=None):
        if tag_id:
            try:
                tag = Tag.objects.get(id=tag_id)
                posts = Post.objects.filter(tag__contains=tag)

                tag = TagSchema().dump(tag)
                posts = PostSchema().dump(posts, many=True)

                data = {'tag': tag, 'posts': posts}
            except DoesNotExist as error:
                data = "За введеним ID наразі немає записів (або отриманий запис має посилання на " \
                       "інший неіснуючий): " + str(error)
            except Val_error as error:
                data = "Введений ID у невірному форматі або неіснуючий: " + str(error)
            return jsonify(data)
        else:
            tags = Tag.objects
            return TagSchema().dump(tags, many=True)

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = TagSchema().loads(json_data)
            res = json.loads(TagSchema().dumps(res))
            Tag.objects.create(**res).save().to_json()
        except ValidationError as error:
            res = error.messages

        return res

    def put(self, tag_id):
        try:
            json_data = json.dumps(request.json)
            try:
                tag_data = TagSchema().loads(json_data)
                tag_data = json.loads(TagSchema().dumps(tag_data))

                tag = Tag(id=tag_id)
                tag.update(id=tag_id, **tag_data)
            except ValidationError as error:
                tag_data = error.messages
            return tag_data
        except Val_error as error:
            data = "Введений ID у невірному форматі або неіснуючий: " + str(error)
            return data

    def delete(self, tag_id):
        try:
            tag_to_delete = Tag.objects.get(id=tag_id)
            tag_to_delete = TagSchema().dump(tag_to_delete)

            tag = Tag(id=tag_id)
            tag.delete()
            return tag_to_delete
        except DoesNotExist as error:
            data = "За введеним ID наразі немає записів: " + str(error)
            return data
        except Val_error as error:
            data = "Введений ID у невірному форматі: " + str(error)
            return data


class AuthorResource(Resource):

    def get(self, author_id=None):
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
                author_posts = Post.objects.filter(author=author_id)

                author = AuthorSchema().dump(author)
                author_posts = PostSchema(exclude=['author']). \
                    dump(author_posts, many=True)

                data = {'author': author, 'posts': author_posts}
                return data
            except DoesNotExist as error:
                data = "За введеним ID наразі немає записів (або отриманий запис має посилання на " \
                       "інший неіснуючий): " + str(error)
                return jsonify(data)
            except Val_error as error:
                data = "Введений ID у невірному форматі:" + str(error)
                return jsonify(data)
        else:
            authors = Author.objects
            return AuthorSchema().dump(authors, many=True)

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = AuthorSchema().loads(json_data)
            res = json.loads(AuthorSchema().dumps(res))
            Author.objects.create(**res).save().to_json()
        except ValidationError as error:
            res = error.messages
        return res

    def put(self, author_id):
        try:
            json_data = json.dumps(request.json)
            try:
                author_data = AuthorSchema().loads(json_data)
                author_data = json.loads(AuthorSchema().dumps(author_data))

                tag = Author(id=author_id)
                tag.update(id=author_id, **author_data)
            except ValidationError as error:
                author_data = error.messages
            return author_data
        except DoesNotExist as error:
            data = "За введеним ID наразі немає записів: " + str(error)
            return data
        except Val_error as error:
            data = "Введений ID у невірному форматі: " + str(error)
            return data

    def delete(self, author_id):
        try:
            author_to_delete = Author.objects.get(id=author_id)
            author_to_delete = AuthorSchema().dump(author_to_delete)

            tag = Author(id=author_id)
            tag.delete()
            return author_to_delete
        except DoesNotExist as error:
            data = "За введеним ID наразі немає записів: " + str(error)
            return data
        except Val_error as error:
            data = "Введений ID у невірному форматі: " + str(error)
            return data


class PostResource(Resource):

    def get(self, post_id=None):
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                post.number_of_views += 1
                post.save()

                return PostSchema().dump(post)
            except DoesNotExist as error:
                data = "За введеним ID наразі немає записів (або отриманий запис має посилання на " \
                       "інший неіснуючий): " + str(error)
                return data
            except Val_error as error:
                data = "Введений ID у невірному форматі:" + str(error)
                return jsonify(data)
        else:
            try:
                posts = Post.objects
                return PostSchema().dump(posts, many=True)
            except DoesNotExist as error:
                data = "Один з отриманих записів має посилання на інший неіснуючий: " + str(error)
                return data

    def post(self):
        json_data = json.dumps(request.json)
        try:
            result = PostSchema().loads(json_data)
            res = json.loads(PostSchema().dumps(result))
            Post.objects.create(**res).save().to_json()

            author = Author.objects.get(id=result['author'])
            author.num_of_publications += 1
            author.save()
        except ValidationError as error:
            res = error.messages
        return res

        def put(self, post_id):
        json_data = json.dumps(request.json)
        try:
            try:
                post_data = PostSchema().loads(json_data)
                post_data = json.loads(PostSchema().dumps(post_data))
                post = Post(id=post_id)

                reference_tags_list = post_data['tag']
                tag_list_updated = []
                for tag_str in reference_tags_list:
                    reference_tag = Tag.objects.filter(id=tag_str)
                    tag_list_updated.append(reference_tag[0].id)
                    
                reference_author = Author.objects.filter(id=post_data['author'])

                post.update(id=post_id,
                            body=post_data['body'],
                            title=post_data['title'],
                            author=reference_author[0].id,
                            tag=tag_list_updated)
            except ValidationError as error:
                post_data = error.messages
            return post_data
        except Val_error as error:
            data = "Введений ID у невірному форматі або неіснуючий: " + str(error)
            return data

    def delete(self, post_id):
        try:
            post_to_delete = Post.objects.get(id=post_id)
            post_to_delete = PostSchema().dump(post_to_delete)

            author_str = post_to_delete['author']
            author_list = author_str.split()
            author = Author.objects.filter(name=author_list[0], surname=author_list[1])[0]
            author = Author.objects.get(id=author.id)
            author.num_of_publications -= 1
            author.save()

            tag = Post(id=post_id)
            tag.delete()
            return post_to_delete
        except DoesNotExist as error:
            data = "За введеним ID наразі немає записів: " + str(error)
            return data
        except Val_error as error:
            data = "Введений ID у невірному форматі: " + str(error)
            return data
