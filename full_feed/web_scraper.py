import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape_site(link, lehrstuhl_name, index):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    entries = []

    if index in [0, 1, 2]:
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
