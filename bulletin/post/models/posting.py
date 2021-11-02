from datetime import datetime

from mongoengine import Document, ReferenceField, StringField, DateTimeField, ListField, IntField

from member.models import Member

from .comment import Comment
from ..dto.post_details import PostDetails


class Posting(Document):
    id = IntField(primary_key=True)
    member = ReferenceField(Member)
    title = StringField(max_length=100)
    content = StringField(max_length=500)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    comments = ListField(Comment)
    hits = IntField(default=0)

    meta = {'collection': 'postings'}

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if other is None:
            # todo: NoneTypeException
            raise Exception
        if self.id == other.id:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.comments.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.comments.delete()
        super().delete(*args, **kwargs)

    def to_details(self):
        return PostDetails(
            id=self.id,
            author=self.member.username,
            title=self.title,
            content=self.content,
            created_at=self.created_at.strftime("%m-%d-%Y, %H:%M:%S"),
            updated_at=self.updated_at.strftime("%m-%d-%Y, %H:%M:%S"),
            comments=list(self.comments),
            hits=self.hits
        )

    @classmethod
    def add(cls, posting):
        cls.objects.create(posting)

    @classmethod
    def get_by_id(cls, post_id):
        return cls.objects(id=post_id).first()

    @classmethod
    def get_partial(cls, offset, limit):
        return list(cls.objects.skip(offset).limit(offset+limit))
