dictionary_unique = {"a": "alpha", "o": "omega", "g": "gamma", "g": "beta"}
for key, value in dictionary_unique.items():  #accessing keys
    print("Key = {} Value = {}".format(key,value))

dictionary_unique.values()  #accessing values without for loop
dictionary_unique.keys() #accessing keys without for loop

#You could even access a value by specifying a key as a parameter to the dictionary.
print("value for key a is = {}".format(dictionary_unique['a']))

#Updating Dictionary in 3 ways 

#1
dictionary_unique['key3'] = 'Geeks'
dictionary_unique['key4'] = 'is'
dictionary_unique['key5'] = 'portal'
dictionary_unique['key6'] = 'Computer'
#2
dict1 = {'key3':'geeks', 'key4':'is', 'key5':'fabulous'} 
dictionary_unique.update(dict1) 

#nested Dictionary
dictionary_nested = {"datacamp":{"Deep Learning": "Python", "Machine Learning": "Pandas"},"linkedin":"jobs","nvidia":"hardware"}