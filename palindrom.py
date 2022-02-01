number = int(input("enter number:"))
#print(str(number[::-1]))
a = number
print(number)
result = 0
while number > 0:
	rem = number %10
	result = result *10+rem
	number = int(number/10)
if a == result:
	print("number is Palindrom")
else:
	print("number is not Palindrom")
