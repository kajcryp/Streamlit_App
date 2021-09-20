import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sql_download as rs


   
#Function to show ratio of campaigns for with no filters.
def AllProducts(start_date, end_date, send_for_automated):


##   start_date:  This is to show you the start date for 
##   send_for_automated:  How many sends are you classifying for a campaign to be automated
    
    #residence_country = UKorInt(country)


    RSconn, cur = rs.get_connection(user='app_sgmk_datascience')
    
    performance_params = {'@start_date' : start_date,
                          '@end_date' : end_date,     
                          '@send_for_automated' : send_for_automated
                          }
    
    df = rs.execute_sql(RSconn=RSconn, sql='Campaign_Ratio_Automated_Manual.sql', params = performance_params, input_type='file')
    
    cur.close()
    RSconn.close()
    
    df.to_csv('AllProducts.csv', index = False)

    x = df.groupby('month_of_send').head(100).sort_values(by='month_of_send', ascending=True, na_position='first')
    x.to_csv('manual_auto_ratio_final.csv', index = False)




#Function to show ratio of campaigns for with no filters.
def AllProductsCampaignCounts(start_date, end_date, send_for_automated):


##   start_date:  This is to show you the start date for 
##   send_for_automated:  How many sends are you classifying for a campaign to be automated
    
    #residence_country = UKorInt(country)


    RSconn, cur = rs.get_connection(user='app_sgmk_datascience')
    
    performance_params = {'@start_date' : start_date,
                          '@end_date' : end_date,     
                          '@send_for_automated' : send_for_automated
                          }
    
    df = rs.execute_sql(RSconn=RSconn, sql='Campaign_Counts.sql', params = performance_params, input_type='file')
    
    cur.close()
    RSconn.close()
    
    #x = df[['automated_projects', 'total_broadcast_sends', 'product_group']]
    x = df
    x.to_csv('Campaign_counts_final.csv', index = False)



def Campaign_Deliveries(start_date, end_date, send_for_automated):


##   start_date:  This is to show you the start date for 
##   send_for_automated:  How many sends are you classifying for a campaign to be automated
    
    #residence_country = UKorInt(country)


    RSconn, cur = rs.get_connection(user='app_sgmk_datascience')
    
    performance_params = {'@start_date' : start_date,
                          '@end_date' : end_date,     
                          '@send_for_automated' : send_for_automated
                          }
    
    df = rs.execute_sql(RSconn=RSconn, sql='Campaign_Templates.sql', params = performance_params, input_type='file')
    
    cur.close()
    RSconn.close()
    
    #x = df[['automated_projects', 'total_broadcast_sends', 'product_group']]
    x = df
    x.to_csv('Campaign_Deliveries_final.csv', index = False)

    