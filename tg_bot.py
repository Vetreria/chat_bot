import logging
import os
import dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from logger import set_logger
from dialogflow import detect_intent_texts


logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def error_handler(update: Update, context: CallbackContext):
    logger.exception('Telegram-бот упал с ошибкой')


def dialogflow_conversation(update : Update, context : CallbackContext):
    project_id = context.bot_data['project_id']
    context.bot.send_message(chat_id = update.effective_chat.id, text = detect_intent_texts(project_id, update.effective_chat.id, update.message.text, skip_fallback = True))
    

def main() -> None:
    dotenv.load_dotenv()
    chat_id = os.environ["SUP_CHAT_TG"]
    sup_tg_bot = os.environ["SUP_BOT_TG"]
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')

    set_logger(logger, sup_tg_bot, chat_id)
    logger.warning('Бот запустился')

    tg_token = os.environ["TG_TOKEN"]
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['project_id'] = project_id
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, dialogflow_conversation))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
    logger.warning('Бот закрылся')


if __name__ == '__main__':
    main()
