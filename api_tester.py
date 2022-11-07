class A:
    def add(a, b):
        return a+b

class B(A):
    def minus(self, a, b):
        return A.add(a, b)

objB = B()
print(objB.minus(1, 2))
