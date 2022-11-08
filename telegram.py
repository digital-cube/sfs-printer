import requests

telegram_token = '5560740641:AAGRm-oyKyIGQYdqw8YNCqy5ZCIjt3XuMhM'

def make_post_request(url: str, json_body: dict):
    r = requests.post(url=url, data=json_body)
    return r.json(), r.status_code


def send_message(msg: str): #request: dict):
    request = \
        {
            "chat_id": 1036660676,
            "text": msg
        }

    if telegram_token is None:
        raise ValueError(
            f'or TELEGRAM_TOKEN({telegram_token}) '
            'were not supplied.'
        )

    telegram_url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'

    response, status_code = make_post_request(
        url=telegram_url,
        json_body=request
    )
    return response, status_code
    
#send_message('5560740641:AAGRm-oyKyIGQYdqw8YNCqy5ZCIjt3XuMhM', {'chat_id': 1036660676, 'text': 'Hi'})