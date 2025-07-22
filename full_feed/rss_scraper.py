import pandas as pd
import feedparser
from datetime import datetime

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
