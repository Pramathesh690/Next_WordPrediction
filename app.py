import streamlit as st
import numpy as np 
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessin.sequence import pad_sequence

## Load the LSTM Model 
model = load_model('next_word_lstm.h5')


# Load the tokenizer 

with open('tokenizer.pickle','rb') as handle:
    tokenizer = pickle.load(handle)

## Function to predict the next word 
def predict_next_word(model,tokenizer , text , max_sequence_len):
  token_list = tokenizer.texts_to_sequences([text])[0]
  if len(token_list) >= max_sequence_len:
    token_list = token_list[-(max_sequence_len-1):]
  token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
  predicted = model.predict(token_list,verbose = 0)
  predicted = model.predict(token_list , verbose = 0 )
  predicted_word_index = np.argmax(predicted)
  for word , index in tokenizer.word_index.items():
    if index == predicted_word_index:
      return word
  return None


## Streamlit app 
st.title("Next Word Prediction with LSTM and Early Stopping")
input_text = st.text_input("Enter the sequence of words","To be or not to")

if st.button("Predict next word"):
  max_sequence_len = model.input_shape[1] + 1 
  next_word = predict_next_word(model, tokenizer, input_text , max_sequence_len)
  st.write(f"Next word: {next_word}")