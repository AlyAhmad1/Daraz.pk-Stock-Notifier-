from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import json
from bs4 import BeautifulSoup
import math

# Create your views here.
class Scrap:
    def Daraz(self,request):
        if request.method=='POST':
            Urls = request.POST['URL']
            Url = Urls.split(',')
            A = []
            try:
                A.append(Scrap.execute_Scrap(Url))
            except:
                messages.error(request,'Error Check You URL Or Input Comma Separated URLS')
                return render(request,'DarazScrapper/Index.html')
            Data = {'URL':Url,'Scrapped':A}
            return render(request,'DarazScrapper/Index.html',Data)
        return render(request,'DarazScrapper/Index.html')

    @classmethod
    def execute_Scrap(cls, URL):
        try:
            result = []
            for i in URL:
                r = requests.get(i)
                soup = BeautifulSoup(r.text, 'html.parser')
                scripts = str(soup.find_all("script")[142])
                stock_s = scripts.split('stockList')[1].strip().split(']')[0][3:]
                stock_list = json.loads(stock_s)
                stock = int(stock_list['stoock'])
                product_name = scripts.split('pdt_name')[1].split('page')[0][2:-2]
                price = scripts.split('pdt_price')[1].split('"}')[0][6:]
                date = datetime.date.today()
                r = scripts.split('ratings')[4][3:].split('}')[0].split(',')
                r1 = r[0]+r[1]
                r2 = scripts.split('ratings')[4][3:].split('}')[0].split(':')[4][1:-1].split(',')
                r3 = f'Ratings 5-stars:{r2[0]}\t 4-stars:{r2[1]}\t3-stars:{r2[2]}\t2-stars:{r2[3]}\t1-stars:{r2[4]}\t'
                rating = r1 + '\n' + r3
                discount, discounted_price = Scrap.discount(scripts, price)
                A = [product_name, stock, price, rating, discount, discounted_price, date]
                result.append(A)

            return result
        except Exception as e:
            raise Exception(e)

    @classmethod
    def discount(cls, script,price):
        try:
            stock_s = script.split('pdt_discount')[1].split(',')[0][4:-2]
            discount = stock_s
            d = 100 - int(stock_s)
            discount_price = math.ceil(int(price)*(d/100))

        except:
            discount = 0
            discount_price = price
        return discount, discount_price


    def Help(self, request):
        return render(request, 'DarazScrapper/Help.html')

    def About(self, request):
        return render(request, 'DarazScrapper/About.html')
