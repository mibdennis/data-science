import read

data=read.load_data()

upv = data.upvote.tolist()

count=upv.count_values() 

ranking=data[upv]['url']

print(count[:100])

print(type(upv))
