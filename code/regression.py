import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


apl = yf.Ticker('AAPL')
data = apl.history(period="Max")
data.reset_index(inplace=True)
data.columns = ['date','open','high','low','close','vol','divs','split']
data.drop(columns=['divs','split'])
data['date'] = pd.to_datetime(data.date)
x = data[['open', 'high', 'low', 'vol']]
y = data['close']
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.15,
                                                    shuffle=False, random_state=42)
regression = LinearRegression()
regression.fit(train_x, train_y)

predicted=regression.predict(test_x)
dfr=pd.DataFrame({'Actual_Price': test_y, 'Predicted_Price': predicted})

plt.plot(dfr.Actual_Price, color='black')
plt.plot(dfr.Predicted_Price, color='lightblue')
plt.title("AAPL prediction chart")
plt.legend()
plt.show()

plt.savefig('/usr/local/airflow/result/regression.png')
