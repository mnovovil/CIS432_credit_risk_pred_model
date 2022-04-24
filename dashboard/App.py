
import streamlit as st

from Dashboard import Dashboard
from Pages import Home, DataAnalysis, LogReg	

dashboard = Dashboard()

dashboard.Add_Page("Home", Home.page)
dashboard.Add_Page("Data Analysis", DataAnalysis.page)
dashboard.Add_Page("Logistic Regression Model", LogReg.page)

dashboard.run()