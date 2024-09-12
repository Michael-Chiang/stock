import requests
import pandas as pd
# 貼上連結
url = 'https://www.slickcharts.com/sp500'
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

request = requests.get(url, headers = headers)

data = pd.read_html(request.text)[0]

# 欄位『Symbol』就是股票代碼
stk_list = data.Symbol

# 用 replace 將符號進行替換
stk_list = data.Symbol.apply(lambda x: x.replace('.', '-'))

stk_list.to_csv('symbol.csv')
