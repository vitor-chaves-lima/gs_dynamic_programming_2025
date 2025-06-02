import logging
from typing import Tuple

from quart import Quart
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from logic.exceptions import (
    QuizAPIException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    PasswordTooShortException,
    PasswordConfirmationMismatchException,
    QuestionNotFoundException,
    AnswerNotFoundException,
    NoQuestionsAvailableException,
    NoCorrectAnswerException,
    InvalidTokenException,
    MissingTokenException,
    ValidationException,
    InvalidInputException,
    RepositoryException,
    EntityNotFoundException
)

logger = logging.getLogger(__name__)


def register_error_handlers(app: Quart) -> None:
    @app.errorhandler(UserAlreadyExistsException)
    async def handle_user_already_exists(error: UserAlreadyExistsException) -> Tuple[dict, int]:
        logger.warning(f"User already exists: {error.message}")
        return {
            "error": "Conflict",
            "message": error.message,
            "error_code": error.error_code
        }, 409

    @app.errorhandler(InvalidCredentialsException)
    async def handle_invalid_credentials(error: InvalidCredentialsException) -> Tuple[dict, int]:
        logger.warning(f"Invalid credentials: {error.message}")
        return {
            "error": "Unauthorized",
            "message": error.message,
            "error_code": error.error_code
        }, 401

    @app.errorhandler(PasswordTooShortException)
    async def handle_password_too_short(error: PasswordTooShortException) -> Tuple[dict, int]:
        logger.warning(f"Password validation failed: {error.message}")
        return {
            "error": "Bad Request",
            "message": error.message,
            "error_code": error.error_code
        }, 400

    @app.errorhandler(PasswordConfirmationMismatchException)
    async def handle_password_confirmation_mismatch(error: PasswordConfirmationMismatchException) -> Tuple[dict, int]:
        logger.warning(f"Password confirmation mismatch: {error.message}")
        return {
            "error": "Bad Request",
            "message": error.message,
            "error_code": error.error_code
        }, 400

    @app.errorhandler(QuestionNotFoundException)
    async def handle_question_not_found(error: QuestionNotFoundException) -> Tuple[dict, int]:
        logger.warning(f"Question not found: {error.message}")
        return {
            "error": "Not Found",
            "message": error.message,
            "error_code": error.error_code
        }, 404

    @app.errorhandler(AnswerNotFoundException)
    async def handle_answer_not_found(error: AnswerNotFoundException) -> Tuple[dict, int]:
        logger.warning(f"Answer not found: {error.message}")
        return {
            "error": "Not Found",
            "message": error.message,
            "error_code": error.error_code
        }, 404

    @app.errorhandler(NoQuestionsAvailableException)
    async def handle_no_questions_available(error: NoQuestionsAvailableException) -> Tuple[dict, int]:
        logger.warning(f"No questions available: {error.message}")
        return {
            "error": "Not Found",
            "message": error.message,
            "error_code": error.error_code
        }, 404

    @app.errorhandler(NoCorrectAnswerException)
    async def handle_no_correct_answer(error: NoCorrectAnswerException) -> Tuple[dict, int]:
        logger.error(f"Data integrity issue - no correct answer: {error.message}")
        return {
            "error": "Internal Server Error",
            "message": "Question data is inconsistent. Please contact support.",
            "error_code": error.error_code
        }, 500

    @app.errorhandler(InvalidTokenException)
    async def handle_invalid_token(error: InvalidTokenException) -> Tuple[dict, int]:
        logger.warning(f"Invalid token: {error.message}")
        return {
            "error": "Unauthorized",
            "message": error.message,
            "error_code": error.error_code
        }, 401

    @app.errorhandler(MissingTokenException)
    async def handle_missing_token(error: MissingTokenException) -> Tuple[dict, int]:
        logger.warning(f"Missing token: {error.message}")
        return {
            "error": "Unauthorized",
            "message": error.message,
            "error_code": error.error_code
        }, 401

    @app.errorhandler(InvalidInputException)
    async def handle_invalid_input(error: InvalidInputException) -> Tuple[dict, int]:
        logger.warning(f"Invalid input: {error.message}")
        return {
            "error": "Bad Request",
            "message": error.message,
            "error_code": error.error_code
        }, 400

    @app.errorhandler(ValidationException)
    async def handle_validation_error(error: ValidationException) -> Tuple[dict, int]:
        logger.warning(f"Validation error: {error.message}")
        return {
            "error": "Bad Request",
            "message": error.message,
            "error_code": error.error_code
        }, 400

    @app.errorhandler(EntityNotFoundException)
    async def handle_entity_not_found(error: EntityNotFoundException) -> Tuple[dict, int]:
        logger.warning(f"Entity not found: {error.message}")
        return {
            "error": "Not Found",
            "message": error.message,
            "error_code": error.error_code
        }, 404

    @app.errorhandler(RepositoryException)
    async def handle_repository_error(error: RepositoryException) -> Tuple[dict, int]:
        logger.error(f"Repository error: {error.message}")
        return {
            "error": "Internal Server Error",
            "message": "Database operation failed. Please try again later.",
            "error_code": error.error_code
        }, 500

    @app.errorhandler(QuizAPIException)
    async def handle_quiz_api_exception(error: QuizAPIException) -> Tuple[dict, int]:
        logger.error(f"Quiz API exception: {error.message}")
        return {
            "error": "Internal Server Error",
            "message": error.message,
            "error_code": error.error_code
        }, 500

    @app.errorhandler(IntegrityError)
    async def handle_integrity_error(error: IntegrityError) -> Tuple[dict, int]:
        logger.error(f"Database integrity error: {str(error.orig)}")
        return {
            "error": "Conflict",
            "message": "Data integrity violation. The operation could not be completed.",
            "error_code": "DATABASE_INTEGRITY_ERROR"
        }, 409

    @app.errorhandler(SQLAlchemyError)
    async def handle_sqlalchemy_error(error: SQLAlchemyError) -> Tuple[dict, int]:
        logger.error(f"Database error: {str(error)}")
        return {
            "error": "Internal Server Error",
            "message": "Database operation failed. Please try again later.",
            "error_code": "DATABASE_ERROR"
        }, 500

    @app.errorhandler(Exception)
    async def handle_generic_exception(error: Exception) -> Tuple[dict, int]:
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }, 500
