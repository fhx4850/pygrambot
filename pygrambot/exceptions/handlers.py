from .base import BotBaseException


class UpdateError(BotBaseException):
    def __init__(self):
        super().__init__('Error getting update. Status "ok": false.')