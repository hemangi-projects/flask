"""
        * 
      * * 
    * * * 
  * * * * 
* * * * * 
  * * * * 
    * * * 
      * * 
        * 
"""
n = int(input("Number:"))
x=0
for i in reversed(range(1,n+1)):
	for j in range(i-1):
		print(" ", end =" ")
	for k in range(n+1-i):
		print("*",end = " ")
	print("")
for i in range(1,n+1):
	if i>1:
		for j in range(i-1):
			print(" ", end =" ")
		for k in range(n+1-i):
			print("*",end = " ")
		print("")
	
