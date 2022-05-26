import os
import json
import dotenv

dotenv.load_dotenv()
project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
lerning_intents = os.getenv('LEARNING_INTENTS')
from google.cloud import dialogflow


def get_questions():
    with open(lerning_intents, "r", encoding="utf-8") as lerning_file:
        questions = json.load(lerning_file)
    return questions


def lerning_dialog():
    try:
        questions = get_questions()
    except OSError:
        print('Ошибка открытия файла с вопросами')
        return

    for intent, phrases in questions.items():
        try:
            create_intent(project_id, intent,
                          phrases['questions'], [phrases['answer']])
        except:
            print('Ошибка создания: {}'.format(intent))


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[
            message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print("Intent created: {}".format(response))


def main() -> None:
    lerning_dialog()


if __name__ == '__main__':
    main()
