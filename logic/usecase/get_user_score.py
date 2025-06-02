from logic.dto.output.user import UserScoreOutput


class GetUserScoreUseCase:
    def __init__(self, user_score_repository):
        self.user_score_repository = user_score_repository

    async def execute(self, user_id: str) -> UserScoreOutput:
        user_score = await self.user_score_repository.find_by_user_id(user_id)

        if not user_score:
            return UserScoreOutput(
                total_score=0,
                total_questions=0,
                correct_answers=0,
                accuracy_percentage=0.0,
                last_completed_at=None
            )

        accuracy = (
                    user_score.correct_answers / user_score.total_questions * 100) if user_score.total_questions > 0 else 0

        return UserScoreOutput(
            total_score=user_score.total_score,
            total_questions=user_score.total_questions,
            correct_answers=user_score.correct_answers,
            accuracy_percentage=accuracy,
            last_completed_at=user_score.completed_at.isoformat() if user_score.completed_at else None
        )