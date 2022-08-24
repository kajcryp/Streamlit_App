# Streamlit App
A data web application that was built to show campaign history.

# PostgreSQL Scripts
 Campaign_Counts_All.sql 
- This script brings through the number of sends for each campaign and helps determine which sends are automated and what are manual
 
 Campaign_Templates.sql  
- This script builds upon Campaign_Counts_All and looks to find what the delivery templates are for each automated campaign
 
 Campaign_Ratio_Automated_Manual.sql 
- This script builds upon Campaign_Counts_All and looks to find the % of campaigns that automated over time

# Python Scripts
 Streamlit_Campaign_Management_data_app.py
- This script is the data app
 
 Streamlit_Manual_automated_Functions.py  
- This script looks to run SQL scripts and download it into CSVs
