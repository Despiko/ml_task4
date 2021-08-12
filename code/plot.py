import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

symbols = ["AAPL", "^GSPC"]

yf_period = "20y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

yf_price = yf.download(
        tickers = symbols,       # tickers list or string as well
        period = yf_period,      # optional, default is '1mo'
        interval = yf_interval,  # fetch data by interval
        group_by = 'ticker',     # group by ticker
        auto_adjust = True,      # adjust all OHLC (open-high-low-close)
        prepost = True,          # download market hours data
        threads = True,          # threads for mass downloading
        proxy = None)

yf_price = yf_price.iloc[:, yf_price.columns.get_level_values(1) == 'Close']
yf_price = round(yf_price[symbols],2)   # change order of columns
yf_price.columns = yf_price.columns.droplevel(1)

yf_percent = round(yf_price[symbols].pct_change() * 100, 2)

yf_percent['YR-MTH'] = pd.to_datetime(yf_percent.index).strftime("%Y-%m")

perf_m = 24

# create dataframe
perf_mth = pd.DataFrame()
perf_mth['YR-MTH'] = yf_percent['YR-MTH'].sort_values().unique()


#  calculate returns
for x in symbols:
    perf_mth[x] = yf_percent[x].groupby(yf_percent['YR-MTH']).sum().values
    perf_mth[x] = round(perf_mth[x],2)


#  update dataframe to last "perf_m" years
perf_mth = perf_mth.tail(perf_m)

# col_name with max row_values
perf_mth['maxSYM'] = perf_mth[symbols].idxmax(axis=1)
perf_mth['max'] = perf_mth[symbols].max(axis=1)

#  performance for last 24 months (2 years)
perf_m = 24

df_plot = perf_mth[symbols].head(-1).tail(perf_m)
df_plot['YR-MTH'] = perf_mth['YR-MTH'].head(-1).tail(perf_m)

#  figure size
plt.figure(figsize=(10, 10))

#  subplot loop
sns.lineplot(x = df_plot['YR-MTH'], y = df_plot['AAPL'])
sns.lineplot(x = df_plot['YR-MTH'], y = df_plot['^GSPC'], color='gray',ls='--')
plt.legend(['AAPL','S&P500'],loc=2)  # top left
plt.title('AAPL vs S&P500 ({} months)'.format(perf_m), fontsize=14)
plt.xlabel('')
plt.ylabel('percent change')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()
plt.savefig('/usr/local/airflow/result/plot.png')
