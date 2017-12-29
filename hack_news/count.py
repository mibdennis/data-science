from collections import Counter
import pandas as pd
import read

data = read.load_data()

def word_counter(itr):
    # Takes in an iterable and return a dictionary; will be data.headline
    final_str = ''
    for str1 in itr.values:
        final_str += " " + str(str1) #added a space because the concatenation does not do that by default
    # Make sure every word is lower-cased so it gets counted the right way
    final_str = final_str.lower()
    # Split the str at whitesp. char
    all_words = final_str.split() # whitesp. delimiter by default
    # Make a dictionary
    word_count = {}
    for word in all_words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
            
    return word_count

counting_dict = word_counter(data.headline)
all_values = counting_dict.values()
first100 = []

for v in sorted(all_values, key = int, reverse = True)[:100]:
    for key,value in counting_dict.items():
        if value == v:
            first100.append((key,value))
print(first100)   
