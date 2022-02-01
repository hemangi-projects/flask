number = int(input("enter number:"))
#print(str(number[::-1]))
a= number
print(number)
result = 0
res=1
while number > 0:
	rem = number %10
	for i in range(len(str(a))):
		res = res*rem
	result = result + res
	res=1
	number = int(number/10)
if result == a:
	print("number is amstrong")
else:
	print("not")
