import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

ticker="4901.T" #富士フィルムのティッカーシンボル

df=yf.download((ticker), start="2023-12-01", end="2025-12-31", interval="1d")
df = df[["Open", "High", "Low", "Close", "Volume"]]
#print(df.head())

df.columns = df.columns.droplevel(1)

# Volumeを削除
# Volume あり→df, Volume なし→df1
df1=df.drop("Volume",axis=1)

df1 = df1.dropna()
print(df1.dtypes)

# fig1 折れ線グラフ
plt.figure(figsize=(15,6))
plt.plot(df1.index, df1)
plt.legend()
plt.savefig("stock_price1.png")
#plt.show()

#fig2 ろうそく足グラフ　Volumeなし
mpf.plot(df1, type="candle", figratio=(15,5), savefig="stock_price2.png")
#plt.show()

# fig3 ろうそく足グラフ　Volumeつき
mpf.plot(df, type="candle", style="yahoo", figratio=(15,5), mav=3,savefig="stock_price3.png", volume=True)
#plt.show()

# fig4 移動平均線
df["MA30"]=df["Close"].rolling(window=30,min_periods=1).mean()
df_ma=df[["Close", "MA30"]]
plt.figure(figsize=(15,6))
plt.plot(df_ma.index, df_ma)
plt.legend()
plt.savefig("stock_price4.png")
#plt.show()

# fig5 ボリンジャーバンド
df["std30"]=df["Close"].rolling(window=30,min_periods=1).std()
df["upper_band"]=df["MA30"] + 2*df["std30"]
df["lower_band"]=df["MA30"] - 2*df["std30"]
plt.figure(figsize=(15,6))
plt.plot(df["Close"], color="blue", label="Close")
plt.plot(df["MA30"], color="orange", label="MA30")
plt.plot(df["upper_band"], color="red", label="Upper Band")
plt.plot(df["lower_band"], color="red", label="Lower Band")
plt.fill_between(df.index, df["lower_band"], df["upper_band"], color="red", alpha=0.3)

plt.legend()
plt.savefig("stock_price5.png")
plt.show()
