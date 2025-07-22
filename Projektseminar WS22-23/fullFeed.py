from bs4 import BeautifulSoup
from datetime import datetime
#from flask import Flask, render_template
import feedparser
import pandas as pd
import requests

links = ["https://www.is.rw.fau.de/neuigkeiten", "https://www.kommunikationswissenschaft.rw.fau.de", "https://www.digitaltransformation.rw.fau.eu", "https://www.pw.rw.fau.de", "https://www.vwrm.rw.fau.de/aktuelles", "https://www.empiricalecon.rw.fau.de", "https://www.emmi.rw.fau.de/aktuelles", "https://www.finanzwissenschaft.rw.fau.de", "http://www.gesoek.wiso.fau.de"]
lehrstuhl = ["Lehrstuhl für Digital Industrial Service Systems", "Juniorprofessur für Kommunikationswissenschaft", "Digital Transformation: Bits to Energy Lab Nuremberg", "Lehrstuhl für Rechnungswesen und Prüfungswesen", "Lehrstuhl für Versicherungswirtschaft und Risikomanagement", "Lehrstuhl für Statistik und empirische Wirtschaftsforschung","Lehrstuhl für Volkswirtschaftslehre, insbes. Empirische Mikroökonomie", "Lehrstuhl für Finanzwissenschaft", "Professur für Gesundheitsökonomie"]

def rss_feed():
    df = pd.DataFrame(columns=['Lehrstuhl', 'Title', 'Date', 'Link', 'Description'])
    df_input = pd.read_csv("lehrstuhl.csv")

    for lehrstuhl_index in range(len(df_input.index)):
        lehrstuhl = df_input["Name"][lehrstuhl_index]
        feed = feedparser.parse(df_input["Link_RSS"][lehrstuhl_index])
        for entry_index in range(0, len(feed.entries)):

            date_string_old = feed.entries[entry_index].published
            date_time_obj = datetime.strptime(date_string_old, '%a, %d %b %Y %H:%M:%S %z')
            date_string_new = datetime.strftime(date_time_obj, "%Y/%m/%d")

            entry_string = pd.Series({'Lehrstuhl': lehrstuhl, 'Title': feed.entries[entry_index].title, 'Date': date_string_new, 'Link': feed.entries[entry_index].link, 'Description': feed.entries[entry_index].description})
            df = pd.concat([df, entry_string.to_frame().T], ignore_index=True)
    return df

def aktualisieren():
    df_rss = rss_feed()
    df = pd.DataFrame(columns=['Lehrstuhl', 'Title', 'Date', 'Link'])
    df2 = pd.DataFrame(columns=['Description'])
    df3 =pd.DataFrame()
    l_index = 0
    for link in links:
        if l_index < 3:
            page = requests.get(links[l_index])
            soup = BeautifulSoup(page.content, 'html.parser')
            tes = soup.select("h2")
            tes2 = soup.select("p")
            for el in tes:
                datum = el.a["href"][1:5] + "-" + el.a["href"][6:8] + "-" + el.a["href"][9:11]
                entry_string = pd.Series({'Lehrstuhl': lehrstuhl[l_index], 'Title': el.a.text, 'Date': datum , 'Link': links[l_index] + el.a["href"]})
                df = pd.concat([df, entry_string.to_frame().T], ignore_index=True)
            for il in tes2:
                if il.has_attr("itemprop"):
                    if len(il.text) > 50:
                        entry_string = pd.Series({"Description" : il.text})
                        df2 = pd.concat([df2, entry_string.to_frame().T], ignore_index=True)
        elif l_index == 3:
            page = requests.get(links[l_index])
            soup = BeautifulSoup(page.content, 'html.parser')
            tes = soup.select("h3")
            tes2 = soup.select("p")
            for el in tes:
                entry_string = pd.Series({'Lehrstuhl': lehrstuhl[l_index], 'Title': el.text, 'Date': "NA" , 'Link': "NA"})
                df = pd.concat([df, entry_string.to_frame().T], ignore_index=True)
            for il in tes2:    
                if len(il.text) > 50:
                    entry_string = pd.Series({"Description" : il.text})
                    df2 = pd.concat([df2, entry_string.to_frame().T], ignore_index=True)
        elif l_index == 4:
            page = requests.get(links[l_index])
            soup = BeautifulSoup(page.content, 'html.parser')
            tes = soup.select("li")
            for el in tes:
                if el.find("strong"):
                    entry_string = pd.Series({'Lehrstuhl': lehrstuhl[l_index], 'Title': "NA", 'Date': "NA" , 'Link': "NA"})
                    df = pd.concat([df, entry_string.to_frame().T], ignore_index=True)
                    entry_string1 = pd.Series({"Description" : el.text})
                    df2 = pd.concat([df2, entry_string1.to_frame().T], ignore_index=True)
        elif l_index == 5:
            page = requests.get(links[l_index])
            soup = BeautifulSoup(page.content, 'html.parser')
            tes = soup.select("h2")
            tes2 = soup.select("p")
            for el in tes:
                if el.has_attr("id"):
                    datum = el.a["href"][1:5] + "-" + el.a["href"][6:8] + "-" + el.a["href"][9:11]
                    entry_string = pd.Series({'Lehrstuhl': lehrstuhl[l_index], 'Title': el.a.text, 'Date': datum , 'Link': links[l_index] + el.a["href"]})
                    df = pd.concat([df, entry_string.to_frame().T], ignore_index=True)
            for il in tes2:
                if il.has_attr("itemprop"):
                    if len(il.text) > 50:
                        entry_string = pd.Series({"Description" : il.text})
                        df2 = pd.concat([df2, entry_string.to_frame().T], ignore_index=True)
        elif l_index == 6:
            page = requests.get(links[l_index])
            soup = BeautifulSoup(page.content, 'html.parser')
            tes = soup.select("p")
            for el in tes:
                if not el.has_attr("class"):
                    entry_string = pd.Series({'Lehrstuhl': lehrstuhl[l_index], 'Title': "NA", 'Date': "NA" , 'Link': "NA"})
                    df = pd.concat([df, entry_string.to_frame().T], ignore_index=True)
                    entry_string1 = pd.Series({"Description" : el.text})
                    df2 = pd.concat([df2, entry_string1.to_frame().T], ignore_index=True)
        elif l_index == 7:
            page = requests.get(links[l_index])
            soup = BeautifulSoup(page.content, 'html.parser')
            tes = soup.select("p")
            count = 3
            datum = ""
            for el in tes:
                if not el.has_attr("class"):
                        if count%3 == 0 and count <= 66:
                            entry_string = pd.Series({'Lehrstuhl': lehrstuhl[l_index], 'Title': el.text, 'Date': "NA" , 'Link': "NA"})
                            df = pd.concat([df, entry_string.to_frame().T], ignore_index=True)
                            count+=1
                        elif (count-1)%3 == 0 and count <= 66:         
                            entry_string1 = pd.Series({"Description" : el.text})
                            df2 = pd.concat([df2, entry_string1.to_frame().T], ignore_index=True)
                            count+=1
                        else:
                            datum = el.text[7:11] + "/" + el.text[4:6] + "/" + el.text[0:2] 
        df3 = pd.concat([df, df2], axis=1, join='inner')
        l_index +=1
    df_all=pd.concat([df_rss, df3], axis=0)
    df_all = df_all[['Date', 'Title', 'Lehrstuhl', 'Description', 'Link']]
    df_all.to_csv('allnews.csv', index=False, encoding='utf-8-sig')
    print("done")
    
aktualisieren()
#app = Flask(__name__)

#@app.route('/')
#def index():
#    return render_template('FrontEnd.html')

#if __name__ == "__main__":
#    app.run()    







