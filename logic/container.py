from sqlalchemy.ext.asyncio import AsyncSession

from domain.repository.user_repository import UserRepositoryImpl
from domain.repository.question_repository import QuestionRepositoryImpl
from domain.repository.answer_repository import AnswerRepositoryImpl
from domain.repository.user_score_repository import UserScoreRepositoryImpl
from domain.repository.user_answer_repository import UserAnswerRepositoryImpl


from logic.config import get_config
from logic.usecase.create_user import CreateUserUseCase
from logic.usecase.get_random_question import GetRandomQuestionUseCase
from logic.usecase.get_ranking import GetRankingUseCase
from logic.usecase.get_user_score import GetUserScoreUseCase
from logic.usecase.login import LoginUseCase
from logic.usecase.submit_answer import SubmitAnswerUseCase


class Container:
    def __init__(self):
        self.config = get_config()
        self._repositories = {}
        self._use_cases = {}

    @staticmethod
    def get_user_repository(session: AsyncSession) -> UserRepositoryImpl:
        return UserRepositoryImpl(session)

    @staticmethod
    def get_question_repository(session: AsyncSession) -> QuestionRepositoryImpl:
        return QuestionRepositoryImpl(session)

    @staticmethod
    def get_answer_repository(session: AsyncSession) -> AnswerRepositoryImpl:
        return AnswerRepositoryImpl(session)

    @staticmethod
    def get_user_score_repository(session: AsyncSession) -> UserScoreRepositoryImpl:
        return UserScoreRepositoryImpl(session)

    @staticmethod
    def get_user_answer_repository(session: AsyncSession) -> UserAnswerRepositoryImpl:
        return UserAnswerRepositoryImpl(session)

    def get_create_user_usecase(self, session: AsyncSession) -> CreateUserUseCase:
        user_repo = self.get_user_repository(session)
        return CreateUserUseCase(user_repo)

    def get_login_usecase(self, session: AsyncSession) -> LoginUseCase:
        user_repo = self.get_user_repository(session)
        return LoginUseCase(user_repo, self.config.SECRET_KEY)

    def get_random_question_usecase(self, session: AsyncSession) -> GetRandomQuestionUseCase:
        question_repo = self.get_question_repository(session)
        answer_repo = self.get_answer_repository(session)
        user_answer_repo = self.get_user_answer_repository(session)
        return GetRandomQuestionUseCase(question_repo, answer_repo, user_answer_repo)

    def get_user_score_usecase(self, session: AsyncSession) -> GetUserScoreUseCase:
        user_score_repo = self.get_user_score_repository(session)
        return GetUserScoreUseCase(user_score_repo)

    def get_ranking_usecase(self, session: AsyncSession) -> GetRankingUseCase:
        user_score_repo = self.get_user_score_repository(session)
        user_repo = self.get_user_repository(session)
        return GetRankingUseCase(user_score_repo, user_repo)

    def get_submit_answer_usecase(self, session: AsyncSession) -> SubmitAnswerUseCase:
        user_answer_repo = self.get_user_answer_repository(session)
        user_score_repo = self.get_user_score_repository(session)
        question_repo = self.get_question_repository(session)
        answer_repo = self.get_answer_repository(session)
        return SubmitAnswerUseCase(user_answer_repo, user_score_repo, question_repo, answer_repo)

container = Container()