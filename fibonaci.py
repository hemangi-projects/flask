number = int(input("enter number:"))
a=0
b=1
for i in range(number-2):
	sum = a+b
	a=b
	b=sum
	print("i:",i)
	print("sum:",sum)
	
print(sum)
