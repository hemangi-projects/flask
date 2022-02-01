"""
* * * * * 
  * * * * 
    * * * 
      * * 
        * 
        * 
      * * 
    * * * 
  * * * * 
* * * * * 
"""
n = int(input("Number:"))
for i in reversed(range(1,n+1)):
	for k in range(n-i):
		print(" ",end=" ")
	for j in range(i):
		print("*", end =" ")
	print("")
for i in range(1,n+1):
	for k in range(n-i):
		print(" ",end=" ")
	for j in range(i):
		print("*", end =" ")
	print("")
