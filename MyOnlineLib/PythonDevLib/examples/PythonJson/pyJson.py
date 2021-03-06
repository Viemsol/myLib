import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'
# parse x:

y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])
###############################################

# a Python object (dict):
y  = {
  "cmd": "Amar",
  "para": [40,50,"010204FF"],
  "status": "pass"
}
# convert into JSON:
z = json.dumps(y)

# the result is a JSON string:
print(z)