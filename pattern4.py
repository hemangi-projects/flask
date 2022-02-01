"""
* * * * * 
  * * * * 
    * * * 
      * * 
        * 
"""
n = int(input("Number:"))
x=0
for i in reversed(range(1,n+1)):
	for j in range(n-i):
		print(" ", end =" ")
	for k in range(i):
		print("*",end = " ")
	print("")
	
