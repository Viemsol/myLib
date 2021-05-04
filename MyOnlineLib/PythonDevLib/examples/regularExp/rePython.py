
'''
'\d\d\d.\d\d.\d\d\d'      it will search of match for 123*12*555 this pattern (. is for any charecter ) \d is for any digit
Is Same as
'\d{3}.\d{2}.\d{3}'      it will search of match for 123*12*555 this pattern (. is for any charecter ) \d is for any digit

also range can be specified
'\d{3,4}.\d{2}.\d{3}'  will match 123*12*555 and 1523*12*555 pattens 3 is min 4 is max numbers Range
------------------------------------------------------
Mr. Abc Mr KBC Mrs lkb

'(Mr|Mrs)\.?\s[A-Z]\w*'        \. is nothing but . character (. have another meaning "any char" in re) , ? after any char meas that chr is optional,\s is space [All upar case latters] \w* is word carecters>0, * will bake 0 or more word cahrecters
The "\w" means "any word character" which usually means alphanumeric (letters, numbers, regardless of case) plus underscore (_)
'''
sentenceNumber =  "123X34p678  1723X34p678  12693X34p678"
import re

if(re.search('\d\d\d.\d\d.\d\d\d',sentenceNumber)):
    print("found")
test = "hhhhhhhhhhhhhhhabcd"
if(re.search('(abcd)',test)):
    print("found")
matches = re.finditer('\d\d\d.\d\d.\d\d\d',sentenceNumber)
for match in matches:
    print(match)

replace = re.sub('\d\d\d.\d\d.\d\d\d', 'GAGAGA', sentenceNumber)
print(replace)

nameTest = "Mr. Pope , Mr Akaba and Mrs Meena are  members of commette "
matches = re.finditer('(Mr|Mrs)\.?\s[A-Z]\w*',nameTest)
for match in matches:
    print(match)