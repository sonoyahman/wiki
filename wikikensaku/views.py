from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib.parse
import os
import datetime
import time

# Create your views here.
#人の場合
def hantei_zinbutu(soup):
    tablelist_text = soup.find("div",{"id":"bodyContent"}).get_text() #wiki本文を抽出
    hitohantei =  ("生誕" in tablelist_text) or ("誕生" in tablelist_text) or ("出生" in tablelist_text) or ("本名" in tablelist_text) or ("生年月日" in tablelist_text)
    return hitohantei

def infobox_shutoku(soup,tsuika_taisho,url):
    tablelist = soup.find(class_="infobox")
    infobox = pd.DataFrame({"名前":[tsuika_taisho],"URL":[url]})
    
    #項目を取得しカラム名として追加+項目を追加
    for youso in tablelist.findAll("tr"):  
        komoku = youso.find("th")
        if komoku != None:
            komoku = komoku.get_text().replace('\n','')
            komoku = komoku.lstrip()

            naiyou = youso.find("td")
            if naiyou != None:
                naiyou = naiyou.get_text().replace('\n','')
                naiyou = naiyou.lstrip()
                infobox[komoku]=[naiyou]
                #zinbutu_list.to_csv("出発点"+zinbutu_list.iloc[0,0] +".csv", encoding='utf_8_sig')#ファイル出力
                    
    return infobox

def link_shutoku(soup,tsuika_taisho):
    shutoku_list = pd.DataFrame()
    soup_honbun = soup.find("div",{"id":"bodyContent"}) #wiki本文を抽出
    tsuika_taisho = soup.find("h1",class_="firstHeading", id="firstHeading").get_text()

    for link in soup_honbun.findAll("a",href=re.compile("^(/wiki/)((?!:).)*$")):
        if "href" in link.attrs:
            html = "https://ja.wikipedia.org"+link.attrs["href"]
            tmp=pd.DataFrame({"名前":[tsuika_taisho],"名称-リンク先":link.attrs["title"],"URL":[html]})
            shutoku_list=pd.concat([shutoku_list,tmp])  
    
    shutoku_list=shutoku_list.drop_duplicates() #ダブり削除
    shutoku_list=shutoku_list.reset_index(drop=True) #インデックス振り直し
    
    #shutoku_list.to_csv(zinbutu.iloc[0,0]+".csv", encoding='utf_8_sig')
    return shutoku_list

def mainkensakufunc(request):
    print("プログラム呼び出し")
    search=request.POST.get("search")
    
    if search != None:
        print("検索開始")
        
        #wiki_url ="https://ja.wikipedia.org/wiki/"
        search_url ="https://ja.wikipedia.org/wiki/" + search 
        
        html = requests.get(search_url)     
        soup = BeautifulSoup(html.text,"lxml")
        
        if hantei_zinbutu(soup)==True:
            tsuika_taisho = soup.find("h1",class_="firstHeading", id="firstHeading").get_text()
            print(tsuika_taisho)
            seed_link=link_shutoku(soup,tsuika_taisho)
            print(seed_link)
            result_table=seed_link.to_html(justify="left",render_links=True)
            #print(os.getcwd())
            dt_now = str(time.time())
            file_name = tsuika_taisho+dt_now+".csv"
            file_address = "media/"+file_name
            csv_table = seed_link.to_csv(file_address, encoding='shift_jis')
            
            output = render(request,"main_result.html",{"table":result_table,"fileaddress":"../"+file_address,"filename":file_name})
            return output
        
        else:
            print("人以外")
            output = render(request,"main.html",{"message":"人物名を入力してください。又は、wikiに記事が存在しない人物です。"})
            return output
    else:
        print("空欄")
        output = render(request,"main.html",{"message":""})
        return output
    
        #seed_info=infobox_shutoku(soup,tsuika_taisho,url)


class MainClass(TemplateView):
    template_name = 'main.html'