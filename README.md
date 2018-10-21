# SocialCops-Challenge
Repository containing the scripts for Challenge 1 of the Technical Round of the Intern Selection Process

To run the analyses, you can choose to use either the Jupyter notebooks or Python scripts:
(N.B CMO_MSP_Mandi.csv and Monthly_data_cmo.csv should both be placed in the same folder as the notebooks and scripts)

# Jupyter Notebooks (preferred) #

The instructions on how to run the individual cells are stated in the notebook. 

The notebooks should be run in the following order:

* Outlier_Elimination.ipynb  
  * outputs clean_monthly_data.csv (CSV file containing filtered data without outliers)

* Seasonality Detection.ipynb 
  * outputs seasonality_type.csv (CSV file containing the appropriate seasonality model for the different APMC time series)
  * outputs deseasonalised_data.csv (CSV file containting the deseasonalised time series for the different APMCs)

* Comparing MSP to Minimum Monthly Price.ipynb 
  * outputs msp_comparison.csv (CSV file with the mean difference between the minimum monthly price and the MSP for APMC with MSP values) 
  * outputs msp_too_high.csv (CSV file listing AMPCs for which the MSP value is too high)
  
* High Price Fluctuation.ipynb
  * outputs flagging_high_fluctuation.csv (CSV file listing the APMCs with the top 5% price fluctuations)
  
 # Python Files #

The scripts should be run in the following order:

* oulier_detection_and_filtering.py  
  * outputs clean_monthly_data.csv (CSV file containing filtered data without outliers)

* seasonal_decomposition.py 
  * outputs seasonality_type.csv (CSV file containing the appropriate seasonality model for the different APMC time series)
  * outputs deseasonalised_data.csv (CSV file containting the deseasonalised time series for the different APMCs)

* MSP_vs_monthly_min_price.py 
  * outputs msp_comparison.csv (CSV file with the mean difference between the minimum monthly price and the MSP for APMC with MSP values) 
  * outputs msp_too_high.csv (CSV file listing AMPCs for which the MSP value is too high)
  
* high_price_fluctuation.py
  * outputs flagging_high_fluctuation.csv (CSV file listing the APMCs with the top 5% price fluctuations)
  
  
  
  
  Stay tuned for the in-depth documentation! I will all be in the Wiki!
