# import module shopping card and class
from shopping import shopping_card
# create object
sc = shopping_card()
# add items
sc.add("vegan donut (ˆڡˆ)◞🍩", 42)
sc.add("vegan kimchi 🥬🧄", 99)
sc.add("Bohnekamp🌱", 1)
sc.add("Bohnekamp🌱", "1")
# get total amount
sc.total()
# print all items
sc.print_all()
# remove one item
sc.remove("Bohnekamp🌱")
# get total amount
sc.total()
# print all items
sc.print_all()