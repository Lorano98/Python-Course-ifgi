class shopping_card:
    def __init__(self):
        # empty card
        self.items = {}

    # Add items to the shopping_card with a given quantity
    def add(self,new_item,quantity):
        if(type(quantity) != int):
            print("Quantity must be an Integer!")
            return
        # Check wether the item is already in the card
        if(self.items.get(new_item) == None):
            # Add it to the card
            self.items.update({new_item: quantity})
        else:
            # Rise the amount
            self.items.update({new_item: self.items[new_item] + quantity})

    # Remove one item from the card
    def remove(self,del_item):
        # Remove item, when there is only 1 item in the card
        if self.items[del_item] == 1:
            self.items.pop(del_item)
        else:
            # Update quantity
            self.items[del_item] -= 1

    # Count the total amount of items
    def total(self):
        sum = 0
        # Add all the quantities
        for item in self.items:
            sum += self.items[item]
        print(f"There are {sum} items in the card.")
    
    # Print all items
    def print_all(self):
        print("Items in the card:")
        print(self.items)