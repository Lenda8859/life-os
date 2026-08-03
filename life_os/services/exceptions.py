"""Понятные ошибки сервисного слоя."""


class LifeOSError(Exception):
    """Базовая ошибка бизнес-логики Life OS."""


class ValidationError(LifeOSError):
    """Переданные данные не прошли проверку."""


class NotFoundError(LifeOSError):
    """Запрошенная сущность не найдена."""


class ConflictError(LifeOSError):
    """Операция конфликтует с уже существующими данными."""
