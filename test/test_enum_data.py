from enum import Enum

class Animal(Enum):
	ant = 1
	dog = 2


print (Animal.ant.value)

for i in Animal:
	print (i.value)	