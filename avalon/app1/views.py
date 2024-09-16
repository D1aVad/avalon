from django.shortcuts import render
from bs4 import BeautifulSoup
import csv
import re
import unidecode
from selenium import webdriver
import time
from .forms import SearchForm
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options




def main_page(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            
            search = form.cleaned_data['search'] 
    

            url = f"https://www.avito.ru/derbent?q={search}"
            r_url = 'https://www.avito.ru'

            

            

            driver = webdriver.Chrome(service= Service())
            driver.get(url)
            time.sleep(35)
            html = driver.page_source

            soup = BeautifulSoup(html)

            elements = soup.find_all('div', class_= 'iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum')
            products = []

            for elem in elements:
                prod_data = {}

                prod_name = elem.find('h3', class_= 'styles-module-root-GKtmM styles-module-root-YczkZ styles-module-size_l-iNNq9 styles-module-size_l_compensated-KFJud styles-module-size_l-YMQUP styles-module-ellipsis-a2Uq1 styles-module-weight_bold-jDthB stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-header-l-iFKq3')
                if prod_name:
                    prod_data['title'] = prod_name.text.strip()
                prod_price = elem.find('p', class_= 'styles-module-root-YczkZ styles-module-size_l-iNNq9 styles-module-size_l_dense-j7nBe styles-module-size_l-YMQUP styles-module-size_dense-TQdU6 stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-l-dense-x3fYE')
                if prod_name:
                    prod_data['price'] = re.sub(r"\\xA0", " ", prod_price.text.strip())
                
                prod_url = elem.find('a', class_= 'iva-item-sliderLink-uLz1v')
                if prod_url:
                    url = r_url + prod_url['href']
                    prod_data['url'] = url
                prod_img = elem.find('img', class_= 'photo-slider-image-YqMGj')
            
                if prod_img:
                    prod_data['img'] = prod_img['src']
                




                for key, value in prod_data.items():
                    modified_value = unidecode.unidecode(value).replace('\xa0', '')
                    prod_data[key] = modified_value

                products.append(prod_data)

                with open('avito_prod.csv', mode='w', newline='', encoding='utf-8') as file:
                    fieldnames = ['title', 'price', 'url', 'img']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)

                    writer.writeheader()
                    for product in products:
                        writer.writerow(product)

                
                
                driver.quit()
                
            return render(request, 'main_page.html')
    else:
        return render(request, 'main_page.html')
