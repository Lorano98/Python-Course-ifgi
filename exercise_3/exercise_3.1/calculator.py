class calculator:
    # constructor
    def __init__(self):
        pass
    # addition 
    def addition(a,b):
        return a+b
    # substraction
    def substraction(a,b):
        return a-b
    # multiplication 
    def multiplication(a,b):
        return a*b
    # division
    def division(a,b):
        # if the second divisor is zero return error
        if(b != 0):
            return a/b
        else:
            return "b is 0!"