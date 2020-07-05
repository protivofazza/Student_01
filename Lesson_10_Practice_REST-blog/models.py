import mongoengine as me
import datetime

me.connect('Blog_Lesson_10')


class Tag(me.Document):
    tag_name = me.StringField(min_length=2, max_length=64)

    def __str__(self):
        return f"#{self.tag_name}"


class Author(me.Document):
    name = me.StringField(min_length=1, max_length=128)
    surname = me.StringField(min_length=1, max_length=128)
    num_of_publications = me.IntField(min_value=0, default=0)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Post(me.Document):
    author = me.ReferenceField(Author)
    title = me.StringField(min_length=2, max_length=256, required=True)
    body = me.StringField(min_length=2, max_length=4096, required=True)
    publication_date = me.DateTimeField(default=datetime.datetime.now())
    tag = me.ListField(me.ReferenceField(Tag))
    number_of_views = me.IntField(default=0)

    def __str__(self):
        return f"'{self.title}'       ({self.author})\n" \
               f"{self.body}\n" \
               f"tags: {self.tag}       '{self.publication_date}'"
