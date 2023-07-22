import requests
import csv

url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON'
response = requests.get(url)
if response.status_code == 200:
    print("下載成功")
    weather = response.json()

location = weather['cwbopendata']['dataset']['location']
weather_list = []
for item in location:
    city_item={}
    city_item['城市']=item['locationName']
    city_item['開始時間']=item['weatherElement'][1]['time'][0]['startTime']
    city_item['結束時間']=item['weatherElement'][1]['time'][0]['endTime']
    city_item['最高溫度']=float(item['weatherElement'][1]['time'][0]['parameter']['parameterName'])
    city_item['最低溫度']=float(item['weatherElement'][2]['time'][0]['parameter']['parameterName'])
    city_item['感覺']=item['weatherElement'][3]['time'][0]['parameter']['parameterName']
    weather_list.append(city_item)

with open('目前天氣.csv', mode='w', encoding='utf-8', newline='') as file:
    fieldnames = ['城市','開始時間', '結束時間','最高溫度','最低溫度', '感覺' ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(weather_list)