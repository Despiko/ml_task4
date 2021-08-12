import pandas as pd
import yfinance as yf

symbols = ["AMZN"]

yf_period = "20y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

stock_parameters = ["shortName", "sector", "industry", "quoteType",
                    "exchange", "totalAssets", "marketCap", "beta", "trailingPE", "volume",
                    "averageVolume", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "dividendRate", "phone"]

yf_info = pd.DataFrame(index = stock_parameters, columns = symbols)

for i in symbols:
    l = []             # initialize
    x = yf.Ticker(i)   # get ticker info
    for j in stock_parameters:
        if 'date' in j.lower():
            d = pd.to_datetime(x.info[j])
            if d is not None:
                l.append(d.strftime("%Y-%m-%d"))  # format date
        else:
            try:      # some parameters error
                l.append(x.info[j])
            except:   # ignore error and continue
                l.append("")
    yf_info[i] = l
    print('{}\t- financial information downloaded'.format(i))

print(yf_info)
yf_info.to_csv('/usr/local/airflow/result/result.csv')

