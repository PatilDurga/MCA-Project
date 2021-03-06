

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

start = '2010-01-01'
end = '2020-12-31'

st.title('Stock Price Trend Prediction ')

#take i/p from user 
user_input = st.text_input('Enter Stock Ticker','AAPL')

df=data.DataReader(user_input,'yahoo',start,end)

#Describing data for user
st.subheader('Data from 2010 - 2020')
st.write(df.describe())

#visualizations
st.subheader('Closing Price vs Time Chart ')
fig = plt.figure(figsize = (12,6))
plt.plot(df.close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = df.close.rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100 , 'r')
plt.plot(df.close , 'b')
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
ma100 = df.close.rolling(100).mean()
ma200 = df.close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100, 'b')
plt.plot(ma200 , 'g')
plt.plot(df.close , 'r')
st.pyplot(fig)

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70) : int(len(df))])

#we scale data coz we need to feet it into our LSTM model i.e keras 
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))


data_training_array = scaler.fit_transform(data_training)

#load model 
model = load_model('keras_model.h5')

#predictions (testing part)

past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing , ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100 , input_data.shape[0]):
    x_test.append(input_data[i-100 : i])
    y_test.append(input_data[i , 0])

x_test , y_test = np.array(x_test) , np.array(y_test)

y_pred= model.predict(x_test)

scaler = scaler.scale_

scale_fact = 1/scaler[0]
y_pred = y_pred * scale_fact
y_test = y_test * scale_fact


#Final Graph 
st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize= (12,6))
plt.plot(y_test , 'b' , label = 'Original Price')
plt.plot(y_pred , 'r' , label = 'Predicted Price')
plt.xlabel('TIME')
plt.ylabel('PRICE')
plt.legend()
st.pyplot(fig2)



