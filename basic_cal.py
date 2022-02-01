print("Please select operation -")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
print("4. Divide")
answer = "y"
while answer == 'y':
	i = True
	while i:
		operator = int(input("Select operations form 1, 2, 3, 4 : "))
		if operator not in (1,2,3,4):
			print("Wrong Input! Please Choose between 1 to 4")
		else:
			i=False
	if operator == 1:
		a = int(input("Enter first number : "))
		b = int(input("Enter second number : "))
		print(str(a) + " + " + str(b) + " = " + str(a+b))
	if operator == 2:
		a = int(input("Enter first number : "))
		b = int(input("Enter second number : "))
		print(str(a) + " - " + str(b) + " = " + str(a-b))
	if operator == 3:
		a = int(input("Enter first number : "))
		b = int(input("Enter second number : "))
		print(str(a) + " * " + str(b) + " = " + str(a*b))
	if operator == 4:
		a = int(input("Enter first number : "))
		b = int(input("Enter second number : "))
		print(str(a) + " / " + str(b) + " = " + str(a/b))
	ans = True
	while ans:
		ans = input("Want some another operation to do?press y/n: ")
		if ans == 'n' or ans == 'y':
			answer = ans;
			ans = False;
		else:
			print("Wrong input");
			ans = True;
