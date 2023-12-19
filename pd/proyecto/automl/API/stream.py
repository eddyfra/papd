import streamlit as st
import requests
import pandas as pd
import json


a = st.number_input('Insert number a', step=1)
b = st.number_input('Insert number b', step=1)
data = {'a':a, 'b':b}
# http://127.0.01:5000/ is from the flask api
if st.button("GET", type="primary"):
    response = requests.get("http://127.0.0.1:5000/mul/",params=data)
    print(response.json())
    data_table1 = pd.json_normalize(response.json())
    st.write(data_table1)
else:
    st.write('Goodbye')

st.write(data)