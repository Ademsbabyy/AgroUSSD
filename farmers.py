import json
import os

class Farmers:
    def __init__(self, farmers_file='farmers.json', produce_file='produce.json'):
        self.farmers_file = farmers_file
        self.produce_file = produce_file
        self.logged_in_farmer = None
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        for file in [self.farmers_file, self.produce_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)

    def register(self, name, phone_number, pin):
        with open(self.farmers_file, 'r+') as f:
            farmers = json.load(f)
            if phone_number in farmers:
                print("Farmer already registered.")
                return False
            farmers[phone_number] = {'name': name, 'pin': pin}
            f.seek(0)
            json.dump(farmers, f, indent=4)
            f.truncate()
        print("Registration successful.")
        return True

    def login(self, phone_number, pin):
        with open(self.farmers_file, 'r') as f:
            farmers = json.load(f)
            if phone_number in farmers and farmers[phone_number]['pin'] == pin:
                self.logged_in_farmer = phone_number
                print(f"Welcome {farmers[phone_number]['name']}!")
                return True
            else:
                print("Invalid credentials.")
                return False

    def add_produce(self, produce_name, quantity, price):
        if not self.logged_in_farmer:
            print("You must be logged in to add produce.")
            return False

        with open(self.produce_file, 'r+') as f:
            produce_data = json.load(f)
            user_produce = produce_data.get(self.logged_in_farmer, [])

            # Add new produce
            user_produce.append({
                "produce_name": produce_name,
                "quantity": quantity,
                "price": price
            })

            produce_data[self.logged_in_farmer] = user_produce
            f.seek(0)
            json.dump(produce_data, f, indent=4)
        print("Produce added successfully.")
        return True

    def view_other_produce(self):
        if not self.logged_in_farmer:
            print("You must be logged in to view produce.")
            return

        with open(self.farmers_file, 'r') as f:
            farmers = json.load(f)

        with open(self.produce_file, 'r') as f:
            produce_data = json.load(f)

        found = False
        print("\nProduce on sale by other farmers:\n" + "-"*40)
        for farmer_id, produce_list in produce_data.items():
            if farmer_id == self.logged_in_farmer:
                continue
            farmer_name = farmers[farmer_id]['name']
            for item in produce_list:
                print(f"Farmer: {farmer_name}")
                print(f"Produce: {item['produce_name']}")
                print(f"Quantity: {item['quantity']}")
                print(f"Price: {item['price']}")
                print("-" * 40)
                found = True

        if not found:
            print("No produce from other farmers available.")

#  Usage:
if __name__ == "__main__":
    app = Farmers()

