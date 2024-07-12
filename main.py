from actions import Inventory, Actions

def inventory():
    print(f"\n{'-'*80}\n{Inventory().get_inventory()[0]}")
    print(f"\nTotal profit: {Inventory().get_inventory()[1]}")

    inventory_choice = int(input(f"""{'-'*80}
                            Inventory: 
                            1. Update actual prices
                            2. Back\n{'-'*80}
                            -> """))
    match inventory_choice:
        case 1: 
            print(f"{' '*28}Loading...\n")
            Actions().update_actual_prices()
            inventory() #anyone number geting back
        
def cancel():
    print(f"\n{' '*28}!Canceled!\n")
    main()

def add_item():
    print(f"""{'-'*80}\nGuide:
- 'app id' is a number that you can get \nfrom https://steamcommunity.com/market/listings/730 "<-- app_id of CS2 fpr example" /Chroma%20Case
- 'item name' s best to indicate as accurately as possible, \notherwise, you may accidentally add the wrong item that you need
- 'buy price' is the price you pay for the item
- 'date' is the date when you bought the item (31.12.2024 23:59:59 for example)
- 'qty' is the quantity of the item you bought
- send 'cancel' if you want to cancel\n{'-'*80}""")
    

    app_id = (input(f"{' '*28}app id -> "))
    if app_id == "cancel":
        cancel()
    item_name = (input(f"{' '*28}item name -> "))
    if item_name == "cancel":
        cancel()
    buy_price = (input(f"{' '*28}buy price -> "))
    if buy_price == "cancel":
        cancel()
    date = (input(f"{' '*28}date -> "))
    if date == "cancel":
        cancel()
    qty = (input(f"{' '*28}qty -> "))
    if qty == "cancel":
        cancel()

    print(f"{' '*28}Loading...")
    Inventory().add_item(app_id=int(app_id), item_name=item_name, buy_price=float(buy_price), date=date, qty=int(qty))
    print(f"\n{' '*28}Item added successfully!\n")
    main()

def remove_item():
    print(f"""{'-'*80}\nGuide: 
- you need to specify both 'date' and 'buy price'
- send 'cancel' if you want to cancel
- 'app id' is a number that you can get \nfrom https://steamcommunity.com/market/listings/ 730 <-- app_id of CS2 fpr example /Chroma%20Case
- 'buy price' must be specified exactly as it is indicated in the inventory. That is, if it is indicated as $15.00 USD, \nyou need to specify 15.00, otherwise the item will not be deleted
- 'item name' s best to indicate as accurately as possible, \notherwise, you may accidentally remove the wrong item that you need\n{'-'*80}""")
    
    app_id = (input(f"{' '*28}app id -> "))
    if app_id == "cancel":
        cancel()
    item_name = (input(f"{' '*28}item name -> "))
    if item_name == "cancel":
        cancel()
    date = (input(f"{' '*28}date -> "))
    if date == "cancel":
        cancel()
    buy_price = (input(f"{' '*28}buy price -> "))
    if buy_price == "cancel":
        cancel()

    Inventory().remove_item(itemName=item_name, date=date, buyPrice=buy_price, app_id=int(app_id))
    print(f"\n{' '*28}Item removed successfully!\n")
    main()

def get_price():
    print(f"""{'-'*80}\n Guide:
- send 'cancel' if you want to cancel
- 'app id' is a number that you can get \nfrom https://steamcommunity.com/market/listings/ 730 <-- app_id of CS2 fpr example /Chroma%20Case
- 'item name' s best to indicate as accurately as possible, \notherwise, you may accidentally remove the wrong item that you need\n{'-'*80}""")
    
    app_id = (input(f"{' '*28}app id -> "))
    if app_id == "cancel":
        cancel()
    item_name = (input(f"{' '*28}item name -> "))
    if item_name == "cancel":
        cancel()
    item = Actions().get_price(app_id=int(app_id), item_name=item_name)
    try:
        print(f"{'-'*80}\nItem steam name: {item[2]}; \nitem price: {item[0]}; \nitem qty: {item[1]};")
    except:
        print(f"Item: {item}")


def main():
    Actions().create_json()
    while True:
        choice = int(input(f"""{'-'*80}
                           Steam Invest Tracker

                           Enter your choice:
                           1. Inventory
                           2. Add item
                           3. Remove item
                           4. Find out the cost of an item
                           5. Exit\n{'-'*80}
                           -> """))
        match choice:
            case 1: #inventory
                inventory()    
            case 2: #add item
                add_item()
            case 3: #remove item
                remove_item()
            case 4: #get price
                get_price()
            case 5: #exit
                print("\nExiting...")
                quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{e}")
        print("\nSomething went wrong, try again after restart...")