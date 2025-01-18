# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    "**Choose the Fruit you want in your custom Smoothie!**"
)
cnx=st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name on Smoothie", "")
st.write("Name on your Smoothie will be ", name_on_order)


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


Ingredients_List = st.multiselect("Choose upto 5 Options",my_dataframe,max_selections=5)
if Ingredients_List:

    Ingredients_String=''
    for fruits in Ingredients_List:
        Ingredients_String += fruits + ' '
    st.write (Ingredients_String)

    my_insert_stmt=""" insert into smoothies.public.orders(ingredients,name_on_order) 
    values ('"""+Ingredients_String+"""','"""+name_on_order +"""')"""
    
    #st.write(my_insert_stmt)
    time_to_Order= st.button ('Submit_Order')
    if time_to_Order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!')

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json)
