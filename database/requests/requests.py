from dataclasses import dataclass, field

from . import users


@dataclass
class Users:
    @property
    def get_user(self):
        return users.get_user

    @property
    def add_user(self):
        return users.add_user

    @property
    def set_role(self):
        return users.set_role


@dataclass
class Requests:
    users: Users = field(default_factory=Users)
