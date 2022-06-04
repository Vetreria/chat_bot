from google.cloud import dialogflow
import logging
logger = logging.getLogger(__file__)


def detect_intent_texts(project_id, session_id, text, skip_fallback):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code='RU-ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if  skip_fallback is False and response.query_result.intent.is_fallback:
        logger.warning('Нет ответа, нужен мешок с костями.')
        return None
    else:
        logger.warning('Сообщение ушло')
        return response.query_result.fulfillment_text