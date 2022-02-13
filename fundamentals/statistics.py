from bs4 import BeautifulSoup
from util.request_handler import load_webpage


class Statistics:

    def __init__(self, ticker):

        self.data = {}

        self.ticker = ticker
        print("\n\n--- Scrapping the Statistics - Ticker: " + self.ticker + " ---")
        self.webpage = "https://finance.yahoo.com/quote/" + self.ticker + "/key-statistics?p=" + self.ticker

        src = load_webpage(self.webpage)

        self.set_statistics_data(src.content)

    def set_statistics_data(self, page_content):

        # getting key statistics data from yahoo finance for the given ticker
        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.findAll("table")
        for t in tabl:
            rows = t.find_all("tr")
            for row in rows:
                if len(row.get_text(separator='|').split("|")[0:2]) > 0:
                    self.data[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[-1]

    def get_data(self):
        return self.data
