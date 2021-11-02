from .models import Member


class MemberService:
    def get_member(self, username: str):
        return Member.get_by_username(username=username)

