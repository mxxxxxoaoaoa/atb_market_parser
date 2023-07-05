# from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs

class AtbWebDriver:
    def __init__(self) -> None:
        pass

    def get_all_categories(self):
        
        """return all categories of products from ATB market by list"""

        url = "https://www.atbmarket.com"
        driver = uc.Chrome()
        driver.get(url)
        source = driver.page_source
        soup = bs(source, 'lxml')
        category_menu = soup.find('ul', {'class': 'category-menu'})
        category_menu_li = category_menu.find_all("li", {'class': "submenu__item"})
        categories = []
        for li in category_menu_li:
            categories.append(url + li.find('a')['href'])
        driver.close()
        return categories
    
    def get_paginations(self, category):

        """return categories with hers number of pages. this future for next steps."""

        try:
            link = f"{category}?page=1000"
            driver = uc.Chrome()
            driver.get(link)
            soup = bs(driver.page_source, 'lxml')
            res = soup.find_all("a", {'class': 'product-pagination__link'})
            title = soup.find('h1', {'class': 'page-title'}).text
            if len(res) == 0:
                driver.close()
                return {
                    "title": title,
                    'pagination': 1,
                    'url': category
                }
            if len(res)!= 0:
                driver.close()
                return {
                    'title': title,
                    'pagination': res[-1].text,
                    'url': category
                }
        except Exception as e:
            print(e)
            return {"message": e}
        
    def get_product(self, category_obj):

        """return json array with product metadata: price, title, url, photo. by category"""

        pages = int(category_obj['pagination'])
        return_data = {
            'title': category_obj['title'],
            'url': category_obj['url'],
            'products': []
        }
        driver = uc.Chrome()
        print("pages: ", pages)
        for i in range(1, pages+1):
            print("page: ", i)
            url = f"{category_obj['url']}?page={i}"
            driver.get(url)
            soup = bs(driver.page_source, 'lxml')
            div = soup.find('div', {"class": "catalog-list"})
            articles = div.find_all('article', {'class': 'catalog-item'})
            for article in articles:
                try:
                    # parse price
                    price_div = article.find("div", {"class": "catalog-item__product-price"})
                    price_datas = price_div.find_all("data")
                    prices = []
                    for data in price_datas:
                        prices.append(float(data['value']))
                    item_price = min(prices) # ended price
                    # # # # # # # # # 
                except Exception as e:
                    print('parse price error')
                    print(e)
                try:
                    # parse title
                    title_div = article.find('div', {'class': 'catalog-item__title'}).find('a')
                    item_url = title_div['href'] # url for product
                    item_title = title_div.text # title of product
                    # # # # # # # # 
                except Exception as e:
                    print('parse title error')
                    print(e)

                try:
                    #parse photo
                    photo_div = article.find("div", {'class': 'catalog-item__photo'}).find('a').find('picture').find('source')
                    item_photo_url = photo_div['srcset'] # url of photo for product
                    # # # # # # # 
                except Exception as e:
                    print("parse photo error")
                    print(e)

                main_host = "https://www.atbmarket.com"
                return_data['products'].append(
                    {
                        "price": item_price,
                        'title': item_title,
                        'url': main_host + item_url,
                        'photo': item_photo_url 
                    }
                )

        driver.close()
        return return_data