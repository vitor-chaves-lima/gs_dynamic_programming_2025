class QuizAPIException(Exception):
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class UserException(QuizAPIException):
    pass


class UserAlreadyExistsException(UserException):
    def __init__(self, username: str):
        super().__init__(f"Username '{username}' already exists", "USER_ALREADY_EXISTS")


class InvalidCredentialsException(UserException):
    def __init__(self):
        super().__init__("Invalid username or password", "INVALID_CREDENTIALS")


class PasswordValidationException(UserException):
    pass


class PasswordTooShortException(PasswordValidationException):
    def __init__(self, min_length: int = 6):
        super().__init__(f"Password must be at least {min_length} characters", "PASSWORD_TOO_SHORT")


class PasswordConfirmationMismatchException(PasswordValidationException):
    def __init__(self):
        super().__init__("Password confirmation does not match", "PASSWORD_CONFIRMATION_MISMATCH")


class QuizException(QuizAPIException):
    pass


class QuestionNotFoundException(QuizException):
    def __init__(self, question_id: str):
        super().__init__(f"Question with ID '{question_id}' not found", "QUESTION_NOT_FOUND")


class AnswerNotFoundException(QuizException):
    def __init__(self, answer_id: str):
        super().__init__(f"Answer with ID '{answer_id}' not found", "ANSWER_NOT_FOUND")


class NoQuestionsAvailableException(QuizException):
    def __init__(self):
        super().__init__("No questions available", "NO_QUESTIONS_AVAILABLE")


class NoCorrectAnswerException(QuizException):
    def __init__(self, question_id: str):
        super().__init__(f"No correct answer found for question '{question_id}'", "NO_CORRECT_ANSWER")


class RepositoryException(QuizAPIException):
    pass


class EntityNotFoundException(RepositoryException):
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"{entity_type} with ID '{entity_id}' not found", "ENTITY_NOT_FOUND")


class AuthenticationException(QuizAPIException):
    pass


class InvalidTokenException(AuthenticationException):
    def __init__(self):
        super().__init__("Invalid or expired token", "INVALID_TOKEN")


class MissingTokenException(AuthenticationException):
    def __init__(self):
        super().__init__("Authentication token is required", "MISSING_TOKEN")


class ValidationException(QuizAPIException):
    pass


class InvalidInputException(ValidationException):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Invalid input for field '{field}': {reason}", "INVALID_INPUT")