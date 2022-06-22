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
  
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contain")
streamlit.dataframe(my_data_row)

fruit_choice = streamlit.text_input('What fruit you would love to add?')
#allow end user to add fruits to the list

streamlit.write('Thanks for adding', fruit_choice)

my_cur.execute("insert into fruit_load_list values('from streamlit')")
