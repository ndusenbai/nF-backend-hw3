import requests
from bs4 import BeautifulSoup
import time
import json
import os

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent
}
base_url = "https://kolesa.kz/"
car_model = "audi"
last_car_id_file = 'last_car_id.json'


def main(event, context):
    last_car_id = get_last_car_id()

    for page in range(1, 5):
        if page == 1:
            req = requests.get(f"{base_url}cars/{car_model}/", headers=headers)
        else:
            req = requests.get(f"{base_url}cars/{car_model}/?page={page}", headers=headers)

        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        cars = soup.find_all('div', class_='a-card')

        if searcher_new_post(cars, last_car_id):
            break


def get_last_car_id():
    if os.path.exists(last_car_id_file):
        with open(last_car_id_file, 'r') as file:
            data = json.load(file)
            return data.get('last_car_id', None)
    return None


def set_last_car_id(last_car_id):
    with open(last_car_id_file, 'w') as file:
        json.dump({'last_car_id': last_car_id}, file)


def searcher_new_post(cars, last_id) -> bool:
    for car in cars:
        item_id = car['data-id']

        if item_id == last_id:
            return True

        set_last_car_id(item_id)

    return False


if __name__ == '__main__':
    main('event', 'context')
