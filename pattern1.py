"""
* 
* * 
* * * 
* * * * 
* * * * *
"""
n = int(input("Number:"))
x=0
for i in range(1,n+1):
	for j in range(i):
		print("*", end =" ")
		x+=1;
	print("")
	
