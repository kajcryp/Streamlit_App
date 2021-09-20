%%writefile streamlit_data_app.py
##Overiding app file with write function. You need to put it as the first line.

##python code for the app

import datetime
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import plotly.express as px

#import Streamlit_Manual_automated_Functions as maf



st.set_page_config(page_title="Data App - Simple", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")

product_groups = ['All Products', 'product 1', 'product 2', 'product 3', 'product 4', 'product 5']
#st.title('Data App - Simple')

# Sidebar Navigation
st.sidebar.title('Product Group')
options = st.sidebar.radio('Select a page:', product_groups)

sends = st.sidebar.slider("Deliveries determining an automated send: ",  min_value = 2, max_value = 10, value = 3)
st.sidebar.write('Sends:', sends)
#st.sidebar.slider("What year do you want to look at?",  min_value = 2019, max_value = 2028, value = 2021)

min_date = datetime.datetime(2021,1,1)
max_date = datetime.date(2021,12,31)

date = st.sidebar.date_input("Pick a date: (format YYYY/MM/DD)", (min_date, max_date))


###### These three variables are created so they can be used as parameters for the MAF import functions so they can create a csv file between relevant dates
start_date = date[0]
end_date = date[1]

no_auto_sends = sends

#### - Using variables above to create csv from MAF import - may need to comment out depending on data source
campaignCounts = maf.AllProductsCampaignCounts(start_date, end_date, no_auto_sends)
ProductRatio = maf.AllProducts(start_date, end_date, no_auto_sends)
Deliveries = maf.Campaign_Deliveries(start_date, end_date, no_auto_sends)      # CSV of deliveries of each automated campaign 


#Reading the csv and bringing it through as dataframes
df = pd.read_csv("manual_auto_ratio_final.csv")

df2 = pd.read_csv('campaign_counts_final.csv')

df3 = pd.read_csv('campaign_deliveries_final.csv')

### Using this function to provide campaign counts with only specific columns and not whole dataframe
def CampaignCountsTotal(product, automated_status):
    
    lx = df2[['automated_projects', 'total_broadcast_sends', 'product_group', 'automated_status']] 
    #brings through only some of the columns of the data
    
    class_23 = lx[(lx["product_group"] == product) & (lx["automated_status"] == automated_status)] 
    #filters the dataframe by product and automated status and uses parameters you put into function
    
    z = class_23.groupby(["automated_projects", "product_group"])['total_broadcast_sends'].sum().head(50) 
    #groups by the data by broadcast_sends
    
    end = z.reset_index().sort_values(by='total_broadcast_sends', ascending=False, na_position='first')  
    #resets z to a dataframe and sorts values by descending values
    
    result = end[['automated_projects', 'total_broadcast_sends']]
    
    return result


def CampaignDeliveries(product, automated_campaign):
    
    delivery_table = df3[(df3.product_group == product) & (df3.automated_projects == automated_campaign)]
    
    list_of_automated_projects = delivery_table['automated_projects'].tolist()
    
    if automated_campaign in list_of_automated_projects:
        
        output1 = delivery_table[['automated_projects', 'delivery_label', 'delivery_channel', 'campaign_code', 'total_sends']]  
        result = output1.groupby(['delivery_label', 'campaign_code','delivery_channel']).sum().sort_values(by=['total_sends', 'delivery_channel'], ascending=False, na_position='first')
               
        return result
    
    else:
        st.write("No campaign found")
    

### for Loop is used to bring through all the data for each product group highlighted at the top of the script 
for product in product_groups:    
    if (product == options) & (options == 'All Products'):
        st.title('Data App - All Products')
        
        plt.style.use('seaborn')
        #Ploting the ratio of sends graph on main page
        fig = plt.figure(figsize=(22,8))
        
               
        plt.title('Ratio of Manual to Automated Campaigns')
        plt.xlabel('Month')
        plt.ylabel('Send Ratio')
        plot = sns.lineplot(x='month_of_send', y='manual_automated_ratio', hue = 'product_group', data=df)
        
        # label points on the plot
        for x, y in zip(df['month_of_send'], df['manual_automated_ratio']):
                
             # the position of the data label relative to the data point can be adjusted by adding/subtracting a value from the x &/ y coordinates
             plt.text(x = x, # x-coordinate position of data label
                      y = y-0.5, # y-coordinate position of data label, adjusted to be 150 below the data point
                      s = '{:.2f}'.format(y) #, # data label, formatted to ignore decimals
                      #color = ‘purple’ # set colour of line
                     )         
        
        st.pyplot(fig) #this is how you how to render your plots on streamlit
        
        data_table = st.beta_expander("Data Table - (Click here to expand!)", expanded = False)
        
        with data_table:
            #Showing the data table
            st.table(df.sort_values(by=['month_of_send', 'product_group'], ascending=True, na_position='first'))
                    
    elif (product == options) & (options!= 'All Products'):
        st.title('Data App - ' + product)
        
        productdf = df[df["product_group"] == product].sort_values(by='month_of_send', ascending=True, na_position='first')    #filters dataframe by product
        st.table(productdf)
        
        Countsdf = CampaignCountsTotal(product, 'Automated')
        
        fig, ax = plt.subplots()
        Countsdf.sort_values('total_broadcast_sends').plot.barh(y='total_broadcast_sends', x = 'automated_projects', figsize =(20,11), ax=ax)
        plt.title('Sends for Automated Campaigns')
        plt.xlabel('Broadcast Sends')
        
        # label each bar in barplot
        for p in ax.patches:
            height = p.get_height() # height of each horizontal bar is the same
            width = p.get_width() # width (average number of passengers)
            
            # adding text to each bar
            ax.text(x = width+1, # x-coordinate position of data label, padded 3 to right of bar
                    y = p.get_y()+(height/2), # # y-coordinate position of data label, padded to be in the middle of the bar
                    s = '{:.0f}'.format(width), # data label, formatted to ignore decimals
                    va = 'center' # sets vertical alignment (va) to center
                   ) 
        
        st.pyplot(fig)
        

        #col2.image(grayscale, use_column_width=True)
        sentence = st.text_input('Input campaign name to find the: (campaign deliveries, campaign code and delivery channel)')

        sentence_search = st.button("Search Deliveries:")
        close_delivery_button = st.button("Close Deliveries")
        
        if sentence_search:
            Delivery_table = CampaignDeliveries(product, sentence)
            st.table(Delivery_table)
        elif close_delivery_button:
            pass
        
        row3_space1, col1, row3_space2, col2, row3_space3 = st.beta_columns((.1, 1, .5, 1, .1))  #Setting layout of the app
        #col1, col2 = st.beta_columns(2)
        
        with col1:
            col1.header("Automated Campaigns:")
            
            Countsdf = CampaignCountsTotal(product, 'Automated')
            groupby_tableA = Countsdf.groupby('automated_projects').sum().sort_values(by=['total_broadcast_sends'], ascending=False, na_position='first')
            st.table(groupby_tableA)

            
        #col1.image(original, use_column_width=True)
        
        
        with col2:
            col2.header("Manual Campaigns/Deliveries:")

            CountsdfManual = CampaignCountsTotal(product, 'Manual')
            groupby_tableM = CountsdfManual.groupby('automated_projects').sum().sort_values(by='total_broadcast_sends', ascending=False, na_position='first')
            st.table(groupby_tableM)

            

        #Countsdf = CampaignCountsTotal(product, 'Automated')
        #Countsdf
    
    else:
        pass
