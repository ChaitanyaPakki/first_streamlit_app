import streamlit
import pandas
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

# Multiselect option on fruits
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# display the file content on the streamlit app as a table
streamlit.dataframe(my_fruit_list)

