# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    "**Choose the Fruit you want in your custom Smoothie!**"
)
cnx=st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name on Smoothie", "")
st.write("Name on your Smoothie will be ", name_on_order)


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
st.dataframe=(pd_df)
#st.stop

Ingredients_List = st.multiselect("Choose upto 5 Options",my_dataframe,max_selections=5)
if Ingredients_List:

    Ingredients_String=''
    for fruits in Ingredients_List:
        Ingredients_String += fruits + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits,' is ', search_on, '.')
        st.subheader(search_on+' Nutrition Value')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" +search_on)
        st.write("https://my.smoothiefroot.com/api/fruit/" +search_on)
        #sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        sf_df = pd.DataFrame(data=smoothiefroot_response.json())
        st.dataframe(sf_df, use_container_width=True)    
    st.write (Ingredients_String)

    my_insert_stmt=""" insert into smoothies.public.orders(ingredients,name_on_order) 
    values ('"""+Ingredients_String+"""','"""+name_on_order +"""')"""
    
    #st.write(my_insert_stmt)
    time_to_Order= st.button ('Submit_Order')
    if time_to_Order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!')
