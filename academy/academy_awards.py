
# coding: utf-8

# In[1]:


import pandas as pd

academy = pd.read_csv('~/Desktop/dataquest/academy/academy_awards.csv', encoding = 'ISO-8859-1')

academy.head()


# In[2]:


for x in range(6,11):
    r = academy.iloc[:,x].value_counts(dropna=True)
    print(r)


# In[3]:


academy['Year']=academy['Year'].str[0:4]
academy['Year']=academy['Year'].astype('int64')


# In[4]:


later_than_2000 = academy[academy['Year']>2000]


# In[5]:


award_categories = ('Actor -- Leading Role','Actor -- Supporting Role','Actress -- Leading Role','Actress -- Supporting Role')
nominations = later_than_2000[later_than_2000["Category"].isin(award_categories)]


# In[6]:


replace_dict = {"YES": 1, "NO": 0}
nominations.iloc[:,5]=nominations.iloc[:,5].map(replace_dict)
nominations["Won"]=nominations["Won?"]
final_nominations = nominations.drop(['Won?','Unnamed: 5','Unnamed: 6','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10'], axis=1) 


# In[7]:


final_nominations.head()


# In[8]:


additional_info_one=final_nominations['Additional Info'].str.rstrip("'}")
additional_info_two=additional_info_one.str.split("{'")
movie_names=additional_info_two.str[0]
characters=additional_info_two.str[1]


# In[9]:


final_nominations['Movie']=movie_names
final_nominations['Character']=characters
final_nominations=final_nominations.drop(['Additional Info'],axis=1)
final_nominations.head()


# In[10]:


import sqlite3 as sq
conn = sq.connect("nominations.db")
final_nominations.to_sql("nominations",conn,index=False)


# In[11]:


q1 = "pragma table_info(nominations)"
print(conn.execute(q1).fetchall())
q2 = "select * from nominations limit 10"
print(conn.execute(q2).fetchall())


# In[13]:


q = "select * from nominations limit 10"
query = conn.execute(q).fetchall()
for qs in query:
    print(qs)


# In[14]:


ceremonies_create = "create table ceremonies (id integer primary key, Year integer, Host text);"

years_hosts = [(2010, "Steve Martin"),
               (2009, "Hugh Jackman"),
               (2008, "Jon Stewart"),
               (2007, "Ellen DeGeneres"),
               (2006, "Jon Stewart"),
               (2005, "Chris Rock"),
               (2004, "Billy Crystal"),
               (2003, "Steve Martin"),
               (2002, "Whoopi Goldberg"),
               (2001, "Steve Martin"),
               (2000, "Billy Crystal"),
            ]
conn.execute(ceremonies_create)


# In[15]:


insert_query = "insert into ceremonies (Year, Host) values (?,?);"
conn.executemany(insert_query, years_hosts)
#execute many!!!!!


# In[16]:


print(conn.execute("select * from ceremonies limit 10;").fetchall())


# In[17]:


print(conn.execute("pragma table_info(ceremonies);").fetchall())


# In[18]:


conn.execute("pragma foreign_keys = on;")


# In[19]:


#setup one-to many relation to nominations/ceremonies
create_nom = '''
create table nominations_two (
    id integer primary key,
    category text,
    nominee text,
    movie text,
    character text,
    won integer,
    ceremony_id integer,
    foreign key(ceremony_id) references ceremonies(id)
)
'''
conn.execute(create_nom)


# In[21]:


nom_query = '''
select ceremonies.id as ceremony_id, nominations.category as category, nominations.nominee as nominee, nominations.movie as movie, nominations.charater as character, nominations.won as won from nominations
inner join ceremonies
on nominations.year == ceremonies.year 
'''
joined_nominations = conn.execute(nom_query).fetchall()


# In[22]:


insert_nominations_two = "insert into nominations_two (ceremony_id, category, nominee, movie, character, won) values(?,?,?,?,?,?);"
conn.executemany(insert_nominations_two, joined_nominations)


# In[24]:


print(conn.execute("select * from nominations_two limit 5;").fetchall())


# In[29]:


conn.execute("drop table nominations")


# In[30]:


conn.execute("alter table nominations_two rename to nominations")


# In[32]:


print(conn.execute("select * from nominations limit 5;").fetchall())


# In[34]:


conn.execute("create table movies (id integer primary key, movie text);")
conn.execute("create table actors (id integer primary key, actor text);")
conn.execute("create table movies_actors (id integer primary key, movie_id references movies(id), actor_id references actors(id))")


# In[36]:


get_movies= conn.execute("select distinct movie from nominations").fetchall()
insert_movies="insert into movies(movie) values(?);"
conn.executemany(insert_movies,get_movies)


# In[37]:


get_actors= conn.execute("select distinct nominee from nominations").fetchall()
insert_actors="insert into actors(actor) values(?);"
conn.executemany(insert_actors,get_actors)


# In[40]:


#populate join table
insert_join = conn.execute("select movie, nominee from nominations").fetchall()
insert = "insert into movies_actors(movie_id, actor_id) values((select id from movies where movie == ?),(select id from actors where actor == ?))"
conn.executemany(insert, insert_join)

