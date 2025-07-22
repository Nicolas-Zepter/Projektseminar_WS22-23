from full_feed.rss_scraper import parse_rss_feeds
from full_feed.web_scraper import scrape_all_sites
from full_feed.data_utils import merge_and_save

def run_update():
    links = [
        "https://www.is.rw.fau.de/neuigkeiten",
        "https://www.kommunikationswissenschaft.rw.fau.de",
        "https://www.digitaltransformation.rw.fau.eu",
        "https://www.pw.rw.fau.de",
        "https://www.vwrm.rw.fau.de/aktuelles",
        "https://www.empiricalecon.rw.fau.de",
        "https://www.emmi.rw.fau.de/aktuelles",
        "https://www.finanzwissenschaft.rw.fau.de",
        "http://www.gesoek.wiso.fau.de"
    ]

    lehrstuhl_names = [
        "Digital Industrial Service Systems", "Kommunikationswissenschaft",
        "Digital Transformation Lab", "Rechnungswesen und Prüfungswesen",
        "Versicherungswirtschaft", "Empirische Wirtschaftsforschung",
        "Empirische Mikroökonomie", "Finanzwissenschaft", "Gesundheitsökonomie"
    ]

    df_rss = parse_rss_feeds("lehrstuhl.csv")
    df_scraped = scrape_all_sites(links, lehrstuhl_names)
    merge_and_save(df_rss, df_scraped)

if __name__ == "__main__":
    run_update()
