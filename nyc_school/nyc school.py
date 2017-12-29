
# coding: utf-8

# In[153]:


import pandas as pd
graduation=pd.read_csv('~/Desktop/dataquest/school_data/2005-2010_Graduation_Outcomes_-_School_Level.csv')
ap_2010=pd.read_csv('~/Desktop/dataquest/school_data/2010__AP__College_Board__School_Level_Results.csv')
class_size=pd.read_csv('~/Desktop/dataquest/school_data/2010-2011_Class_Size_-_School-level_detail.csv')
demographics=pd.read_csv('~/Desktop/dataquest/school_data/2006_-_2012_School_Demographics_and_Accountability_Snapshot.csv')
hs_directory=pd.read_csv('~/Desktop/dataquest/school_data/2014_-_2015_DOE_High_School_Directory.csv')
sat_results=pd.read_csv('~/Desktop/dataquest/school_data/2012_SAT_Results.csv')


# In[154]:


data_files=[graduation,ap_2010,class_size,demographics,hs_directory,sat_results]
data={}
data['graduation']=graduation
data['ap_2010']=ap_2010
data['class_size']=class_size
data['demographics']=demographics
data['hs_directory']=hs_directory
data['sat_results']=sat_results


# In[155]:


print(data['sat_results'].head())


# In[156]:


for key in data:
    print(data[key].head())


# In[157]:


survey_all=pd.read_csv('~/Desktop/dataquest/school_data/survey_all.txt',delimiter='\t',encoding='windows-1252')
survey_d75=pd.read_csv('~/Desktop/dataquest/school_data/survey_d75.txt',delimiter='\t',encoding='windows-1252')
survey=pd.concat([survey_all,survey_d75],axis=0)
print(survey.head())


# In[158]:


survey['DBN']=survey['dbn']
survey_fields=["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]
survey=survey.loc[:,survey_fields]
data['survey']=survey
print(survey.head())


# In[159]:


data['hs_directory']['DBN']=data['hs_directory']['dbn']

def add_col(col):
    str_col=str(col)
    if len(str_col)>1:
        return str_col
    else:
        return str_col.zfill(2)
    
data['class_size']['padded_csd']=data['class_size']['CSD'].apply(add_col)
data['class_size']['DBN']=data['class_size']['padded_csd']+data['class_size']['SCHOOL CODE']
print(data['class_size'].head())


# In[160]:


cols=['SAT Math Avg. Score','SAT Critical Reading Avg. Score','SAT Writing Avg. Score']
for col in cols:
    data['sat_results'][col]=pd.to_numeric(data['sat_results'][col],errors='coerce'
)

data['sat_results']['sat_score']=data['sat_results'][cols[0]]+data['sat_results'][cols[1]]+data['sat_results'][cols[2]]
data['sat_results']['sat_score'].head()


# In[161]:


import re
def convert(str):
    coords = re.findall('\(.+\)',str)
    lat = coords[0].split(',')[0].replace('(','')
    return lat

data['hs_directory']['lat']=data['hs_directory']['Location 1'].apply(convert)
print(data['hs_directory']['lat'].head())


# In[162]:


def convert2(str):
    coords = re.findall('\(.+\)',str)
    lon = coords[0].split(',')[1].replace(')','')
    return lon

data['hs_directory']['lon']=data['hs_directory']['Location 1'].apply(convert2)
data['hs_directory']['lat']=pd.to_numeric(data['hs_directory']['lat'],errors='coerce')
data['hs_directory']['lon']=pd.to_numeric(data['hs_directory']['lon'],errors='coerce')
print(data['hs_directory'].head())


# In[163]:


class_size = data['class_size']
class_size=class_size[class_size['GRADE '] == '09-12']
class_size=class_size[class_size['PROGRAM TYPE'] == 'GEN ED']
print(class_size.head())


# In[164]:


import numpy as np
dbn=class_size.groupby('DBN')
class_size=dbn.agg(np.mean)

class_size.reset_index('DBN',inplace=True)
data['class_size']=class_size
print(data['class_size'].head())


# In[165]:


data['demographics']=data['demographics'][data['demographics']['schoolyear']==20112012]
print(data['demographics'].head())


# In[166]:


data['graduation']=data['graduation'][data['graduation']['Cohort']=='2006']
data['graduation']=data['graduation'][data['graduation']['Demographic']=='Total Cohort']
print(data['graduation'].head())


# In[167]:


cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']
for col in cols:
    data['ap_2010'][col]=pd.to_numeric(data['ap_2010'][col],errors='coerce')
print(data['ap_2010'].dtypes)


# In[168]:


combined = data['sat_results']
combined=combined.merge(data['ap_2010'],on='DBN',how='left')
combined=combined.merge(data['graduation'],on='DBN',how='left')
print(combined.head())
print(combined.shape)


# In[169]:


combined=combined.merge(data['class_size'],on='DBN',how='inner')
combined=combined.merge(data['demographics'],on='DBN',how='inner')
combined=combined.merge(data['survey'],on='DBN',how='inner')
combined=combined.merge(data['hs_directory'],on='DBN',how='inner')
print(combined.head())
print(combined.shape)



# In[170]:


mean = combined.mean()
combined = combined.fillna(mean)
combined = combined.fillna(0)
print(combined.head())


# In[171]:


def ext(col):
    return col[0:2]
combined['school_dist']=combined['DBN'].apply(ext)
print(combined['school_dist'].head())


# In[172]:


correlations=combined.corr()
correlations=correlations['sat_score']
print(correlations)


# In[173]:


import matplotlib.pyplot as plt
combined.plot.scatter(x='total_enrollment',y='sat_score')
plt.show()


# In[174]:


low_enrollment=combined[combined['total_enrollment']<1000]
low_enrollment=low_enrollment[low_enrollment['sat_score']<1000]
print(low_enrollment['School Name'])


# In[175]:


combined.plot.scatter(x='ell_percent',y='sat_score')
plt.show()


# In[176]:


from mpl_toolkits.basemap import Basemap
m = Basemap(
    projection='merc', 
    llcrnrlat=40.496044, 
    urcrnrlat=40.915256, 
    llcrnrlon=-74.255735, 
    urcrnrlon=-73.700272,
    resolution='i'
)

m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)

longitudes=combined['lon'].tolist()
latitudes=combined['lat'].tolist()
m.scatter(longitudes,latitudes,s=20,zorder=2,latlon=True,c=combined['ell_percent'],cmap='summer')
plt.show()


# In[177]:


dist=combined.groupby('school_dist')
districts=dist.agg(np.mean)
districts.reset_index('school_dist',inplace=True)
print(districts.head())


# In[178]:


m= Basemap(
    projection='merc',
    llcrnrlat=40.496044,
    urcrnrlat=40.915256,
    llcrnrlon=-74.255735,
    urcrnrlon=-73.700272,
    resolution='i'
)

m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)

longitudes=districts['lon'].tolist()
latitudes=districts['lat'].tolist()
m.scatter(longitudes,latitudes,s=50,zorder=2,latlon=True,c=districts['ell_percent'],cmap='summer')
plt.show()


# In[179]:


get_ipython().magic('matplotlib inline')
correlations[survey_fields].plot.bar()


# In[180]:


plt.scatter(combined['saf_s_11'],combined['sat_score'])


# There is a correlation between school safty and SAT scores, though the correlation is not strong enough to show a very obvious linear correlation in the plot. While most of the schools with an average score higher than 1600, shools with an average score lower than 1500 also have a safty score lower than 5.

# In[184]:


districts = combined.groupby("school_dist").agg(np.mean)
districts.reset_index(inplace=True)

m = Basemap(
    projection='merc', 
    llcrnrlat=40.496044, 
    urcrnrlat=40.915256, 
    llcrnrlon=-74.255735, 
    urcrnrlon=-73.700272,
    resolution='i'
)

m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)
m.fillcontinents(color='white',lake_color='#85A6D9')

longitudes = districts["lon"].tolist()
latitudes = districts["lat"].tolist()
m.scatter(longitudes, latitudes, s=50, zorder=2, latlon=True, c=districts["saf_s_11"], cmap="summer")
plt.show()


# Most of the schooles located in Manhattan and Queens have high safety scores. While most of the schools in Brooklyn have low safety schools. And the safety scores of the schools in the Bronx are seems evenly distributed. 

# In[190]:


race = ['white_per','asian_per','black_per','hispanic_per']
combined.corr()['sat_score'][race].plot.bar()


# According to the bar plot, the SAT scores have a positive correlation with the white and asian students, while its correlation with black and hispanic students is negative.

# In[196]:


plt.scatter(combined['hispanic_per'],combined['sat_score'])


# In[197]:


hispanic = combined[combined['hispanic_per']>95]
print(hispanic['School Name'])


# In[200]:


non_hispanic = combined[combined['hispanic_per']<10]
print(non_hispanic['School Name'])


# From the scatter plot, we discover a negative correlation between the hispanic percentage of the student body and SAT score. As we explore the schools with high hispanic percentage(over 95%), the graduation rate is relatively low, compared with the average level of schools in New York. While the schools with low hispanic percentage(<10%), Asian students normally take the major proportion of the student body, and the academic performance are normally above the average level among the NY High schools.

# In[204]:


gender=['male_per','female_per']
combined.corr()['sat_score'][gender].plot.bar()
plt.show()


# As shown in the plot, male percentage seems has a slight negative correlation with SAT score, while female percentage has a slight positive correlation with SAT score.

# In[205]:


plt.scatter(combined['female_per'],combined['sat_score'])


# The schools with relatively balanced gender proporation with a female percentage at around 40% and those with a female percentage are between 60% to 80% tend to have higher SAT scores. There is an interesting finding in the plot that the schools exclusively for female students have relatively lower SAT scores.

# In[211]:


high = combined[combined['female_per']>60]
high = high[high['sat_score']>1700]
print(high['School Name'])


# Most of the shools have high rankings among NY high schools and have a predominant percentage of white students. They  seems to be selective liberal arts schools with high academic standards.

# In[212]:


combined['ap_per']=combined['AP Test Takers ']/combined['total_enrollment']
plt.scatter(combined['ap_per'],combined['sat_score'])


# The plot seems divided into two directions, as the AP percentage of a batch of schools have positive correlation with  SAT scores, while some others do not show the correlation between the two factors. However, for most of the schools with low AP percentage do have a low SAT scores.

# In[217]:


#correlation between class size and SAT scores
plt.scatter(combined['AVERAGE CLASS SIZE'],combined['sat_score'])

