import logging
# import os
import telegram


logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, sup_tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = sup_tg_token
        self.tg_bot.send_message(chat_id=self.chat_id, text='LOG-BOT: started')

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def set_logger(logger, sup_tg_token, chat_id):
    logger_bot = telegram.Bot(token=sup_tg_token)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(logger_bot, chat_id))