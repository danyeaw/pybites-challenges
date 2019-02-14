import collections


Item = collections.namedtuple("Item", "name cost")

living_room = [
    Item("TV", 200),
    Item("Couch", 100),
    Item("Computer", 800),
    Item("Rug", 50),
]
bedroom = [
    Item("Bed", 50),
]
house_inventory = {"Living Room": living_room, "Bedroom": bedroom}

for room in house_inventory:
    print("Room:", room)
    for item in house_inventory[room]:
        print(f"Item: {item.name}, ${item.cost}")

