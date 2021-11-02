from .dto.signup_info import SignUpInfo
from .exceptions import MemberNotFoundException, DuplicatedIdException
from .models import Member


class MemberService:
    def get_member(self, username: str):
        member = Member.get_by_username(username=username)
        if member is None:
            raise MemberNotFoundException
        else:
            return member

    def add_member(self, signup_info: SignUpInfo):
        new_member = Member(
            username=signup_info.username,
            password=signup_info.password
        )
        try:
            return Member.add(new_member)
        except Exception:
            raise DuplicatedIdException
