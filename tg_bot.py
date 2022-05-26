import logging
import os
import dotenv
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger(__file__)

dotenv.load_dotenv()
chat_id = os.environ["SUP_CHAT_TG"]
sup_tg_token = os.environ["SUP_BOT_TG"]
project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, sup_tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = sup_tg_token
        self.tg_bot.send_message(chat_id=self.chat_id, text='LOG-BOT: started')

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def detect_intent_texts(update: Update, context: CallbackContext, language_code='ru-RU'):
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, update.message.chat_id)
    text_input = dialogflow.TextInput(
        text=update.message.text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)
    logger.warning('Сообщение ушло')


def error_handler(update: Update, context: CallbackContext):
    logger.exception('Telegram-бот упал с ошибкой')


def set_logger(logger):
    logger_bot = telegram.Bot(token=sup_tg_token)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(logger_bot, chat_id))


def main() -> None:
    set_logger(logger)
    logger.warning('Бот запустился')

    tg_token = os.environ["TG_TOKEN"]
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, detect_intent_texts))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
    logger.warning('Бот закрылся')


if __name__ == '__main__':
    main()
