description = "Dynamic Plotting"

# Your app goes in the function run()
def run():
  import streamlit as st
  import time
  import random
  import plotly.express as px
  import pandas as pd

  placeholder = st.empty()
  start_button = st.empty()

  def radar_chart():
    df = pd.DataFrame(dict(
    r=[random.randint(0,22),
       random.randint(0,22),
       random.randint(0,22),
       random.randint(0,22),
       random.randint(0,22)],
    theta=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    placeholder.write(fig)

  if start_button.button('Start',key='start'):
    start_button.empty()
    if st.button('Stop',key='stop'):
        pass
    while True:
        radar_chart()
        time.sleep(0.5)

# end of app

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
