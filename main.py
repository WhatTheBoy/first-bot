import requests
import json
import time
import config
from pprint import pprint

def answer_user_bot(data):
    data = {
        'chat_id': config.MY_ID,
        'text': data
    }
    url = config.URL.format(
        token=config.TOKEN,
        method=config.SEND_METH
    )
    response = requests.post(url, data=data)
    print(response)

def parse_weather_data(data):
    for elem in data['weather']:
        weather_state = elem['main']
    temp = round(data['main']['temp'] -273.15 ,2)
    city = data['name']
    msg = f'The weather in {city}: Temp is {temp}, State is {weather_state}'
    return msg

def get_weather(location):
    url = config.WEATHER_URL.format(city=location,
                                    token=config.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    data = json.loads(response.content)


    return parse_weather_data(data)


def get_message(data):
    return data['message']['text']
    print(text)

def save_update_id(update):
    with open(config.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(update['update_id']))
    config.UPDATE_ID =update['update_id']
    return True

def main():
    while True:
        url = config.URL.format(token=config.TOKEN, method=config.UPDATE_METH)
        content = requests.get(url).text

        data = json.loads(content)
        result = data['result'][::-1]

        needed_part = None


        for elem in result:
            if elem['message']['chat']['id'] == config.MY_ID:
                needed_part = elem
                break


        if config.UPDATE_ID != needed_part['update_id']:
            message = get_message(needed_part)
            msg = get_weather(message)
            answer_user_bot(msg)
            save_update_id(needed_part)


        time.sleep(1)


if __name__ == '__main__':
    main()

