import random
import dotenv
import os
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


def detect_intent_texts(project_id, session_id, text, language_code):
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


def answer_sender(event, vk_api, project_id):
    answer = detect_intent_texts(project_id, event.user_id, event.text, language_code = 'ru-RU')
    if answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message= answer,
            random_id=random.randint(1,1000)
        )


def start_bot(vk_token, project_id):
    vk_session = vk.VkApi(token = vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_sender(event, vk_api, project_id)


def main() -> None:
    dotenv.load_dotenv()
    vk_token = os.getenv("VK_GROUP_API")
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    start_bot(vk_token, project_id)
    

if __name__ == '__main__':
    main()