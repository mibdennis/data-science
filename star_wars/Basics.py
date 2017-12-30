
# coding: utf-8

# In[41]:


import pandas as pd
star_wars = pd.read_csv("star_wars.csv", encoding="ISO-8859-1")


# In[42]:


star_wars = star_wars[pd.notnull(star_wars["RespondentID"])]


# In[43]:


yes_no = {"Yes": True, "No": False}

for col in [
    "Have you seen any of the 6 films in the Star Wars franchise?",
    "Do you consider yourself to be a fan of the Star Wars film franchise?"
    ]:
    star_wars[col] = star_wars[col].map(yes_no)

star_wars.head()


# In[44]:


import numpy as np

movie_mapping = {
    "Star Wars: Episode I  The Phantom Menace": True,
    np.nan: False,
    "Star Wars: Episode II  Attack of the Clones": True,
    "Star Wars: Episode III  Revenge of the Sith": True,
    "Star Wars: Episode IV  A New Hope": True,
    "Star Wars: Episode V The Empire Strikes Back": True,
    "Star Wars: Episode VI Return of the Jedi": True
}

for col in star_wars.columns[3:9]:
    star_wars[col] = star_wars[col].map(movie_mapping)

star_wars.head()


# In[45]:


star_wars=star_wars.rename(columns={
    "Which of the following Star Wars films have you seen? Please select all that apply.": "seen_1",
    "Unnamed: 4":"seen_2",
    "Unnamed: 5":"seen_3",
    "Unnamed: 6":"seen_4",
    "Unnamed: 7":"seen_5",
    "Unnamed: 8":"seen_6"
})
star_wars.head()


# In[46]:


star_wars[star_wars.columns[9:15]]=star_wars[star_wars.columns[9:15]].astype(float)


# In[47]:


star_wars=star_wars.rename(
columns={"Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.":"ranking_1",
         "Unnamed: 10":"ranking_2",
         "Unnamed: 11":"ranking_3",
         "Unnamed: 12":"ranking_4",
         "Unnamed: 13":"ranking_5",
         "Unnamed: 14":"ranking_6"
})


# In[48]:


star_wars[star_wars.columns[9:15]].mean()


# In[49]:


from matplotlib import pyplot as plt
get_ipython().magic('matplotlib inline')

plt.bar(range(6),star_wars[star_wars.columns[9:15]].mean())


# According to the bar plot, the fourth movie of the franchise gets the highest ranking, while the 3rd one, which is also the latest one, has the lowest ranking. Generally, the older triology gets higher scores than the newer one.

# In[51]:


star_wars[star_wars.columns[3:9]].sum()


# In[52]:


plt.bar(range(6),star_wars[star_wars.columns[3:9]].sum())


# The elder triology generally has been watched more than the newer one, at least within the sample group. 

# In[61]:


fan = star_wars[star_wars["Do you consider yourself to be a fan of the Star Wars film franchise?"]==True]
non_fan = star_wars[star_wars["Do you consider yourself to be a fan of the Star Wars film franchise?"]==False]


# In[66]:


plt.bar(range(6),fan[fan.columns[9:15]].mean())


# In[67]:


plt.bar(range(6),non_fan[non_fan.columns[9:15]].mean())


# There is an interesting comparison between the Star Wars fans and non-fans regarding the ratings of the six movies. For Star Wars fans, the old triology generally rank much higher than the new triology. While for non-fan audience, there is no obvious difference between the ratings of the two triologies. However, the fifth movie is rated as the highest among the six movies within both groups.

# In[70]:


plt.bar(range(6),fan[fan.columns[3:9]].sum())


# In[71]:


plt.bar(range(6),non_fan[non_fan.columns[3:9]].sum())


# There is also a huge difference on the total exposure of the movies between the two groups. While the franchise movies are almost equally seen by the fan group, the old triology has a higher exposure within the non-fan group. The last two movies of the franchise have highest exposure overall.

# In[72]:


star_wars['Education'].value_counts()


# In[79]:


college=star_wars[star_wars['Education']=='Some college or Associate degree']
bachelor=star_wars[star_wars['Education']=='Bachelor degree']
graduate=star_wars[star_wars['Education']=='Graduate degree']
high=star_wars[star_wars['Education']=='High school degree']


# In[80]:


plt.bar(range(6),college[college.columns[9:15]].mean())


# In[81]:


plt.bar(range(6),graduate[graduate.columns[9:15]].mean())


# In[83]:


plt.bar(range(6),bachelor[bachelor.columns[9:15]].mean())


# In[84]:


plt.bar(range(6),high[high.columns[9:15]].mean())


# In[85]:


star_wars['Unnamed: 16'].value_counts()


# In[110]:


star_wars=star_wars.rename(
columns={
    "Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.":"Han Solo",
    "Unnamed: 16":"Luke Skywalker",
    "Unnamed: 17":"Princess Leia Organa",
    "Unnamed: 18":"Anakin Skywalker",
    "Unnamed: 19":"Obi Wan Kenobi",
    "Unnamed: 20":"Emperor Palpatine",
    "Unnamed: 21":"Darth Vader",
    "Unnamed: 22":"Lando Calrissian",
    "Unnamed: 23":"Boba Fett",
    "Unnamed: 24":"C-3P0",
    "Unnamed: 25":"R2 D2",
    "Unnamed: 26":"Jar Jar Binks",
    "Unnamed: 27":"Padme Amidala",
    "Unnamed: 28":"Yoda",
}
)


# In[111]:


favorite_mapping = {
    "Very favorably ": 3,
    "Somewhat favorably": 2,
    "Neither favorably nor unfavorably (neutral)": 1,
    "Somewhat unfavorably ": -1,
    "Very unfavorably": -2,
    "Unfamiliar (N/A)": 0
}

for col in star_wars.columns[15:29]:
    star_wars[col] = star_wars[col].map(favorite_mapping)


# In[112]:


plt.bar(range(14),star_wars[star_wars.columns[15:29]].sum())

