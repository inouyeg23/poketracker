import streamlit as st
from bs4 import BeautifulSoup
import requests, json, lxml


st.title('_Poggers_ Pokemon Card Tracker')

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

query = st.text_input("query", label_visibility='hidden')

params = {
    '_nkw': query,           # search query  
    '_pgn': 1,                # page number
    'LH_Sold': '1'          # shows sold items
}


def get_results():
    html = requests.get('https://www.ebay.com/sch/i.html', params=params, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    data = []

    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        #link = item.select_one('.s-item__link')['href']
        try:
            price = item.select_one('.s-item__price').text
        except:
            price = None

        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None
     
        try:
            sold_date = item.select_one(".s-item__title--tagblock .POSITIVE").text
        except:
            sold_date = None

        if title == "Shop on eBay":
            continue

        data.append({
            'title': title, 
            #'link': link, 
            'price': price,
            'shipping': shipping,
            'date': sold_date
        })

    return data


st.write(get_results())
