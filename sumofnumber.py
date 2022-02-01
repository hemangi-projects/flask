number = int(input("enter number:"))
res = 0
while number > 0:
	rem = number%10
	res = res+rem
	number = int(number /10)
	if number == 0 and res > 9:
		number = res
		res = 0
print(res)
