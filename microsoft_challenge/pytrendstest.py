from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

kw_list = ["Blockchain", "test"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
print(pytrends.interest_over_time())
