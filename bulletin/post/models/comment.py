from datetime import datetime

from mongoengine import ReferenceField, StringField, NULLIFY, DateTimeField, Document

from member.models import Member


class Comment(Document):
    commenter = ReferenceField(Member)
    content = StringField(max_length=200)
    parent = ReferenceField("self", reverse_delete_rule=NULLIFY)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'comments'}
