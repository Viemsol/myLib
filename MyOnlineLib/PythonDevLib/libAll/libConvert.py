def base36encode(number, filLen=5,alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
	"""Converts an integer to a base36 string."""
	if not isinstance(number, (int, int)):
		raise TypeError('number must be an integer')

	base36 = ''
	sign = ''

	if number < 0:
		sign = '-'
		number = -number
	out =""
	if 0 <= number < len(alphabet):
		out =  sign + alphabet[number]
	else:
		while number != 0:
			number, i = divmod(number, len(alphabet))
			base36 = alphabet[i] + base36
		out = sign + base36
	
	while(len(out)<filLen):
		out = "0"+out

	print(out)
	return out

def base36decode(number):
    return int(number, 36)