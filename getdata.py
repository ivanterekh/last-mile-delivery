import herepy
import requests
import json
import csv

#апи ключ для инфы с HERE
geocoderApi = herepy.GeocoderApi('bOZAeO552D42cNgIwLvUz0gVvU-JNWTFI9gmIXDL1qY')

#инфа для получения адресов магазинов, заголовок такой чтобы наебывать сервера и нам возвращали ответ, а на блочили как ботов (на всякий случай)
url = 'https://evroopt.by/wp-content/themes/evroopt/klaster-shop-load.php?magazine=5&city=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA&type_shop='
headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36'
      }
r = requests.get(url, headers = headers)

#парсим json ответа
dd = json.loads(r.text)

#если честно, я хз зачем я пишу всё в файл, если потом все равно читаю из него, но пусть будет
filename = 'shops.csv'
with open(filename, "a", newline="", encoding='utf-8') as file:
    for shop in range(len(dd['info'])):
        towrite = dd['info'][shop]['city']
        writer = csv.writer(file)
        writer.writerow([towrite])

#собственно, чтение
with open('shops.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

all_minsk_shops = data

#иногда апи возвращает несколько вариантов на запрос - выбираем лучший по оценке результата
def find_best_item(rd):
    best_score = 0
    best_item = 0
    for item in range(len(rd['items'])):
        if rd['items'][item]['scoring']['queryScore'] > best_score:
            best_score = rd['items'][item]['scoring']['queryScore']
            best_item = item

    return best_item

#отправка запросов в HERE
full_info = []
for i in range(len(all_minsk_shops)):
    shop = all_minsk_shops[i][0].replace('Минск, ', '')
    response = geocoderApi.street_intersection(shop, 'Minsk city')
    response_dict = response.as_dict()
    best_item = find_best_item(response_dict)
    if response_dict['items'][best_item]['address']['countryCode'] == 'BLR':
        response_dict['items'][best_item]['address'].pop('label')
        d1 = response_dict['items'][best_item]['address']
        d2 = response_dict['items'][best_item]['access'][0]
        shop_info = {**d1, **d2}
        full_info.append(shop_info)

filename = 'full_info.csv'

#запись в файл, на самом деле достаточно странно возвращаются данные (на двух языках), 
#кодировку указывал utf-8 потому что в юпитере у меня были какие-то проблемы с другими
#потом попробую изменить
with open(filename, "a", newline="", encoding='utf-8') as file:
    header = ['countryCode', 'countryName', 'state', 'county', 'city', 'street', 'postalCode', 'houseNumber', 'lat', 'lng']
    writer = csv.DictWriter(file, fieldnames = header)
    writer.writeheader()
    for row in full_info:
        writer.writerow(row)