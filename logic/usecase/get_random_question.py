import random

from domain.utils.uuid import bytes_to_uuid_str
from logic.dto.output.quiz import QuestionOutput, AnswerOutput
from logic.exceptions import NoQuestionsAvailableException


class GetRandomQuestionUseCase:
    def __init__(self, question_repository, answer_repository, user_answer_repository):
        self.question_repository = question_repository
        self.answer_repository = answer_repository
        self.user_answer_repository = user_answer_repository

    async def execute(self) -> QuestionOutput:
        questions = await self.question_repository.find_all_active()

        if not questions:
            raise NoQuestionsAvailableException()

        question = random.choice(questions)

        answers = await self.answer_repository.find_by_question_id(question.id)

        random.shuffle(answers)

        answer_outputs = [
            AnswerOutput(
                id=bytes_to_uuid_str(answer.id),
                text=answer.text,
                order_position=i
            ) for i, answer in enumerate(answers)
        ]

        return QuestionOutput(
            id=bytes_to_uuid_str(question.id),
            title=question.title,
            description=question.description,
            points=question.points,
            difficulty_level=question.difficulty_level,
            category=question.category,
            answers=answer_outputs,
        )
