from .dto.signup_info import SignUpInfo
from .models import Member


class MemberService:
    def get_member(self, username: str):
        member = Member.get_by_username(username=username)
        if member is None:
            # todo: MemberNotFoundException
            raise Exception
        else:
            return member

    def add_member(self, signup_info: SignUpInfo):
        new_member = Member(
            username=signup_info.username,
            password=signup_info.password
        )
        try:
            return Member.add(new_member)
        except Exception as e:
            # todo: duplicated ID exception
            raise e
