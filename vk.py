from cgitb import text
import logging
from turtle import update
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
    
    print(response.query_result.fulfillment_text)

def start_bot(vk_token, project_id):
    vk_session = vk.VkApi(token = vk_token)
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
                detect_intent_texts(project_id, event.user_id, event.text, language_code = 'ru-RU')
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


def main() -> None:
    dotenv.load_dotenv()
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    vk_token = os.getenv("VK_GROUP_API")
    start_bot(vk_token, project_id)
    
    

if __name__ == '__main__':
    main()