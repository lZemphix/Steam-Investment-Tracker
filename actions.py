import requests
import json, os, asyncio
from bs4 import BeautifulSoup
import pandas as pd

class Actions:

    def __init__(self):
        self.create_json()
        self.json_data = json.load(open("inventory.json"))

    def create_json(self):
        """create inventory.json if not exists"""
        if not os.path.exists("inventory.json"):
            base_json_data = {
                "totalProfit": "$0.00 USD",
                "items": []
            }
            with open("inventory.json", "w") as file:
                json.dump(base_json_data, file, indent=4)


    def get_data(self, app_id: int, item_name: str):
        """return response from link"""
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        link = f"https://steamcommunity.com/market/search?q={item_name.replace(' ', '+')}&appid={app_id}"
        return requests.get(link, headers=headers)
    
    def generate_html(self, app_id: int, item_name: str):
        """generate html from link"""
        with open("index.html", "w") as file:
            file.write(self.get_data(app_id, item_name).text)

    def get_price(self,app_id: int, item_name: str):
        """return price, qty, name, game"""
        try:
            bs = BeautifulSoup(self.get_data(app_id, item_name).text, "lxml")
            price = bs.find("span", {"class": "sale_price"}).text.strip()
            qty = bs.find("span", {"class": "market_listing_num_listings_qty"}).text
            name = bs.find("span", {"class": "market_listing_item_name"}).text.strip()
            game = bs.find("span", {"class": "market_listing_game_name"}).text
            return price, qty, name, game
        except:
            return "Item not found in steam market"

    def update_total_profit(self):
        """Update total profit in inventory.json"""

        json_data = json.load(open("inventory.json"))
        _, _, items_data = Inventory().get_inventory()
        total_profit = 0
        for item in items_data:
            total_profit += float(item["itemProfit"].replace("$", "").replace("USD", ""))
        json_data["totalProfit"] = f"${total_profit:.2f} USD"
        with open("inventory.json", "w") as file:
            json.dump(json_data, file, indent=4)

    def update_actual_prices(self):
        """Update actual prices in inventory.json"""
        names = []
        for item in self.json_data["items"]:
            names.append(item["itemName"] if item["itemName"] not in names else None)
            names = list(filter(None, names))
        for name in names:
            item_price, item_qty, item_name, app_name = Actions().get_price(app_id=self.json_data["items"][names.index(name)]["appId"], item_name=name)
            for item in self.json_data["items"]: #TODO: O^2(((( need to optimize
                if item["itemName"] == item_name:
                    item["priceNow"] = item_price
                    item['itemProfit'] = f"${round((float(item_price.replace('$', '').replace('USD', '')) - float(item['buyPrice'].replace('$', '').replace('USD', ''))) * item['qty'], 2)} USD"
                    with open("inventory.json", "w") as file:
                        json.dump(self.json_data, file, indent=4)
                    print(f"[=] updated {item_name}")
        self.update_total_profit()

    


class Inventory:

    def __init__(self):
        self.json_data = json.load(open("inventory.json"))
    
    def add_item(self, *, app_id: int, item_name: str, buy_price: float, date: str, qty: int,) -> None:
        """Write new item to inventory.json"""
        
        self.actual_price, self.qty, self.steam_item_name, self.app_name = Actions().get_price(app_id, item_name)
        item_profit = (float(self.actual_price.replace("$", "").replace("USD", "")) - buy_price) * qty
        self.json_data["items"].append(
            {
                "date": date,
                "itemName": self.steam_item_name.replace("\u2605 ", ""),
                "buyPrice": f"${buy_price:.2f} USD",
                "priceNow": self.actual_price,
                "qty": qty,
                "itemProfit": f"${item_profit:.2f} USD",
                "appName": self.app_name,
                "appId": app_id,
            }
        )
        with open("inventory.json", "w") as file:
            json.dump(self.json_data, file, indent=4)

    def remove_item(self, *, itemName: str, date: str = None, buyPrice: str = None, app_id: int) -> None:
        """Remove item from inventory.json"""
        item_name = (Actions().get_price(app_id=app_id, item_name=itemName)[2]).replace("\u2605 ", "")
        buy_price = f"${buyPrice} USD"
        if date and buyPrice:
            for item in self.json_data["items"]:
                if item["itemName"] == item_name and item["date"] == date and item["buyPrice"] == buy_price:
                    self.json_data["items"].remove(item)
                    break
        else:
            print("Need to specify date or buyPrice")
        with open("inventory.json", "w") as file:
            json.dump(self.json_data, file, indent=4)
        
    def get_inventory(self):
        """Get all items from inventory.json"""
        items_data = json.load(open("inventory.json"))["items"]
        profit_data = json.load(open("inventory.json"))["totalProfit"]
        dataframe = pd.DataFrame(items_data)
    
        return dataframe.to_string(), profit_data, items_data


if __name__ == "__main__":
    print("scrpt test")
    # update_actual_prices()
    # print(Actions().get_price(730, "falchion knife (minimal-ware)"))
    # Inventory().remove_item(itemName="falchion knife freehand (minimal-ware)", date='12.07.2024 21:34:10', buyPrice="166.00", app_id=730)
    # Inventory().add_item(app_id=730, item_name="falchion knife (minimal-ware)", buy_price=166.0, date='12.07.2024 21:34:10', qty=1)


