from bs4 import BeautifulSoup
import requests
import json
link='https://www.worldometers.info/coronavirus/'
source = requests.get(link).text    
soup = BeautifulSoup(source, 'lxml')

def extract_nat():
    #locating required data
    tb=soup.find('table',id='main_table_countries_today')
    rows=tb.find_all('tr',class_="")[1:21]#countries
    
    #initializing variables to store
    name_list=[]
    tcase,tdeath,trecov,acases,tcasepm,deathpm,ttest,testpm,pop,hypr={},{},{},{},{},{},{},{},{},{}

    #extracting & storing the data
    for nat in rows:
        data=nat.find_all('td')

        if nat.a==None:
            hyp=''
        else:
            hyp=link+nat.a['href']

        name_list.append(data[1].text.strip())
        tcase[name_list[-1]]=resolve(data[2].text)
        tdeath[name_list[-1]]=resolve(data[4].text)
        trecov[name_list[-1]]=resolve(data[6].text)
        acases[name_list[-1]]=resolve(data[8].text)
        tcasepm[name_list[-1]]=resolve(data[10].text)
        deathpm[name_list[-1]]=resolve(data[11].text)
        ttest[name_list[-1]]=resolve(data[12].text)
        testpm[name_list[-1]]=resolve(data[13].text)
        pop[name_list[-1]]=resolve(data[14].text)
        hypr[name_list[-1]]=hyp
    return name_list,tcase,tdeath,trecov,acases,tcasepm,deathpm,ttest,testpm,pop,hypr

def extract_wr():
    tb=soup.find('table',id='main_table_countries_today')    
    #initializing variables to store
    name_list=[]
    tcase={}
    ncase={}
    tdeath={}
    ndeath={}
    trecov={}
    acases={}

    wr=tb.find_all('tr',{'class':"total_row_world"})[-1]#only world
    data=wr.find_all('td') 

    name_list.append(data[1].text)
    tcase[data[1].text]=int(data[2].text.replace(',',''))
    ncase[data[1].text]=int(data[3].text.replace(',',''))
    tdeath[data[1].text]=int(data[4].text.replace(',',''))
    ndeath[data[1].text]=int(data[5].text.replace(',',''))
    trecov[data[1].text]=int(data[6].text.replace(',',''))
    acases[data[1].text]=int(data[7].text.replace(',',''))    

    rw=tb.find_all('tr',{'class':"total_row_world row_continent"})#list of continents
    for row in rw[:-1]:
        data=row.find_all('td')
        name_list.append(data[1].text[1:-1])
        tcase[name_list[-1]]=resolve(data[2].text)
        ncase[name_list[-1]]=resolve(data[3].text)
        tdeath[name_list[-1]]=resolve(data[4].text)
        ndeath[name_list[-1]]=resolve(data[5].text)
        trecov[name_list[-1]]=resolve(data[6].text)
        acases[name_list[-1]]=resolve(data[7].text)    
    return name_list,tcase,ncase,tdeath,ndeath,trecov,acases

def natone(url):
    parsed_html = requests.get(url) # url is link to the country specific page of site
    soup = BeautifulSoup(parsed_html.content, "lxml")

    divs=soup.find_all('div',class_="row graph_row")
    gr_list=[]
    req=('Total Cases','Daily New Cases','Active Cases','Total Deaths','Daily Deaths')
    for i in divs:
        script=str(i.script)
        hd=script.split('text: \'',1)[1].split('\'',1)[0]
        if hd not in req:
            continue
        dates = script.split("categories: [",1)[1].split("]",1)[0]
        dates = "["+dates+"]"
        dates = json.loads(dates)

        data = script.split("data: [",1)[1].split("]",1)[0]
        data = "["+data+"]"
        data = json.loads(data)
        for i in range(len(data)):
            if data[i]==None:
                data[i]=0
        gr_list.append((hd,dates,data))
    return gr_list

def resolve(data):
    if data=='' or data==' ' or data=='N/A':
        return 0
    else:
        return int(data.replace(',',''))