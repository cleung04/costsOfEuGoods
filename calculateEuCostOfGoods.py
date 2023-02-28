#this script calculates based on VAT refund rates at customs. VAT rate is 22% but nearly half of this is not refunded 
#to a foreign national purchasing goods in EU states

#import pandas
import pandas as pd
#import numpy
import numpy as np

#read excel sheet
data=pd.read_excel('goodsCosts.xlsx')

#for testing
#print content of excel sheet
data

#import excel data into a dataframe
df = pd.DataFrame(data, columns=['Receipt', 'Item', 'Cost', 'Person'])

#total of receipt amounts  
dff = df.groupby(["Receipt"]).Cost.sum().reset_index()

#Using Numpy.Select to Set Values Using Multiple Conditions
#assign VAT refund % based on total balance on receipt to the third decimal place
dff["RefundVAT"] = .121
dff['RefundVAT'] = np.where(dff["Cost"] < 3000, .109, dff['RefundVAT'])

#Add New Column by merging two dataframes 
df = pd.merge(df,dff,on=['Receipt','Receipt'], how='left')

# Creating a column of actual cost of items after VAT refund 
df['costBeforeTax'] = (df['Cost_x'] - (df['Cost_x'] * df['RefundVAT']))

#assign euro to USD conversion rate to the second decimal place
df["euroToUsd"] = 1.07

# Creating a column of actual cost of items after conversion to USD
df['costInUSD'] = round(df['costBeforeTax'] * df['euroToUsd'],2)

#Sum actual cost of items in USD based on person
df2 = round(df.groupby('Person').sum(),2)
print(df2)

#remove all columns except names and totals 
df2 = df2.drop(df2.columns[[0,1,2,3,4,5]], axis=1)  # df.columns is zero-based pd.Index

# Display modified DataFrame
print("Total costs in USD after VAT refund for each person:")
print(df2)