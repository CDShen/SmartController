from enum import Enum

class Animal(Enum):
	ant = 1
	dog = 2


for i in Animal:
	print (i)