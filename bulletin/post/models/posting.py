from datetime import datetime

from mongoengine import Document, ReferenceField, StringField, DateTimeField, ListField, IntField, LongField

from member.models import Member

from .comment import Comment


class Posting(Document):
    id = LongField(primary_key=True)
    member = ReferenceField(Member)
    title = StringField(max_length=100)
    content = StringField(max_length=500)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    comments = ListField(Comment)
    hits = IntField(default=0)

    meta = {'collection': 'postings'}

    def __eq__(self, other):
        if other is None:
            # todo: NoneTypeException
            raise Exception
        if self.id == other.id:
            return True
        else:
            return False

    @classmethod
    def add(cls, posting):
        cls.objects.create(posting)
