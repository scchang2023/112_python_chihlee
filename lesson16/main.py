import csv
import pandas as pd
import streamlit as st
import ffn

def getStockNames() -> pd.Series:
    with open('codeSearch.csv',encoding='utf-8',newline='') as file:
        next(file)
        csv_reader = csv.reader(file)
        stock_codes = {}
        for item in csv_reader:
            key  =  item[2]
            stock_codes[key] = item[3]
        
    code_series:pd.Series = pd.Series(stock_codes)
    return code_series

def displayData(dataFrame:pd.DataFrame,start_year) -> None:
    st.subheader(f'{start_year}~目前的歷史資料')
    st.dataframe(dataFrame)

#多重選取
stockNames:pd.Series = getStockNames()
print(stockNames)
stock_name_id = stockNames.index + "_" + stockNames.values
options = st.sidebar.multiselect('請選擇',
                       stock_name_id,
                       placeholder='股票:')

names:list[str] = []
for name in options:
    name_string = name.split("_")[0]
    names.append(name_string + ".TW")
#print(names)
prices = ffn.get(names, start='2010-01-01')

displayData(prices,start_year='2010-01-01')