from shopping import shopping_card

sc = shopping_card()

sc.add("vegan donut", 42)
sc.add("vegan kimchi", 99)
sc.add("Bohnekamp", 1)
sc.add("Bohnekamp", "1")
sc.total()
sc.print_all()

sc.remove("Bohnekamp")
sc.total()
sc.print_all()