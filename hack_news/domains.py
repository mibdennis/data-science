import read

data = read.load_data()
domain=data.url
counts=domain.value_counts()

#for name,row in domain.items():
#   print("{0}:{1}".format(name,row))
 print(counts.iloc[:100])
print (type(counts))
