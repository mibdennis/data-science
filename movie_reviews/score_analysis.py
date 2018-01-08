
# coding: utf-8

# In[1]:


import pandas as pd

movies = pd.read_csv("fandango_score_comparison.csv")
movies


# In[5]:


import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

plt.hist(movies["Metacritic_norm_round"])
plt.show()
plt.hist(movies["Fandango_Stars"])
plt.show()


# the Metacritic scores are much more diverse, while the scores from Fandango are concentrated betwen 3.0 to 5.0, which are generally higher than Metacritic.

# In[12]:


import numpy as np
fd_mean = movies['Fandango_Stars'].mean()
fd_median = np.median(movies['Fandango_Stars'])
mt_mean = movies['Metacritic_norm_round'].mean()
mt_median = np.median(movies['Metacritic_norm_round'])
fd_st = np.std(movies['Fandango_Stars'])
mt_st = np.std(movies['Metacritic_norm_round'])
print("fandango mean", fd_mean)
print(fd_median)
print(mt_mean)
print(mt_median)
print(fd_st)
print(mt_st)


# Scores on Metacritic are given by professional movie critics, and the score range is much more diverse than the scores on Fandango which are pro to high scores.

# From the data analysis results, the normalized mean of Metacritic is slightly lower than the normalized median, while the mean on Fandango is higher than the median. It means more scores are under the mean score in Fandango, while the opposite it true for Metacritic. 
# The the same time, lower standard deviation means a narrower variation of the score distribution around the mean. Therefore, the score variation is more moderate on Fandango, which is in line with our observation from the visualization.

# In[22]:


movies['fm_diff'] = np.absolute(movies['Metacritic_norm_round'] - movies['Fandango_Stars'])


# In[24]:


movies.sort_values(by = ['fm_diff'], ascending = False)


# In[28]:


from scipy.stats import pearsonr
r_value, p_value = pearsonr(movies['Fandango_Stars'],movies['Metacritic_norm_round'])
print(r_value)


# The r value is merely about 0.18, which means the correlation between the Fandango stars and Metacritic scores are not obvious.

# In[44]:


from scipy.stats import linregress
slope, intercept, r_value, p_value, stderr_slope  = linregress(movies['Metacritic_norm_round'],movies['Fandango_Stars'])


# In[46]:


predict_three = 3*slope+intercept
predict_one = 1*slope+intercept
predict_five = 5*slope+intercept
print(predict_three)
print(predict_one)
print(predict_five)


# In[47]:


plt.scatter(movies["Metacritic_norm_round"], movies["Fandango_Stars"])
plt.plot([1,5],[predict_one,predict_five])
plt.xlim(1,5)
plt.show()

