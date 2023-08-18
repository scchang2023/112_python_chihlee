# 載入 selenium 相關模組
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# 時間 delay 模組
import time
# 存成 csv 檔
import csv
# 取得目前時間模組
from datetime import datetime
# 取得時區
import pytz
# 系統路徑
import os

def get_cur_date()->str:
    '''
    - 取得台灣目前year-month-day
    '''
    taiwan_timezone = pytz.timezone('Asia/Taipei')
    current_date = datetime.now(taiwan_timezone)    
    date = f"{current_date.year}-{current_date.month}-{current_date.day}"
    return date

def create_chrome_driver()->webdriver:
    options = Options()
    current_cwd = os.path.abspath(os.getcwd())
    options.chrome_executable_path=f"{current_cwd}\chromedriver_win32.exe"
    # options.chrome_executable_path=f"{current_cwd}/chromedriver_linux64.exe"
    print(options.chrome_executable_path)
    # 建立 driver 物件實體
    driver=webdriver.Chrome(options=options)
    return driver

def close_chrome_driver(dr:webdriver)->None:
    dr.close()
    return

def connect_login_page(dr:webdriver)->None:
    dr.get("http://www.cnyiot.com/MLogin.aspx")
    username_input = dr.find_element(By.ID, "username")
    password_input = dr.find_element(By.ID, "password")
    username_input.send_keys("00011049")
    password_input.send_keys("14725818")
    btn_singin = dr.find_element(By.ID, "subBt")
    btn_singin.send_keys(Keys.ENTER)
    return

def connect_meters_status_page(dr:webdriver)->None:
    dr.get("http://www.cnyiot.com/MMpublicw.aspx")
    return

def get_meters_status(dr:webdriver)->list:
    meter_element = dr.find_element(By.ID, "table1")
    # print(meter_element.text)
    meter_element_list = meter_element.text.splitlines()
    meter_element_list = meter_element_list[9:]
    # print(meter_element_list)
    data = []
    for i in meter_element_list:
        meter_item={}
        i = i.replace("在线 （通水 )","在线(通水)")
        i = i.split(' ')
        meter_item['水錶名稱'] = i[0]
        meter_item['水錶號碼'] = i[1]
        meter_item['總水量'] = i[5]
        meter_item['狀態'] = i[6]
        meter_item['供電方式'] = i[7]
        # print(meter_item)
        data.append(meter_item)
    # print(data)
    return data

def save_meters_status_csv(data:list)->None:
    date = get_cur_date()
    filename = f"{date}-目前水錶使用狀態.csv"    
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['水錶名稱','水錶號碼', '總水量','狀態','供電方式']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)    
    return

def connect_meter_history_page(meter:str, dr:webdriver)->None:
    url = f"http://www.cnyiot.com/MMpublicHis.aspx?ID={meter}"
    # print(url)
    dr.get(url)
    return

def get_meter_history(dr:webdriver)->(list, float):
    meter_element = dr.find_element(By.ID, "table1")
    # print(meter_element.text)
    meter_element_list = meter_element.text.splitlines()
    meter_element_list = meter_element_list[7:]
    data = []
    total_usage = 0
    for i in meter_element_list:
        meter_item={}
        i = i.replace("查看详情","")
        i = i.split(' ')
        meter_item['開始日期'] = i[1]
        meter_item['開始時間'] = i[2]
        meter_item['結束日期'] = i[3]
        meter_item['結束時間'] = i[4]
        meter_item['開始總水量'] = i[5]
        meter_item['結束總水量'] = i[6]
        meter_item['使用水量'] = i[8]
        total_usage += float(meter_item['使用水量'])
        data.append(meter_item)
    # print(data, total_usage)
    return (data, total_usage)

def save_meter_history_csv(meter:str, data:list, usage:float)->None:
    date = get_cur_date()
    filename = f"{date}-{meter}.csv"
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['開始日期','開始時間', '結束日期','結束時間','開始總水量', '結束總水量', '使用水量']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        file.writelines("全部總使用量為 %.1f" % usage)
    return

def main():
    driver = create_chrome_driver()
    connect_login_page(driver)
    time.sleep(3)
    connect_meters_status_page(driver)
    time.sleep(3)
    meters_status = get_meters_status(driver)
    save_meters_status_csv(meters_status)
    for i in meters_status:
        print(i)
        connect_meter_history_page(i["水錶號碼"], driver)
        time.sleep(3)
        (meter_history, total_usage) = get_meter_history(driver)
        time.sleep(3)
        save_meter_history_csv(i["水錶名稱"], meter_history, total_usage)
    close_chrome_driver(driver)

if __name__ == "__main__":
    main()