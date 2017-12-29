
# coding: utf-8

# In[2]:


import pandas
data = pandas.read_csv("~/Desktop/dataquest/thanksgiving.csv", encoding="Latin-1")
print(data.head)


# In[10]:


print(data.columns)


# In[14]:


data['Do you celebrate Thanksgiving?'].value_counts() #difference w/o paranthesis?


# In[15]:


data = data[data['Do you celebrate Thanksgiving?']=='Yes']


# In[16]:


data['What is typically the main dish at your Thanksgiving dinner?'].value_counts()


# In[19]:


tofurkey = data[data['What is typically the main dish at your Thanksgiving dinner?']=='Tofurkey']


# In[20]:


print(tofurkey['Do you typically have gravy?'])


# In[21]:


apple_isnull = pandas.isnull(data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple'])
pumpkin_isnull = pandas.isnull(data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin'])
pecan_isnull = pandas.isnull(data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan'])


# In[22]:


ate_pies = apple_isnull & pumpkin_isnull & pecan_isnull


# In[25]:


print(ate_pies.value_counts())


# In[42]:


def ext_int(age_str):
    if pandas.isnull(age_str):
        return None
    age_str = age_str.split(" ")[0]
    age_str = age_str.replace("+","")
    return int(age_str)


# In[46]:


data['int_age']=data['Age'].apply(ext_int)
data['int_age'].describe()


# We need to be cautious about the shortcomings of the result due to the following reasons:
#     1. The first year of each age range is use to replace the actual age of a sample, which leads to inacurracy of age counts;
#     2. Some rows missing age record are deleted;
# Therefore, it is not a complete true depiction of the ages of survey participants.

# In[56]:


def str_int(inc_str):
    if pandas.isnull(inc_str):
        return None
    inc_str = inc_str.split(" ")[0]
    if inc_str == 'Prefer':
        return None
    inc_str=inc_str.replace('$','')
    inc_str=inc_str.replace(',','')
    return int(inc_str)
        


# In[58]:


data['int_income']=data['How much total combined money did all members of your HOUSEHOLD earn last year?'].apply(str_int)
data['int_income'].describe()


# We only have a rough approximation of the income. Besides, it skews downward as we use the threshold number of each income range to represent all the incomes within this range. 

# In[59]:


low_inc = data[data['int_income'] < 150000]
low_inc['How far will you travel for Thanksgiving?'].value_counts()


# In[60]:


high_inc = data[data['int_income'] > 150000]
high_inc['How far will you travel for Thanksgiving?'].value_counts()


# In both high income and low income range, people who don't travel at all are more than people in different types of traveling, according to our finding. 

# In[62]:


data.pivot_table(index='Have you ever tried to meet up with hometown friends on Thanksgiving night?',columns='Have you ever attended a "Friendsgiving?"',values='int_age')


# In[65]:


data.pivot_table(index='Have you ever tried to meet up with hometown friends on Thanksgiving night?',columns='Have you ever attended a "Friendsgiving?"',values='int_income')


# People who tried to meet up with hometown friends tend to be elder and acquire higher income than people who ever attended a "Friendsgiving". People who did not attend neither activities have the highest income and with the eldest average age, while people who attended both activities are with the youngest average age and have the lowest income. Therefore, We could not reject our hypothesis according to our findings.
