import requests, os, json
from dotenv import load_dotenv


load_dotenv()
BASE_KEY = os.getenv('BASE_KEY')
API_KEY = os.getenv('API_KEY')

history = [
        {
            "role": "system",
            "text": "Ты помощник учителя. Ты должен вопросы в формате json на любую тему. Пример вопроса в json: \"{\"text\" : \"текст вопроса\", \"answers\" : [{\"text\" : \"текст ответа 1\", \"correct\" : true}, {\"text\" : \"текст ответа 2\", \"correct\" : false}]}\". В правильном ответе \"correct\" должен быть true, а в неправильном false. Максимум ответов - 4. Правильных ответов может быть несколько, но должен быть хотя бы один. Писать что-то помимо самого json не нужно. Пожалуйста, используй только \" в качестве кавычек, '«' использовать нельзя и не повторяй ответы. Нецелые числа разделяй с помощью точки. Это очень важно!"
        },
        {
            "role": "user",
            "text": "Придумай вопрос с 4 ответами по математике за 6 класс"
        },
        {
            "role": "assistant",
            "text": "\"{\"text\" : \"Укажите лишнюю пару слов\", \"answers\" : [{\"text\" : \"картина - рисовать\", \"correct\" : true}, {\"text\" : \"продавец - продавать\", \"correct\" : false}, {\"text\" : \"врач - лечить\", \"correct\" : false}, {\"text\" : \"учитель - учить\", \"correct\" : false}]}\""
        }
    ]


def clear_history():
    global history
    history = [
        {
            "role": "system",
            "text": "Ты помощник учителя. Ты должен вопросы в формате json на любую тему. Пример вопроса в json: \"{\"text\" : \"текст вопроса\", \"answers\" : [{\"text\" : \"текст ответа 1\", \"correct\" : true}, {\"text\" : \"текст ответа 2\", \"correct\" : false}]}\". В правильном ответе \"correct\" должен быть true, а в неправильном false. Максимум ответов - 4. Правильных ответов может быть несколько, но должен быть хотя бы один. Писать что-то помимо самого json не нужно. Пожалуйста, используй только \" в качестве кавычек, '«' использовать нельзя и не повторяй ответы. Нецелые числа разделяй с помощью точки. Это очень важно!"
        },
        {
            "role": "user",
            "text": "Придумай вопрос с 4 ответами по математике за 6 класс"
        },
        {
            "role": "assistant",
            "text": "\"{\"text\" : \"Укажите лишнюю пару слов\", \"answers\" : [{\"text\" : \"картина - рисовать\", \"correct\" : true}, {\"text\" : \"продавец - продавать\", \"correct\" : false}, {\"text\" : \"врач - лечить\", \"correct\" : false}, {\"text\" : \"учитель - учить\", \"correct\" : false}]}\""
        }
    ]

def get_question(theme, ans_count):
    global history
    history.append({
        "role": "user",
        "text": f"Придумай вопрос с {ans_count} ответами по теме \"{theme}\""
    })
    prompt = {
        "modelUri": f"gpt://{BASE_KEY}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.9,
            "maxTokens": "2000"
        },
        "messages": history
    }


    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = json.loads(response.text).get("result").get("alternatives")[0].get("message").get("text")
    history.append({
        "role" : "assistant",
        "text" : result
    })
    return result


if __name__ == "__main__":
    print(get_question("информатика 8 класс", 4))