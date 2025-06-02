from domain.model.user_answer import UserAnswer
from domain.model.user_score import UserScore
from domain.repository.answer_repository import AnswerRepositoryImpl
from domain.repository.question_repository import QuestionRepositoryImpl
from domain.repository.user_answer_repository import UserAnswerRepositoryImpl
from domain.repository.user_score_repository import UserScoreRepositoryImpl
from domain.utils.uuid import uuid_to_bytes, bytes_to_uuid_str
from logic.dto.input.quiz import SubmitAnswerInput
from logic.dto.output.quiz import SubmitAnswerOutput
from logic.exceptions import (
    QuestionNotFoundException,
    AnswerNotFoundException,
    NoCorrectAnswerException
)


class SubmitAnswerUseCase:
    def __init__(self, user_answer_repository: UserAnswerRepositoryImpl, user_score_repository: UserScoreRepositoryImpl,
                 question_repository: QuestionRepositoryImpl, answer_repository: AnswerRepositoryImpl):
        self.user_answer_repository = user_answer_repository
        self.user_score_repository = user_score_repository
        self.question_repository = question_repository
        self.answer_repository = answer_repository

    async def execute(self, user_id: str, input_data: SubmitAnswerInput) -> SubmitAnswerOutput:
        question = await self.question_repository.find_by_id(input_data.question_id)
        if not question:
            raise QuestionNotFoundException(input_data.question_id)

        selected_answer = await self.answer_repository.find_by_id(input_data.answer_id)
        if not selected_answer:
            raise AnswerNotFoundException(input_data.answer_id)

        all_answers = await self.answer_repository.find_by_question_id(input_data.question_id)
        correct_answer = next((ans for ans in all_answers if ans.is_correct), None)

        if not correct_answer:
            raise NoCorrectAnswerException(input_data.question_id)

        is_correct = selected_answer.is_correct
        points_earned = question.points if is_correct else 0

        user_answer = UserAnswer(
            user_id=uuid_to_bytes(user_id),
            question_id=uuid_to_bytes(input_data.question_id),
            answer_id=uuid_to_bytes(input_data.answer_id),
            is_correct=is_correct,
            points_earned=points_earned,
        )

        await self.user_answer_repository.save(user_answer)

        user_score = await self.user_score_repository.find_by_user_id(user_id)

        if not user_score:
            user_score = UserScore(
                user_id=uuid_to_bytes(user_id),
                total_score=0,
                total_questions=0,
                correct_answers=0
            )

        user_score.total_score += points_earned
        user_score.total_questions += 1
        if is_correct:
            user_score.correct_answers += 1

        await self.user_score_repository.save(user_score)

        return SubmitAnswerOutput(
            is_correct=is_correct,
            points_earned=points_earned,
            correct_answer_id=bytes_to_uuid_str(correct_answer.id),
            explanation=f"A resposta correta é: {correct_answer.text}",
            current_score=user_score.total_score,
        )