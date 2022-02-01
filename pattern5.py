"""
        * 
      * * * 
    * * * * * 
  * * * * * * * 
* * * * * * * * *
"""
n = int(input("Number:"))
for i in range(1,n+1):
	if i % 2 != 0:
		for j in range(int((n-i)/2)):
			print(" ", end =" ")
		for k in range(i):
			print("*",end = " ")
		print("")
	
