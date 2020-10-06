import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.title('BBC Most Read Monitor')

st.write('There are some beans in my suitcase.')

x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x)
f = plt.figure(figsize=(7, 7))
plt.plot(x, y)
st.write(f)
