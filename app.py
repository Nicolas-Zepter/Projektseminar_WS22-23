from flask import Flask, render_template, request
import pandas as pd
import os
import threading
import webbrowser
import time

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), 'allnews.csv')

def load_data():
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["Date", "Title", "Lehrstuhl", "Link"])  # Remove rows missing key info
    df["Description"] = df["Description"].fillna("")  # Replace NaN with empty string
    return df

def get_lehrstuhl_options(df):
    return sorted(df["Lehrstuhl"].dropna().unique())

@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_data()
    search_query = request.values.get('search', '').strip()
    lehrstuhl_filter = request.values.get('lehrstuhl', '')
    sort_by = request.values.get('sort_by', 'Date')
    sort_dir = request.values.get('sort_dir', 'desc')

    # Filter by Lehrstuhl
    if lehrstuhl_filter:
        df = df[df['Lehrstuhl'] == lehrstuhl_filter]

    # Search in Title and Description
    if search_query:
        mask = df['Title'].str.contains(search_query, case=False, na=False) |\
               df['Description'].str.contains(search_query, case=False, na=False)
        df = df[mask]

    # Sort
    ascending = (sort_dir == 'asc')
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=ascending)
    else:
        df = df.sort_values(by='Date', ascending=False)

    # Prepare Lehrstuhl dropdown
    lehrstuhl_options = get_lehrstuhl_options(load_data())

    # Convert to records for template
    records = df.to_dict(orient='records')

    return render_template(
        'index.html',
        records=records,
        lehrstuhl_options=lehrstuhl_options,
        search_query=search_query,
        lehrstuhl_filter=lehrstuhl_filter,
        sort_by=sort_by,
        sort_dir=sort_dir
    )

if __name__ == '__main__':
    threading.Thread(target=lambda: (time.sleep(1), webbrowser.open_new_tab('http://127.0.0.1:5000'))).start()
    app.run(debug=True)
