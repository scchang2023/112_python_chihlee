import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

value = st.slider("三角函式",min_value=0, max_value=10)
#t = np.arange(0.,1.0,0.05)
t = np.arange(0.,value,0.05)
#print(t)
#st.write(t)
y1 = np.sin(2 * np.pi * t)
y2 = np.cos(2 * np.pi * t)
#print(y1)
#print(y2)
#st.write(y1)
#st.write(y2)
figure1 = plt.figure(figsize=(8,4))
axes1 = figure1.add_subplot()
axes1.plot(y1)
axes1.plot(y2)
#plt.show()
st.write(figure1)