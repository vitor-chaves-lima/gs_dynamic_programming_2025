import hashlib
import jwt
import datetime

from domain.repository.user_repository import UserRepositoryImpl
from domain.utils.uuid import bytes_to_uuid_str
from logic.dto.input.user import LoginInput
from logic.dto.output.user import LoginOutput
from logic.exceptions import InvalidCredentialsException


class LoginUseCase:
    def __init__(self, user_repository: UserRepositoryImpl, secret_key: str):
        self.user_repository = user_repository
        self.secret_key = secret_key

    async def execute(self, input_data: LoginInput) -> LoginOutput:
        user = await self.user_repository.find_by_username(input_data.username)
        if not user:
            raise InvalidCredentialsException()

        password_hash = hashlib.sha256(input_data.password.encode()).hexdigest()
        if user.password_hash != password_hash:
            raise InvalidCredentialsException()

        expires_in = 3600
        payload = {
            'user_id': bytes_to_uuid_str(user.id),
            'username': user.username,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=expires_in)
        }

        access_token = jwt.encode(payload, self.secret_key, algorithm='HS256')

        return LoginOutput(
            user_id=bytes_to_uuid_str(user.id),
            username=user.username,
            email=user.email,
            access_token=access_token,
            expires_in=expires_in
        )