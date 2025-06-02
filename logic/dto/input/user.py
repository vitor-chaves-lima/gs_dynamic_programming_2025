from dataclasses import dataclass


@dataclass
class CreateUserInput:
    username: str
    email: str
    password: str
    password_confirmation: str
    first_name: str
    last_name: str

@dataclass
class LoginInput:
    username: str
    password: str