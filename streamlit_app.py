import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

# creating a function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
#Section to display API response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit you would love to know about?', 'Kiwi')
  if not fruit_choice:
    streamlit.error("Please select to get fruit information")
  else:
    return_from_fuction = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(return_from_fuction)
except URLError as e:
  streamlit.error()

streamlit.text("View our Fruit List - Add Your Favourites!")
#Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Select * From FRUIT_LOAD_LIST")
    return my_cur.fetchall()

#adding button to load fruits
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#allow end user to add fruits to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
    return "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input('What fruit you would love to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  return_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(return_from_function)

