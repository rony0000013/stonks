from pytickersymbols import PyTickerSymbols

stock_data = PyTickerSymbols()
sp_stocks = stock_data.get_stocks_by_index("S&P 500")
nd_stocks = stock_data.get_stocks_by_index("NASDAQ 100")
dow_stocks = stock_data.get_stocks_by_index("DOW JONES")

nd_stocks = tuple(map(lambda x: (x["name"], x["symbol"]), nd_stocks))
sp_stocks = tuple(map(lambda x: (x["name"], x["symbol"]), sp_stocks))
dow_stocks = tuple(map(lambda x: (x["name"], x["symbol"]), dow_stocks))
stocks = nd_stocks + sp_stocks + dow_stocks

# print(list(nd_stocks) + list(sp_stocks) + list(dow_stocks))

import csv
import json


# data = {}
# for stock in stocks:
#     data[stock[0]] = stock[1]
#     # Save data as JSON
#     with open("stocks.json", "w") as file:
#         json.dump(data, file)

stocks = json.load(open("stocks.json"))

print(len(stocks))
