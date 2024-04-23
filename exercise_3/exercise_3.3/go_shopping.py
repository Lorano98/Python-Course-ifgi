import easy_shopping

print(easy_shopping.calc.addition(7,5))
print(easy_shopping.calc.substraction(34,21))
print(easy_shopping.calc.multiplication(54,2))
print(easy_shopping.calc.division(144,2))
print(easy_shopping.calc.division(45,0))

sc = easy_shopping.shopping_card()

sc.add("vegan donut", 42)
sc.add("vegan kimchi", 99)
sc.add("Bohnekamp", 1)
sc.add("Bohnekamp", "1")
sc.total()
sc.print_all()

sc.remove("Bohnekamp")
sc.total()
sc.print_all()