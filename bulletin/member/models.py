from mongoengine import Document, StringField

from .exceptions import NoneTypeException


class Member(Document):
    username = StringField(max_length=50)
    password = StringField(max_length=1000)

    meta = {
        'collection': 'members',
        'indexes': [
            {'fields': ['username'], 'unique': True},
        ],
    }

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if other is None:
            raise NoneTypeException
        if self.username == other.username:
            return True
        else:
            return False

    @classmethod
    def get_by_username(cls, username: str):
        return cls.objects(username=username).first()

    @classmethod
    def add(cls, member):
        member.save()
