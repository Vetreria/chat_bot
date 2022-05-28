from asyncio import exceptions
from msilib.schema import Error
import random
import logging
import os
import dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from logger import set_logger
from dialogflow import detect_intent_texts


logger = logging.getLogger(__file__)


def send_answer(event, vk_api, project_id):
    answer = detect_intent_texts(
        project_id, event.user_id, event.text)
    if answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
    else:
        logger.warning('Нет ответа на вопрос')


def start_bot(vk_token, project_id):
    try:
        logger.warning('Бот запустился')
        vk_session = vk.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_answer(event, vk_api, project_id)
    except BaseException:
        logger.exception('Бот ВК упал с ошибкой')


def main() -> None:
    dotenv.load_dotenv()
    chat_id = os.environ["SUP_CHAT_TG"]
    sup_tg_token = os.environ["SUP_BOT_TG"]
    set_logger(logger, sup_tg_token, chat_id)
    vk_token = os.getenv("VK_GROUP_API")
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    start_bot(vk_token, project_id)
    


if __name__ == '__main__':
    main()
