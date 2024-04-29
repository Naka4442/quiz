# from openai import OpenAI


# API_TOKEN = 'sk-utr8kuqsVUgBqbvw525d4f9aE6984f6eAdD6D62b828eBeCd'
# BASE_URL = 'https://neuroapi.host'
# client = OpenAI(api_key=API_TOKEN,)

# completion = client.chat.completions.create(
#   model="ChatGPT-3.5-Turbo",
#   messages=[
#     {"role": "system", "content": "Ты волшебник, который придумывает загадки детям 6-8 лет"},
#     {"role": "user", "content": "Сочини 3 загадки в формате json"}
#   ]
# )

# print(completion.choices[0].message)

import openai # openai==0.28

openai.api_key = "sk-OdfItJ3AHERxqNhAAdB8914917Dc4d608aD476E9259aBf2e" # Ваш API ключ
openai.api_base = "https://eu.neuroapi.host/v1" # Наш API Endpoint


def main():
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "write a poem about a tree"}],
        stream=True,
    )

    if isinstance(chat_completion, dict):
        # not stream
        print(chat_completion.choices[0].message.content)
    else:
        # stream
        for token in chat_completion:
            content = token["choices"][0]["delta"].get("content")
            if content != None:
                print(content, end="", flush=True)


if __name__ == "__main__":
    main()