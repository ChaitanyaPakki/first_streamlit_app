import streamlit
import pandas
import requests

streamlit.title("My Mom's new Healthy Diner")

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# to read the CSV file from S3 bucket
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

# setting Fruit name as index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Multiselect option on fruits and pre populating list to set an example
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the file content on the streamlit app as a table
streamlit.dataframe(fruits_to_show)

#Section to display API response
streamlit.header('Fruityvice Fruit Advice!')

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#streamlit.text(fruityvice_response.json())

#normalising JSON version of data
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#output the response as table
streamlit.dataframe(fruityvice_normalized)
