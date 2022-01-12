import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = 'https://auto.ria.com/uk/legkovie/'
params = {'page': 1}
# set a number greater than the number of the first page to start the cycle
pages = 2
n = 0

itemsBrand = []
itemsModel = []
itemsPrice = []
itemsYear = []
itemsRegion = []
itemsTransmission = []
itemsFuel = []
itemsEngineCapacity = []
itemsMileage = []
itemsLink = []


to_json = []

while params['page'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('section', class_='ticket-item')
    # print(items)

    for n, i in enumerate(items, start=n+1):
        itemBrand = i.find('span', class_='blue bold').text.split()[0]
        itemsBrand.append(itemBrand)
        itemModel = ' '.join(i.find('span', class_='blue bold').text.split()[1::])
        itemsModel.append(itemModel)
        itemPrice = i.find('span', class_='bold green size22').text.strip()
        itemsPrice.append(itemPrice)
        itemYear = i.find('a', class_='address').text.split()[-1]
        itemsYear.append(itemYear)
        itemRegion = i.find('li', class_='item-char view-location js-location').text.strip().split(' (')[0]
        itemsRegion.append(itemRegion)
        itemTransmission = i.find_all('li', class_='item-char')[3].text.replace(' ', '')
        itemsTransmission.append(itemTransmission)
        itemFuel = i.find_all('li', class_='item-char')[2].text.split(',')[0]
        itemsFuel.append(itemFuel)
        itemEngineCapacity = i.find_all('li', class_='item-char')[2].text.split(',')[-1]
        itemsEngineCapacity.append(itemEngineCapacity)
        itemMileage = i.find('li', class_='item-char js-race').text
        itemsMileage.append(itemMileage)
        itemLink = i.find('a', class_='m-link-ticket').get('href')
        itemsLink.append(itemLink)

        print(f'{n}: {itemBrand},\n     Model: {itemModel},\n     Price: {itemPrice} $,\n     Year: {itemYear},\n     '
              f'Region: {itemRegion},\n     Transmission: {itemTransmission},\n     Fuel type: {itemFuel},\n     '
              f'Engine capacity: {itemEngineCapacity},\n     Mileage: {itemMileage}')
        item_to_json = {
            'Brand': itemBrand,
            'Model': itemModel,
            'Price': itemPrice,
            'Year': itemYear,
            'Region': itemRegion,
            'Transmission': itemTransmission,
            'Fuel type': itemFuel,
            'Engine capacity': itemEngineCapacity,
            'Mileage': itemMileage,
            'Link': itemLink
        }
        to_json.append(item_to_json)

    # last_page_num = int(soup.find('a', class_='page-link js-next').get('data-page'))
    # print(last_page_num)
    last_page_num = 200
    pages = last_page_num if pages < last_page_num else pages
    params['page'] += 1
# print(len(itemsBrand), len(itemsModel), len(itemsPrice), len(itemsYear), len(itemsRegion), len(itemsTransmission),
#       len(itemsFuel), len(itemsEngineCapacity), len(itemsMileage))
df = pd.DataFrame({
    'Brand': itemsBrand,
    'Model': itemsModel,
    'Price': itemsPrice,
    'Year': itemsYear,
    'Region': itemsRegion,
    'Transmission': itemsTransmission,
    'Fuel type': itemsFuel,
    'Engine capacity': itemsEngineCapacity,
    'Mileage': itemsMileage,
    'Link': itemsLink
})
df.to_csv('autos.csv', index=False)

with open('autos.json', 'w') as f:
    f.write(json.dumps(to_json, indent=4))