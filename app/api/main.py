import asyncio
import logging

import quart_schema
from quart import Quart, request
from quart_schema import QuartSchema
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from hypercorn.config import Config
from hypercorn.asyncio import serve

from domain.model.base import Base

from logic.config import get_config
from logic.container import container
from logic.dto.input.quiz import SubmitAnswerInput
from logic.dto.output.quiz import QuestionOutput, SubmitAnswerOutput
from logic.dto.output.ranking import RankingOutput
from logic.dto.output.user import LoginOutput, UserScoreOutput, UserOutput

from logic.dto.input.user import CreateUserInput, LoginInput
from logic.middlewares.jwt_required import jwt_required
from logic.middlewares.optional_jwt import optional_jwt

from logic.error_handlers import register_error_handlers

logging.basicConfig(level=logging.ERROR)
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('hypercorn.error').setLevel(logging.ERROR)
logging.getLogger('hypercorn.access').setLevel(logging.ERROR)


def create_app():
    app = Quart(__name__)

    QuartSchema(
        app,
        info={
            "title": "Quiz Management System API",
            "version": "1.0.0",
            "description": "API for Quiz Management System",
            "contact": {
                "name": "Quiz API Support",
                "email": "support@quizapi.com"
            }
        },
        tags=[
            {"name": "Authentication", "description": "User authentication and registration"},
            {"name": "Quiz", "description": "Quiz questions and answer submission"},
            {"name": "User", "description": "User profile and score management"},
            {"name": "Ranking", "description": "User rankings and leaderboards"},
            {"name": "Health", "description": "API health check endpoints"}
        ],
        security=[{"bearerAuth": []}],
        security_schemes={
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearer_format": "JWT",
            }
        },
    )

    config = get_config()
    app.config.update(config.__dict__)

    engine = create_async_engine(
        config.DATABASE_URL(),
        future=True
    )

    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    app.db_engine = engine
    app.async_session = async_session

    register_error_handlers(app)

    @app.route('/api/auth/register', methods=['POST'])
    @quart_schema.tag(["Authentication"])
    @quart_schema.validate_request(CreateUserInput)
    @quart_schema.validate_response(UserOutput, 201)
    async def register(data: CreateUserInput):
        async with app.async_session() as session:
            usecase = container.get_create_user_usecase(session)
            result = await usecase.execute(data)
            return result, 201

    @app.route('/api/auth/login', methods=['POST'])
    @quart_schema.tag(["Authentication"])
    @quart_schema.validate_request(LoginInput)
    @quart_schema.validate_response(LoginOutput, 200)
    async def login(data: LoginInput):
        async with app.async_session() as session:
            usecase = container.get_login_usecase(session)
            result = await usecase.execute(data)
            return result, 200

    @app.route('/api/questions/random', methods=['GET'])
    @quart_schema.tag(["Quiz"])
    @quart_schema.security_scheme([])
    @quart_schema.validate_response(QuestionOutput, 200)
    @jwt_required
    async def get_random_question():
        async with app.async_session() as session:
            usecase = container.get_random_question_usecase(session)
            result = await usecase.execute()
            return result, 200

    @app.route('/api/quiz/answer/<uuid:question_id>/<uuid:answer_id>', methods=['POST'])
    @quart_schema.tag(["Quiz"])
    @quart_schema.validate_response(SubmitAnswerOutput, 200)
    @jwt_required
    async def submit_answer(question_id: str, answer_id: str):
        async with app.async_session() as session:
            usecase = container.get_submit_answer_usecase(session)
            data = SubmitAnswerInput(question_id=question_id, answer_id=answer_id)
            result = await usecase.execute(request.current_user_id, data)
            return result, 200

    @app.route('/api/score', methods=['GET'])
    @quart_schema.tag(["User"])
    @quart_schema.validate_response(UserScoreOutput, 200)
    @jwt_required
    async def get_user_score():
        async with app.async_session() as session:
            usecase = container.get_user_score_usecase(session)
            result = await usecase.execute(request.current_user_id)
            return result, 200

    @app.route('/api/ranking', methods=['GET'])
    @quart_schema.tag(["Ranking"])
    @quart_schema.validate_response(RankingOutput, 200)
    @optional_jwt
    async def get_ranking():
        async with app.async_session() as session:
            usecase = container.get_ranking_usecase(session)
            result = await usecase.execute()
            return result, 200

    @app.route('/health', methods=['GET'])
    @quart_schema.tag(["Health"])
    async def health_check():
        return {"status": "healthy", "service": "quiz-api"}, 200

    @app.before_serving
    async def setup_database():
        async with app.db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return app


def main():
    app = create_app()

    config = Config()
    config.bind = ["0.0.0.0:8000"]
    config.debug = False
    config.access_log_format = ""
    config.errorlog = None

    print("Quiz API server starting on http://0.0.0.0:8000")
    print("API Documentation available at: http://0.0.0.0:8000/docs")
    asyncio.run(serve(app, config))


if __name__ == "__main__":
    main()