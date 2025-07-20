from utils import menu, add_to_dict


def pokemart(player):
    print("\nwelcome to the pokemart!")
    print("how can we assist you today?")

    item_prices = {
        "pokeball": 1000,
        "great ball": 5000,
        "ultra ball": 10000,
        "master ball": 50000,
        "potion": 1000,
        "super potion": 2500,
        "hyper potion": 20000,
        "revive": 2500,
        "max revive": 10000,
        "party revive": 50000,
        "book": 10000,
    }

    options = ["Buy", "Sell", "Exit"]

    while True:
        choice = menu(options)

        if choice == 0:
            print("you selected 'buy'")
            print("here are the available items and their prices:")

            print(f"\nyour money: Ƀ{player.money:.2f}\n")

            shop_items_displays = []
            shop_items = []
            for item, price in item_prices.items():
                shop_items_displays.append(f"{item.title()}: Ƀ{price:.2f}")
                shop_items.append(item)

            item_choice = menu(shop_items_displays)
            try:
                quantity_choice = int(
                    input("enter the quantity you want to buy: (>0) ")
                )
                if quantity_choice < 1:
                    quantity_choice = 1

            except:
                quantity_choice = 1

            total_cost = item_prices[shop_items[item_choice]] * quantity_choice

            print(
                f"the total cost of {quantity_choice}x {shop_items[item_choice]} is Ƀ{total_cost}."
            )

            confirm_choice = input(
                "confirm your purchase? (Y/anything that isn't 'Y'): "
            )
            if confirm_choice.upper() == "Y":
                # see if player can afford purchase
                if total_cost <= player.money:
                    print("purchase successful! thank you for shopping!")
                    # deduct cost from players money
                    player.money -= total_cost
                    add_to_dict(player.items, shop_items[item_choice], quantity_choice)
                    print(f"you now have Ƀ{player.money:.2f}")
                else:
                    print("you don't have enough money to make this purchase")
            else:
                print("purchase canceled.")

        elif choice == 1:
            print("you selected 'sell'")
            print("pick another option you cheapo")

        elif choice == 2:
            print("thank you for visiting the pokemart. goodbye!")
            break

        player.display_items()
