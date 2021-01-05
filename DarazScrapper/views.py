from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import json
from bs4 import BeautifulSoup


# Create your views here.
class Scrap:
    def Daraz(self,request):
        if request.method=='POST':
            Urls = request.POST['URL']
            Url=Urls.split(',')
            URL_foud = True
            A = []
            try:
                A.append(Scrap.execute_Scrap(Url, URL_foud))
            except:
                messages.error(request,'Error Check You URL Or Input Comma Separated URLS')
                return render(request,'DarazScrapper/Index.html')
            Data = {'URL':Url,'Scrapped':A}
            return render(request,'DarazScrapper/Index.html',Data)
        return render(request,'DarazScrapper/Index.html')


    @classmethod
    def execute_Scrap(cls,URL,URL_foud):
        try:
            result = []
            for i in URL:
                r = requests.get(i)
                soup = BeautifulSoup(r.text, 'html.parser')
                scripts = str(soup.find_all("script")[143])
                stock_s = scripts.split('stockList')[1].strip().split(']')[0][3:]
                stock_list = json.loads(stock_s)
                stock = int(stock_list['stoock'])
                product_name = scripts.split('pdt_name')[1].split('page')[0][2:-2]
                date = datetime.date.today()
                # print('---------------',product_name, stock, date)
                print(stock_s)
                A = [product_name, stock, date]
                result.append(A)
            return result
        except:
            raise Exception('')


