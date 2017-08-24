from enum import Enum

class Animal(Enum):
	ant = 1
	dog = 2


c = Animal(2)
if c == Animal.dog:
	print (c.value)

# for i in Animal:
# 	print (i)