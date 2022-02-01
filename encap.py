class Base:
    def __init__(self):
        self.a = "GeeksforGeeks"
        self.__c = "GeeksforGeekssssssssssssss"
        print("dfgdfgdg",self.a)
        print("rrrrrrrrrrr",self.__c)
    def foo(self):
    	print("fooooooooooo",self.__c)
    
  
# Driver code
obj1 = Base()
print("classssssssssssss",obj1.a)
#obj2 = Derived()
print("classdooooooooooooo",obj1.foo())
print("classdooooooooooooo",obj1.__c)

