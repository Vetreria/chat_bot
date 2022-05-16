import logging
import dotenv
import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


dotenv.load_dotenv()
project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


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


def main() -> None:
    dotenv.load_dotenv()
    tg_token = os.environ["TG_TOKEN"]
    os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, detect_intent_texts))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
