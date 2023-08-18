# 載入 selenium 相關模組
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
from datetime import datetime
import pytz

def get_cur_date()->str:
    '''
    - 取得台灣目前year-month-day
    '''
    taiwan_timezone = pytz.timezone('Asia/Taipei')
    current_date = datetime.now(taiwan_timezone)    
    date = f"{current_date.year}-{current_date.month}-{current_date.day}"
    return date

def create_chrome_driver():
    options = Options()
    options.chrome_executable_path=".\chromedriver.exe"
    # 建立 driver 物件實體
    driver=webdriver.Chrome(options=options)
    return driver

def close_chrome_driver(dr:webdriver):
    dr.close()
    return

def connect_login_page(dr:webdriver):
    dr.get("http://www.cnyiot.com/MLogin.aspx")
    username_input = dr.find_element(By.ID, "username")
    password_input = dr.find_element(By.ID, "password")
    username_input.send_keys("00011049")
    password_input.send_keys("14725818")
    btn_singin = dr.find_element(By.ID, "subBt")
    btn_singin.send_keys(Keys.ENTER)
    return

def connect_cur_meter_page(dr:webdriver):
    dr.get("http://www.cnyiot.com/MMpublicw.aspx")
    return

def get_cur_meter_status(dr:webdriver)->list:
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
    print(data)
    return data

def save_cur_meter_status_csv(data:list)->None:
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

def get_meter_history(dr:webdriver)->list:
    meter_element = dr.find_element(By.ID, "table1")
    # print(meter_element.text)
    meter_element_list = meter_element.text.splitlines()
    meter_element_list = meter_element_list[7:]
    data = []
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
        print(meter_item)
        data.append(meter_item)
        # total_usage += float(meter_item['使用水量'])
    print(data)
    return data

def save_meter_history_csv(meter:str, data:list)->None:
    date = get_cur_date()
    filename = f"{date}-{meter}.csv"
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['開始日期','開始時間', '結束日期','結束時間','開始總水量', '結束總水量', '使用水量']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return

def main():
    driver = create_chrome_driver()
    connect_login_page(driver)
    time.sleep(5)

    connect_cur_meter_page(driver)
    time.sleep(5)
    data = get_cur_meter_status(driver)
    save_cur_meter_status_csv(data)

    meter = "50300036790"
    connect_meter_history_page(meter, driver)
    time.sleep(5)
    data = get_meter_history(driver)
    time.sleep(5)
    save_meter_history_csv(meter, data)

    close_chrome_driver(driver)

if __name__ == "__main__":
    main()