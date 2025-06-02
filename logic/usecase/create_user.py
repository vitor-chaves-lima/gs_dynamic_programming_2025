import hashlib

from domain.model.user import User
from domain.repository.user_repository import UserRepositoryImpl
from domain.utils.uuid import bytes_to_uuid_str
from logic.dto.input.user import CreateUserInput
from logic.dto.output.user import UserOutput
from logic.exceptions import (
    PasswordTooShortException,
    PasswordConfirmationMismatchException,
    UserAlreadyExistsException
)


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    async def execute(self, input_data: CreateUserInput) -> UserOutput:
        if len(input_data.password) < 6:
            raise PasswordTooShortException()

        if input_data.password != input_data.password_confirmation:
            raise PasswordConfirmationMismatchException()

        existing_user = await self.user_repository.find_by_username(input_data.username)
        if existing_user:
            raise UserAlreadyExistsException(input_data.username)

        password_hash = hashlib.sha256(input_data.password.encode()).hexdigest()

        user = User(
            username=input_data.username,
            email=input_data.email,
            password_hash=password_hash,
            first_name=input_data.first_name,
            last_name=input_data.last_name
        )

        await self.user_repository.save(user)

        return UserOutput(
            id=bytes_to_uuid_str(user.id),
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
