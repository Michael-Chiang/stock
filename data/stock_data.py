import requests
import pandas as pd
import yfinance as yf
import time
# 貼上連結
url = 'https://www.slickcharts.com/sp500'
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

request = requests.get(url, headers = headers)

data = pd.read_html(request.text)[0]

# 欄位『Symbol』就是股票代碼
stk_list = data.Symbol

# 用 replace 將符號進行替換
stk_list = data.Symbol.apply(lambda x: x.replace('.', '-'))


            # 公司資料 #

# 取得個股公司資料的語法，先測試一檔看看
stk_basic_data = yf.Ticker('AAPL').info

# 將 yfinance 有提供的數據項目取出存在 info_columns，它將會成為 stk_info_df 這張總表的欄位項目
info_columns = list(stk_basic_data.keys())

# 創立一個名為 stk_info_df 的總表，用來存放所有股票的基本資料！其中 stk_list 是我們先前抓到的股票代碼喔！
stk_info_df = pd.DataFrame(index = stk_list.sort_values(), columns = info_columns)

# 創立一個紀錄失敗的 list
failed_list_info= []

# 開始迴圈抓資料
for i in stk_info_df.index:
    try:
        # 打印出目前進度
        print(f'processing: {i}')
        # 抓下來的資料暫存成 dictionary
        info_dict = yf.Ticker(i).info
        # 由於 yahoo finance 各檔股票所提供的欄位項目都不一致！所以這邊要針對每一檔股票分別取出欄位項目
        columns_included = list(info_dict.keys())
        # 因為在別檔公司裡有著 AAPL 裡所沒有的會計科目，因此要取兩家公司會計科目的交集
        intersect_columns = [x for x in info_columns if x in columns_included]
        # 有了該股欄位項目後，就可順利填入總表中相對應的位置
        stk_info_df.loc[i,intersect_columns] = list(pd.Series(info_dict)[intersect_columns].values)
        # 停一秒，再抓下一檔，避免對伺服器造成負擔而被鎖住
        time.sleep(1)
    except:
        failed_list_info.append(i)
        continue

stk_info_df.to_csv('infodata.csv')


            # 基本面 #
failed_list_basic = []

for i in stk_list:
    try:
        # 打印出目前進度
        print(f'processing: {i}')
        # 填入股票代碼後直接下載成 csv 格式
        stock = yf.Ticker(i)
        stock.financials.to_csv(f'basicdata/profit_loss_account/profit_loss_account_{i}.csv')
        stock.balance_sheet.to_csv(f'basicdata/balance_sheet/balance_sheet_{i}.csv')
        stock.cashflow.to_csv(f'basicdata/cashflow/cash_flow_{i}.csv')

        time.sleep(1)
    except:
        failed_list_basic.append(i)
        continue


            # 價量資料＋股利發放＋股票分割
failed_list_rowdata= []

for i in stk_list:
    try:
        # 打印出目前進度
        print(f'processing: {i}')
        # 填入股票代碼後直接下載成 csv 格式
        stock = yf.Ticker(i)
        df = stock.history(period = 'max').to_csv(f'rowdata/{i}.csv')
        
        time.sleep(1)
    except:
        failed_list_rowdata.append(i)
        continue
