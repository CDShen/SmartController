from enum import Enum

class Animal(Enum):
	ant = 1
	dog = 2


# print (Animal.ant.value)

# for i in Animal:
# 	print (i.value)

a = Animal.ant
b = Animal.ant
c = Animal.dog

if a <= b:
	print('same')

if b <= c:
	print('same')