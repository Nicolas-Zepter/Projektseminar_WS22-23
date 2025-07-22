import pandas as pd

def merge_and_save(df_rss, df_scraped, output_path="allnews.csv"):
    df_all = pd.concat([df_rss, df_scraped], ignore_index=True)
    df_all = df_all[['Date', 'Title', 'Lehrstuhl', 'Description', 'Link']]
    df_all.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Data saved to {output_path}")
