import pandas as pd
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import requests


def parse_rss_feeds(csv_path):
    df_input = pd.read_csv(csv_path)
    data = []

    for _, row in df_input.iterrows():
        lehrstuhl = row["Name"]
        feed = feedparser.parse(row["Link_RSS"])

        for entry in feed.entries:
            try:
                date_obj = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                date_str = date_obj.strftime('%Y/%m/%d')
            except AttributeError:
                date_str = "NA"

            data.append({
                "Lehrstuhl": lehrstuhl,
                "Title": entry.title,
                "Date": date_str,
                "Link": entry.link,
                "Description": entry.get("description", "")
            })

    return pd.DataFrame(data)


def scrape_site(link, lehrstuhl_name, index):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    entries = []

    if index == 0 or index == 1 or index == 2:
        headers = soup.select("h2")
        paras = soup.select("p")
        for h in headers:
            if h.a:
                href = h.a.get("href", "")
                date = f"{href[1:5]}-{href[6:8]}-{href[9:11]}" if len(href) > 10 else "NA"
                entries.append({
                    "Lehrstuhl": lehrstuhl_name,
                    "Title": h.a.text.strip(),
                    "Date": date,
                    "Link": link + href,
                    "Description": ""
                })
        for p in paras:
            if p.has_attr("itemprop") and len(p.text) > 50:
                entries[-1]["Description"] = p.text.strip()

    return pd.DataFrame(entries)


def scrape_all_sites(links, lehrstuhl_names):
    df_all = pd.DataFrame(columns=['Lehrstuhl', 'Title', 'Date', 'Link', 'Description'])

    for i, url in enumerate(links):
        try:
            df = scrape_site(url, lehrstuhl_names[i], i)
            df_all = pd.concat([df_all, df], ignore_index=True)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return df_all


def run_update():
    
    # Input
    lehrstuhl_csv = "lehrstuhl.csv"
    links = [
        "https://www.is.rw.fau.de/neuigkeiten", "https://www.kommunikationswissenschaft.rw.fau.de",
        "https://www.digitaltransformation.rw.fau.eu", "https://www.pw.rw.fau.de",
        "https://www.vwrm.rw.fau.de/aktuelles", "https://www.empiricalecon.rw.fau.de",
        "https://www.emmi.rw.fau.de/aktuelles", "https://www.finanzwissenschaft.rw.fau.de",
        "http://www.gesoek.wiso.fau.de"
    ]
    lehrstuhl_names = [
        "Digital Industrial Service Systems", "Kommunikationswissenschaft",
        "Digital Transformation Lab", "Rechnungswesen und Prüfungswesen",
        "Versicherungswirtschaft", "Empirische Wirtschaftsforschung",
        "Empirische Mikroökonomie", "Finanzwissenschaft", "Gesundheitsökonomie"
    ]

    # Parse
    df_rss = parse_rss_feeds(lehrstuhl_csv)
    df_scraped = scrape_all_sites(links, lehrstuhl_names)

    # Combine and export
    df_all = pd.concat([df_rss, df_scraped], ignore_index=True)
    df_all = df_all[['Date', 'Title', 'Lehrstuhl', 'Description', 'Link']]
    df_all.to_csv("allnews.csv", index=False, encoding='utf-8-sig')
    print("Update complete – allnews.csv created.")


if __name__ == "__main__":
    run_update()
