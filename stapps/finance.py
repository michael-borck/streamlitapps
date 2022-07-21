description = "Financial Dashboard"

# Your app goes in the function run()
def run():
    # !pip install streamlit
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import yfinance as yf # https://pypi.org/project/yfinance/
    from ta.volatility import BollingerBands
    from ta.trend import MACD
    from ta.momentum import RSIIndicator

    ##################
    # Set up sidebar #
    ##################

    # Add in location to select image.

    option = st.selectbox('Select one symbol', ( 'AAPL', 'MSFT',"SPY",'WMT','NMT.AX'))


    import datetime

    today = datetime.date.today()
    before = today - datetime.timedelta(days=700)
    start_date = st.date_input('Start date', before)
    end_date = st.date_input('End date', today)
    if start_date > end_date:
        st.error('Error: End date must fall after start date.')


    ##############
    # Stock data #
    ##############

    # https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#momentum-indicators

    df = yf.download(option,start= start_date,end= end_date, progress=False)

    indicator_bb = BollingerBands(df['Close'])

    bb = df
    bb['bb_h'] = indicator_bb.bollinger_hband()
    bb['bb_l'] = indicator_bb.bollinger_lband()
    bb = bb[['Close','bb_h','bb_l']]

    macd = MACD(df['Close']).macd()

    rsi = RSIIndicator(df['Close']).rsi()


    ###################
    # Set up main app #
    ###################

    st.write('Stock Bollinger Bands')

    st.line_chart(bb)

    progress_bar = st.progress(0)

    # https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

    st.write('Stock Moving Average Convergence Divergence (MACD)')
    st.area_chart(macd)

    st.write('Stock RSI ')
    st.line_chart(rsi)


    st.write('Recent data ')
    st.dataframe(df.tail(10))


# end of app

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
