
# coding: utf-8

# # Summary
# 
# This document reads the data and computes several simple metrics using datasets provided in the exercise.  It also exports pre-processed dataset to several formats for subsequent data visualization. Finally, it discusses churn rate for users.
# 
# ***
# 
# 

# In[97]:

import pandas as pd
import matplotlib.pyplot as plt
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Let's read some transaction data

file = 'Downloads/2017-07_sr_data_analyst_task_(1)/transactions.csv'

transactions = pd.read_csv(file)
transactions['date'] = pd.to_datetime(transactions['date'])
transactions.index = transactions['date']

transactions.head()
transactions.info()

# Just some descriptive stats

transactions.describe()


# # KPI 1: Average number of transactions per client in 2016

# In[98]:

transactions.groupby('user_id')['type'].count().mean()


# # KPI 2:  Monthly volume of transactions

# In[99]:

volume = transactions.resample('M').type.count()
volume


# There is a marked seasonal trend in terms of number user transactions with winter months having a higher volume.

# In[100]:

my_plot = volume.plot(kind='line', title='Monthly Volume of Transactions')
my_plot.set_ylabel("Transactions")
my_plot.set_xlabel("Month")
plt.style.use('fivethirtyeight')
plt.show()


# # KPI 3: Growth rate in customer transactions

# Let's examine the growth in the number of transaction at the beginning of the year and the total (cumulatative) number of transaction for the year.

# In[101]:

beginning = volume["2016-01-31"]
end = volume.sum()


# In[102]:

float(end)/beginning*100


# In[103]:

volume.cumsum().plot(title= "Cumulatative Volume\n of Transactions: 2016")
plt.show()


# # KPI 4: Most common type of transactions

# We can now examine the most common type of transation. For this, we will import data dictionary containing the detailed 
# description of each transaction.

# In[104]:

# let's add data dictionary to get transactions type

file = 'Downloads/2017-07_sr_data_analyst_task_(1)/transaction_types.csv'
type_trans = pd.read_csv(file)
type_trans.head()

type_trans.columns.values

# Looks like there's some empty space in the column name, which we should remove

type_trans = type_trans.rename(columns=lambda x: x.strip())


# In[105]:

combined = pd.merge(transactions,type_trans,how="left",left_on="type",right_on="type")
combined['explanation'].value_counts().idxmax()


# It appears that _Credit Transfers_ was the most common type of transaction in 2016. Let's create a simple bar plot to examine this information visually and a larger context. The output below provides more detailed information by transaction type.

# In[106]:

combined.groupby('explanation')['explanation'].count().plot(kind = 'bar', title="Transaction Volume\n by Type of Transaction: 2016")
plt.show()


# In[107]:

combined.groupby('explanation')['explanation'].count()


# In[108]:

file = 'Downloads/2017-07_sr_data_analyst_task_(1)/users.csv'
user = pd.read_csv(file)
user.describe()


# # KPI 5: Growth in the New User Registrations

# Let's examine number of new signups in the first two months of 2016 and the growth between two time periods.

# In[109]:

user['sign_up'] = pd.to_datetime(user['sign_up'])
user.index = user['sign_up']
users = user.resample('M').user_id.count()
users


# The number of new registrations in February is much lower when compared to January. However, if we compare beginning of the year versus cumulatative total, there's a clear growth. 

# In[110]:

User_beginning = users["2016-01-31"]
User_end = users.sum()
float(User_end)/User_beginning*100


# #  Other KPIs:
# 
# ### Percent of users with KYC initiated

# In[111]:

float(user.kyc_initiated.count())/user.sign_up.count()*100


# ### Percent passing KYC

# In[112]:

float(user.kyc_completed.count())/user.kyc_initiated.count()*100


# # File Export
# 
# ***
# 
# Using pandas  to_csv  and  to_json methods to export to a different formats.

# In[113]:

to_export = combined.groupby('explanation')['type'].count().to_frame()
to_export.reset_index(level=1)
to_export.to_csv('export.csv')


# Just an example of how to export to json. This can be copied and pasted directly into html file or loaded externally.

# In[114]:

toexport = to_export.reset_index()
toexport.to_json(orient='records').replace('},{', '} {')


# # Churn Rate
# 
# ***
# 

# The _churn rate_ can be defined as a percentage of users/clients who terminate or discontinue using services offered by N26 within established time frame typically a year. To calculate the churn rate we would need to get a datafile containing number of users who stopped using N26 and divide it by the total number of _active users_. The _users.csv_ can be used to calculate denominator; datafile for numerator is not provided in this exercise.
# 
# Churn rate is an important metric since it relates to the number of customers, ability to provide loans and the overall financial stability of the given bank. Churn rate can provide key insights into why customer leave the institution, their level of satisfaction, and their overall level of interaction with the bank. Finally, it also poses questions related to retention strategies.
