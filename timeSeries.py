import cryptocompare
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import argparse

parser = argparse.ArgumentParser(description="Time Series Decomposition for Crypto Prices")
parser.add_argument("SrcName", type=str, help="Source cryptocurrency symbol (e.g., BTC)")
parser.add_argument("DestName", type=str, help="Destination currency symbol (e.g., USD)")
parser.add_argument("TimeFrame", type=str, help="TimeFrame (e.g., W)")
args = parser.parse_args()

SrcName = args.SrcName
DestName = args.DestName
TimeFrame = args.TimeFrame

data = cryptocompare.get_historical_price_day(SrcName, currency=DestName) #, limit=2000
df = pd.DataFrame(data)
df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True)

monthly_data = df['close'].resample(TimeFrame).mean()

#decompose to tree main things
decomposition = seasonal_decompose(monthly_data, model='additive', period=12)

#split datas
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# assume sycle: Trend + Residual (without Seasonal)
cyclic = (trend + residual) - trend.mean()

fig, axes = plt.subplots(4, 1, figsize=(8, 8), sharex=True)

plt.suptitle(f"{SrcName} to {DestName} in {TimeFrame} timeFrame", fontsize=16)

monthly_data.plot(ax=axes[0], title='Observed (Primary Price)')
trend.plot(ax=axes[1], title='Trend (Long Time)')
seasonal.plot(ax=axes[2], title='Seasonality (Seasonality Patterns)')
residual.plot(ax=axes[3], title='Residual (Noises)')
# cyclic.plot(ax=axes[4], title='Cyclic (Cyclic Patterns)')

plt.tight_layout()
plt.show()