number = int(input("enter number:"))
#print(str(number[::-1]))

print(number)
result = 0
while number > 0:
	rem = number %10
	result = result *10+rem
	number = int(number/10)
print("result :",result)
