from os import listdir
from tkinter.messagebox import NO
from unicodedata import category
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

df=pd.read_csv('data//1.csv')

header=['Seller Platform','Seller SKU','Manufacturer Name','Manufacturer Code','Product Title','Description','Packaging','QTY','Category','Subcategory','Product Page URL','Attachment URL','Images URL']


def saveData(data):
    with open('data.csv',mode='w',encoding='UTF-8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

class Scrapper():
    def __init__(self,url) -> None:
        self.productPageURL=url
        self.sellerPlatform='Benco Dental'
        self.sellerSKU=None
        self.manufacturerName=None
        self.manufacturerCode=None
        self.productTitle=None
        self.description=None
        self.Packaging="-1"
        self.QTY="-1"
        self.category=None
        self.subCategory=None
        self.AttachmentURL="-1"
        self.ImagesURL=''

        self.soup=None
    
    def sendRequest(self):
        r=requests.get(self.productPageURL)
        self.soup=BeautifulSoup(r.text,'lxml')

    def getSellerSKU(self):
        self.sellerSKU=self.soup.find("span",itemprop="sku").text
        

    def getManufactureName(self):
        self.manufacturerName=self.soup.find("span",itemprop="brand").text
    
    def getManufacturerCode(self):
        self.manufacturerCode=self.soup.find("meta",itemprop="model").get('content')

    def getProductTitle(self):
        self.productTitle=self.soup.find(class_="product-name",itemprop="name").text.strip()

    def getDescription(self):
        try:
            self.description=self.soup.find(class_='product-description',itemprop="description").text.strip()
        except:
            self.description="-1"

    def getCategory(self):
        self.category=self.soup.find(class_='breadcrumb-bar').findAll('li')[1].text.replace('/','').strip()

    def getSubCategory(self):
        self.subCategory=self.soup.find(class_='breadcrumb-bar').findAll('li')[2].text.replace('/','').strip()

    def getImages(self):
        
        x=self.soup.find(id='activeImageArea')
        y=self.soup.find(id='alternateImageArea')
        
        if x is not None:
            x=x.find('img').get('src').split('?')[0]
            self.ImagesURL=str(self.ImagesURL)+x

        if y is not None:
            y=y.find('img').get('src').split('?')[0]
            self.ImagesURL+=","+self.ImagesURL


masterData=[]
for index,i in df.iterrows():
    obj=Scrapper(i['url'])
    obj.sendRequest()
    obj.getSellerSKU()
    obj.getCategory()
    obj.getSubCategory()
    obj.getDescription()
    obj.getImages()
    obj.getManufactureName()
    obj.getManufacturerCode()
    obj.getProductTitle()
    header=['Seller Platform','Seller SKU','Manufacturer Name',
    'Manufacturer Code','Product Title','Description','Packaging','QTY','Category','Subcategory','Product Page URL','Attachment URL','Images URL']
    masterData.append([obj.sellerPlatform,obj.sellerSKU,obj.manufacturerName,obj.manufacturerCode,obj.productTitle,obj.description,obj.Packaging,obj.QTY,obj.category,
    obj.subCategory,obj.productPageURL,obj.AttachmentURL,obj.ImagesURL])
    if index%50:
        saveData(masterData)
    

saveData()