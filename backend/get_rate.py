import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
from random import randint
import pickle
from datetime import datetime

def get_rate_from_aia(year='2025', month='9'):
    print("開始解析友邦網站")
    # 友邦
    headers = {
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Content-Type': 'application/json;charset=utf-8',  # 如果是 JSON 数据
        # 'Authorization': '{}',  # 如果需要认证
        # 根据 Postman 中的设置，复制所有相关的头部
    }
    # r = requests.get('https://www.aia.com.tw/libs/granite/csrf/token.json', headers=headers)
    # time.sleep(0.5)
    url = 'https://www.aia.com.tw/zh-tw/api.CreditRate'
    all_aia = []
    for page in range(1, 6):
        # print(page)
        payload = {
            'product_code':'',
            'year':year,
            'month':month,
            'pageindex':page
        }
        # 发送 POST 请求，提交表单数据
        session = requests.session()
        response = session.post(url,params=payload, headers=headers)
        time.sleep(1)
        all_aia.extend(response.json()['datas'])
    return all_aia
    print("解析友邦網站成功")
    
def get_rate_from_yuanta():
    print("開始解析元大網站")
    # 元大
    url = 'https://www.yuantalife.com.tw/api/api/interest-rate'
    session = requests.session()
    response = session.get(url)
    yuanta = response.json()
    print("解析元大網站成功")
    return yuanta

def get_rate_from_fubon(year='114', month='9'):
    print("開始解析富邦網站")
    # 富邦
    url = f'https://www.fubon.com/life/product/interest-rate/rate-change/?page=1&year={year}&month={month}#ViewList'
    session = requests.session()
    response = session.get(url, verify=False)
    Soup = BeautifulSoup(response.text,'html.parser')
    pages = Soup.findAll('option')[-1].text
    print('pages:', pages)
    time.sleep(10)
    fubon = []
    for page in range(1, int(pages)+1):
        # print(page)
        url = f'https://www.fubon.com/life/product/interest-rate/rate-change/?page={page}&year={year}&month={month}#ViewList'
        session = requests.session()
        response = session.get(url, verify=False)
        Soup = BeautifulSoup(response.text,'html.parser')
        dict = {}
        
        for i in Soup.findAll('td'):
            if i['data-title'] == '宣告年月':
                dict['rateTime'] = i.text
            if i['data-title'] == '險種名稱':
                dict['productName'] = i.text
            if i['data-title'] == '險種代碼':
                dict['productCode'] = i.text
            if i['data-title'] == '宣告利率':
                dict['rateValue'] = i.text
            if len(list(dict.keys())) == 4:
                fubon.append(dict)
                dict = {}
        time.sleep(randint(1,10))
        print("解析富邦網站成功")
    return fubon

def get_rate_from_fubon2(year='114', month='9'):
    print("開始解析富邦2網站")
    # 富邦
    url = f'https://www.fubon.com/life/product/interest-rate/annuity-rate-change/rate-change/?page=1&year={year}&month={month}#ViewList'
    session = requests.session()
    response = session.get(url, verify=False)
    Soup = BeautifulSoup(response.text,'html.parser')
    pages = Soup.findAll('option')[-1].text
    if pages == '12月':
        pages = 1
    # print('pages:', pages)
    time.sleep(10)
    fubon2 = []
    for page in range(1, int(pages)+1):
        # print(page)
        url = f'https://www.fubon.com/life/product/interest-rate/annuity-rate-change/rate-change/?page={page}&year={year}&month={month}#ViewList'
        session = requests.session()
        response = session.get(url, verify=False)
        Soup = BeautifulSoup(response.text,'html.parser')
        dict = {}
        
        for i in Soup.findAll('td'):
            if i['data-title'] == '宣告年月':
                dict['rateTime'] = i.text
            if i['data-title'] == '險種名稱':
                dict['productName'] = i.text
            if i['data-title'] == '險種代碼':
                dict['productCode'] = i.text
            if i['data-title'] == '契約始期':
                dict['period'] = i.text
            if i['data-title'] == '險種狀態':
                dict['status'] = i.text
            if i['data-title'] == '宣告利率':
                dict['rateValue'] = i.text
            if len(list(dict.keys())) == 6:
                fubon2.append(dict)
                dict = {}
        
        time.sleep(randint(1,10))
        print("解析富邦2網站成功")
    return fubon2
def get_rate_from_taiwanlife(year='114', month='9'):
    print("開始解析台灣人壽網站")
    # 台灣人壽
    url = 'https://www.taiwanlife.com/portal-api/Rate'
    headers = {
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Content-Type': 'application/json;charset=utf-8',  # 如果是 JSON 数据
        'Connection': 'close',
        # 'Authorization': '{}',  # 如果需要认证
        # 根据 Postman 中的设置，复制所有相关的头部
    }
    payload = {
        "item_serno": '',
        "rate_type": "A",
        "page_no": '1',
        "subtype": '',
        "year": f"{int(year)+1911}",
        "month": month
    }

    # 发送 POST 请求，提交表单数据
    session = requests.session()
    response = session.post(url,json=payload, headers=headers, verify=False)
    page_size = response.json()['page_info']['total_page_size']
    taiwanlife = []
    for page in range(1, page_size+1):
        payload = {
            "item_serno": '',
            "rate_type": "A",
            "page_no": str(page),
            "subtype": '',
            "year": f"{int(year)+1911}",
            "month": month
        }
        response = session.post(url,json=payload, headers=headers, verify=False)
        time.sleep(randint(1,10))
        taiwanlife.extend(response.json()['datas'])

    print("解析台灣人壽網站成功")
    return taiwanlife

def get_rate_from_transglobe(year='114', month='9'):
    print("開始解析全球人壽網站")
    # 全球人壽
    headers = {
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Content-Type': 'application/json;charset=utf-8',  # 如果是 JSON 数据
        'Connection': 'close',
        # 'Authorization': '{}',  # 如果需要认证
        # 根据 Postman 中的设置，复制所有相关的头部
    }
    url = 'https://www.transglobe.com.tw/api/mediaAPI?v=1735224343123'
    if int(month) < 10:
        month = f'0{month}'
    payload = {
        "API_ID": "98cd795c40564bcfad2605653b9046c3",
        "session_key": "d64c8a19669945759fbfdf336263929a",
        "params": [
            {
                "year": f"{int(year)+1911}"
            },
            {
                "month": month
            }
        ]
    }
    session = requests.session()
    response = session.post(url,json=payload, headers=headers, verify=False)
    transglobe = response.json()['datas']
    print("解析全球人壽網站成功")
    return transglobe


def get_rate_from_hontai(year='114', month='9'):
    print("開始解析宏泰網站")
    # 宏泰
    url = f'https://www.hontai.com.tw/18pages/rate/{year}/{month}'
    session = requests.session()
    response = session.get(url, verify=False)
    Soup = BeautifulSoup(response.text,'html.parser')
    hontai = []
    count = 1
    tmp = {}
    for i in Soup.findAll('td'):
        if count ==1:
            tmp['time'] = i.text
        if count == 2:
            tmp['name'] = i.text
        if count == 3:
            tmp['code'] = i.text
        if count == 4:
            tmp['rate'] = i.text
            hontai.append(tmp)
            tmp = {}
            count = 1
            continue
        count += 1
    print("解析宏泰網站成功")
    return hontai

def get_rate_from_firstlife():
    print("開始解析第一金網站")
    # 第一金
    url = 'https://www.firstlife.com.tw/FirstWeb/ProductRateChange'
    session = requests.session()
    response = session.get(url, verify=False)
    Soup = BeautifulSoup(response.text,'html.parser')
    firstlife = []
    tmp = {}
    for i in Soup.findAll('tr')[1:-1]:
        tmp['name'] = i.find('th').text
        tmp['code'] = i.findAll('td')[0].text
        tmp['rate'] = i.findAll('td')[1].text
        firstlife.append(tmp)
        tmp = {}
    print("解析第一金網站成功")
    return firstlife

def get_rate_from_kgilife():
    print("開始解析凱基人壽網站")
    # 凱基
    headers = {
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Content-Type': 'application/json;charset=utf-8',  # 如果是 JSON 数据
        'Connection': 'close',
        # 'Authorization': '{}',  # 如果需要认证
        # 根据 Postman 中的设置，复制所有相关的头部
    }
    url = 'https://www.kgilife.com.tw/api/client/DeclareInterestList/GetData?sc_lang=zh-TW&amp;sc_site=kgil-zh-tw'
    payload = {
        'isOIU': 'false',
        'page': '3',
        'searchTxt': ''
        }
    session = requests.session()
    response = session.post(url,json=payload, headers=headers, verify=False)
    page_size = response.json()['PageTotal']
    kgilife = []
    for page in range(1, page_size+1):
        payload = {
            'isOIU': 'false',
            'page': str(page),
            'searchTxt': ''
            }
        response = session.post(url,json=payload, headers=headers, verify=False)
        time.sleep(randint(10,100))
        kgilife.extend(response.json()['InterestData'])
    print("解析凱基人壽網站成功")
    return kgilife

def get_rate_from_skl(year='114', month='9'):
    print("開始解析新光人壽網站")
    # 新光人壽
    url = f'https://www.skl.com.tw/sklife_web/jsp/SklifeRate.jsp?action=rate&year={year}'
    session = requests.session()
    response = session.get(url, verify=False)
    page_size = response.json()['pageInfo']['totalPage']
    skl = []
    for page in range(1, page_size+1):
        url = f'https://www.skl.com.tw/sklife_web/jsp/SklifeRate.jsp?action=rate&year={year}&pageSize=10&page={page}'
        session = requests.session()
        response = session.get(url, verify=False)
        for i in response.json()['content']:
            count = 1
            tmp = {}
            for j in i['row']:
                if count == 1:
                    tmp['name'] = j['value']
                if count == 2:
                    tmp['code'] = j['value']
                if count == 5:
                    tmp['rate'] = j['value']
                    count = 0
                    skl.append(tmp)
                    tmp = {}
                    continue
                count +=1
    print("解析新光人壽網站成功")
    return skl

def get_rate_from_fglife(year='114', month='9'):
    print("開始解析遠雄人壽網站")
    # 遠雄
    url = 'https://www.fglife.com.tw/showInterestRateDate.html'
    headers = {
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',  # 如果是 JSON 数据
        'Connection': 'close',
        # 'Authorization': '{}',  # 如果需要认证
        # 根据 Postman 中的设置，复制所有相关的头部
    }
    payload = {
        'QryYear': year,
        'QryMonth': month
    }
    session = requests.session()
    response = session.post(url,data=payload, headers=headers, verify=False)
    fglife = response.json()['interestRates']
    print("解析遠雄網站成功")
    return fglife

def get_rate_from_taishin():
    print("開始解析台新人壽網站")
    # 台新
    url = 'https://www.taishinlife.com.tw/zh-tw/insured/page/interest-rate-announcement'
    session = requests.session()
    response = session.get(url)
    Soup = BeautifulSoup(response.text,'html.parser')
    taishin = []

    for i in Soup.findAll('option'):
        tmp = {}
        tmp['name'] = i.text
        url = f"https://www.taishinlife.com.tw/zh-tw/insured/page/interest-rate-announcement?product={i['value']}"
        session = requests.session()
        response = session.get(url, verify=False)
        Soup = BeautifulSoup(response.text,'html.parser')
        tmp['rate'] = Soup.findAll('td')[2].text.strip()
        taishin.append(tmp)
        time.sleep(randint(10,100))

    print("解析台新人壽網站成功")
    return taishin

def get_all_rates():
    # 自動取得當前年月
    now = datetime.now()
    year = now.year - 1911
    month = now.month
    all_rates = {
        "aia": get_rate_from_aia(year=year, month=month),
        "yuanta": get_rate_from_yuanta(),
        "fubon": get_rate_from_fubon(year=year, month=month),
        "fubon2": get_rate_from_fubon2(year=year, month=month),
        "taiwanlife": get_rate_from_taiwanlife(year=year, month=month),
        "transglobe": get_rate_from_transglobe(year=year, month=month),
        "hontai": get_rate_from_hontai(year=year, month=month),
        "firstlife": get_rate_from_firstlife(),
        "kgilife": get_rate_from_kgilife(),
        "skl": get_rate_from_skl(year=year, month=month),
        "fglife": get_rate_from_fglife(),
        "taishin": get_rate_from_taishin()
    }
    # 寫入 pkl 檔
    with open("all_rates.pkl", "wb") as f:   # wb = write binary
        pickle.dump(all_rates, f)

def get_rates_and_update_excel(df, year='114', month='9'):

    # 讀取 pkl 檔
    with open("all_rates.pkl", "rb") as f:   # rb = read binary
        all_rates = pickle.load(f)
        print("讀取 pkl 檔成功")
    all_aia = all_rates["aia"]
    yuanta = all_rates["yuanta"]
    fubon = all_rates["fubon"]
    fubon2 = all_rates["fubon2"]
    taiwanlife = all_rates["taiwanlife"]
    transglobe = all_rates["transglobe"]
    hontai = all_rates["hontai"]
    firstlife = all_rates["firstlife"]
    kgilife = all_rates["kgilife"]
    skl = all_rates["skl"]
    fglife = all_rates["fglife"]
    taishin = all_rates["taishin"]
    print(all_aia)

    # 整理資料
    # df = pd.read_excel('./商品名稱.xlsx')
    col_name = f'{year}_{month}'
    df[col_name] = None
    for id, row in df.iterrows():
        try:
            print(id, row['公司'], row['名稱'])
            # 元大
            for item in yuanta['result']:
                if row['公司'].strip()=='元大' and row['名稱'].strip() in item['Contract'].upper() and item['Month'] == month and item['Year'] == f'{int(year)+1911}':
                    df.loc[id, col_name] = item['Rate']
            # 友邦
            for item in all_aia:
                if row['公司'].strip()=='友邦' and row['名稱'].strip() in item['productName'].upper() and item['rateTime']==f'{int(year)+1911}/{month}/01':
                    print(item)
                    df.loc[id, col_name] = item['rateValue']

            # 富邦
            for item in fubon:
                if row['公司'].strip()=='富邦' and row['名稱'].strip() in item['productName'].upper() and item['rateTime']==f'{year}/{month}':
                    df.loc[id, col_name] = item['rateValue']

            # 富邦2
            for item in fubon2:
                if row['公司'].strip()=='富邦' and row['名稱'].strip() in item['productName'].upper() and item['rateTime']==f'{year}/{month}':
                    df.loc[id, col_name] = item['rateValue']
            
            # 台灣人壽
            for item in taiwanlife:
                if row['公司'].strip()=='台灣' and row['名稱'].strip() in item['item_name'].upper():
                    df.loc[id, col_name] = item['rate']
            # 全球
            for item in transglobe:
                if row['公司'].strip()=='全球' and row['名稱'].strip() in item['name'].upper():
                    df.loc[id, col_name] = item['rate']
            # 宏泰
            for item in hontai:
                if row['公司'].strip()=='宏泰' and row['名稱'].strip() in item['name'].upper():
                    df.loc[id, col_name] = item['rate']

            # 第一金
            for item in firstlife:
                if row['公司'].strip()=='第一金' and row['名稱'].strip() in item['name'].upper():
                    df.loc[id, col_name] = item['rate']

            # 凱基
            for item in kgilife:
                if row['公司'].strip()=='凱基' and row['名稱'].strip() in item['PlanName'].upper():
                    df.loc[id, col_name] = item['InterestRate']

            # 新光
            for item in skl:
                if row['公司'].strip()=='新光' and row['名稱'].strip() in item['name'].upper():
                    df.loc[id, col_name] = item['rate']
            # 遠雄
            for item in fglife:
                if row['公司'].strip()=='遠雄' and row['名稱'].strip() in item['planDesc'].upper():
                    df.loc[id, col_name] = item['interestRates']
            # 台新
            for item in taishin:
                if row['公司'].strip()=='台新' and row['名稱'].strip() in item['name'].upper():
                    df.loc[id, col_name] = item['rate']
        except Exception as e:
            print(e)
            continue
        df.to_csv(f'./商品_{year}{month}.csv',index=False, encoding='utf-8-sig')
        return df
        

if __name__ == "__main__":
    get_all_rates()
    # df = pd.read_excel('./商品名稱.xlsx')
    # get_rates_and_update_excel(df)
    