import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import date
import numpy as np
from plotly import graph_objs as go
from stocknews import StockNews

st.markdown('Page 1')
st.sidebar.markdown('Page 1')
# Setting time constraint
start = '2018-01-01'
today = date.today().strftime('%Y-%m-%d')

# Adding title, sidebar, etc
st.title('Minimum Viable Product')

# List of available stocks
stocks = ['AAPL', 'MSFT', 'GME', 'F', 'TM', 'GOOG']
select_stocks = st.selectbox("Pick a Stock", stocks)

# Adding a benchmark
benchmark_symbol = '^GSPC'
benchmark_data = yf.download(benchmark_symbol, start=start, end=today)

@st.cache_resource
def load_data(ticker):
    data = yf.download(ticker, start=start, end=today)
    data.reset_index(inplace=True)
    return data

# Plotting the graph with percent change calculations
st.subheader('Price Movements')
data_load = load_data(select_stocks)
data2 = data_load.copy()
data2['% Change'] = data2['Close'] / data_load['Close'].shift(1) - 1
st.write(data2.tail())

# st.write(benchmark_data.tail())

# Adding benchmark data to compare
benchmark_data2 = benchmark_data.copy()
benchmark_data2['% Change'] = benchmark_data2['Close'] / benchmark_data2['Close'].shift(1) - 1

########### Annual Return
st.subheader('Annual Return')
annual_return = data2['% Change'].mean() * 252 * 100
st.write('Annual Return represents the percentage change in the investments value over a one-year period. In this context, it indicates that the investment has grown/shrunk by', round(annual_return, 2), '%', 'on an annual basis.')

########### Standard Deviation
st.subheader('Standard Deviation')
stdev = np.std(data2['% Change']) * np.sqrt(252)
st.write('Standard Deviation is a measure of the amount of variation or dispersion in a set of values. In the context of financial investments, a higher standard deviation indicates a higher level of risk or volatility. Here, ', round(stdev * 100, 2), '%', 'represents the degree of fluctuation in the investments returns.')

########### Risk Return
st.subheader('Risk Return')
st.write('Risk-Return Ratio, also known as the Sharpe Ratio, is a measure of the relationship between the risk (as measured by standard deviation) and the return of an investment. A ratio close to 1 suggests a balanced relationship between risk and return. In this case, a ratio of: ', round(annual_return / (stdev * 100), 2))

########## Plotting the data
def plot_raw_data(load_data, benchmark_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data2['Date'], y=data2['Close'], name=f'{select_stocks} Close'))
    # fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data['Close'], name=f'{benchmark_symbol} Close'))
    fig.update_layout(title_text='Time Series Data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data(data_load, benchmark_data)

st.markdown('Page 2')
st.sidebar.markdown('Page 2')
st.title('Financial Analysis')



benchmark_data['% Change'] = benchmark_data['Close'].pct_change()
bench_ret = benchmark_data['% Change']
bench_dev = (bench_ret + 1).cumprod()-1
# Adding a subplot for cumulative return
def plot_cumulative_return(stock_data, benchmark_data):
    fig = go.Figure()

    # Calculate cumulative return of the selected stock
    stock_data['Cumulative Return'] = (1 + stock_data['% Change']).cumprod() - 1

    # Calculate cumulative return of the benchmark
    benchmark_data['Cumulative Return'] = (1 + benchmark_data['% Change']).cumprod() - 1

    # Plotting cumulative return of the selected stock
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Cumulative Return'], name=f'{select_stocks} Cumulative Return'))

    # Plotting cumulative return of the benchmark
    fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data['Cumulative Return'], name=f'{benchmark_symbol} Cumulative Return'))

    fig.update_layout(title_text='Cumulative Return Comparison', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_cumulative_return(data2, benchmark_data2)


# Fetching the latest 5 news for the selected stock
st.header(f'News of {select_stocks}')
sn = StockNews(select_stocks)
df_news = sn.read_rss()
# Displaying the news in a loop
for i in range(10):
    st.subheader(f'News {i + 1}')
    st.write(f"Published: {df_news['published'][i]}")
    st.write(f"Title: {df_news['title'][i]}")
    st.write(f"Summary: {df_news['summary'][i]}")