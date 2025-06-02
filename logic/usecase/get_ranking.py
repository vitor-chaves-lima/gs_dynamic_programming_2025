from domain.repository.user_repository import UserRepositoryImpl
from domain.repository.user_score_repository import UserScoreRepositoryImpl
from domain.utils.uuid import bytes_to_uuid_str
from logic.dto.output.ranking import RankingOutput, RankingUserOutput


class GetRankingUseCase:
    def __init__(self, user_score_repository: UserScoreRepositoryImpl, user_repository: UserRepositoryImpl):
        self.user_score_repository = user_score_repository
        self.user_repository = user_repository

    async def execute(self) -> RankingOutput:
        all_scores = await self.user_score_repository.find_all()

        user_totals = {}
        for score in all_scores:
            if score.user_id not in user_totals:
                user_totals[score.user_id] = {
                    'total_score': 0,
                    'total_questions': 0,
                    'correct_answers': 0
                }

            user_totals[score.user_id]['total_score'] += score.total_score
            user_totals[score.user_id]['total_questions'] += score.total_questions
            user_totals[score.user_id]['correct_answers'] += score.correct_answers

        sorted_users = sorted(
            user_totals.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )

        ranking_users = []
        for position, (user_id, totals) in enumerate(sorted_users, 1):
            user = await self.user_repository.find_by_id(bytes_to_uuid_str(user_id))
            if user:
                accuracy = (totals['correct_answers'] / totals['total_questions'] * 100) if totals[
                                                                                                'total_questions'] > 0 else 0

                ranking_users.append(RankingUserOutput(
                    position=position,
                    user_id=bytes_to_uuid_str(user_id),
                    username=user.username,
                    total_score=totals['total_score'],
                    total_questions=totals['total_questions'],
                    accuracy_percentage=accuracy
                ))

        return RankingOutput(
            users=ranking_users,
            total_users=len(user_totals)
        )