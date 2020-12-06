from data import MENU, money_value

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0,
}

water_v = resources["water"]
milk = resources["milk"]
coffee = resources["coffee"]
R_money = resources["money"]

def give_me_money():
    """Checking value of inserted money"""
    print("Please insert coins.")
    quarters = int(input("How many quarters $0.25 ? "))
    dimes = int(input("How many dimes $0.10 ? "))
    nickles = int(input("How many nickles $0.05 ? "))
    pennies = int(input("How many pennies $0.01 ? "))
    value = quarters * money_value["quarters"] + dimes * money_value["dimes"] + nickles * money_value["nickles"] + pennies * money_value["pennies"]
    return value


def change (val, coffe):
    """Checks how much to spend change"""
    how_much_to_spend = val - MENU[coffe]["cost"]
    return how_much_to_spend


def checkin_availability(w, m, c, coffe):
    not_enough = []
    if  w - MENU[coffe]["ingredients"]["water"] < 0:
        not_enough.append("Water")
    if coffe != 'espresso':
        if m - MENU[coffe]["ingredients"]["milk"] < 0:
            not_enough.append("Milk")
    if c - MENU[coffe]["ingredients"]["coffee"] < 0:
        not_enough.append("Coffee")
    return not_enough
    

    

    
# Flag
working_machine = True


while working_machine:
    coffe_pick = input(" What would you like? (espresso/latte/cappuccino): ").lower()
    if coffe_pick == 'espresso' or coffe_pick == 'latte' or coffe_pick == 'cappuccino':
            is_enough = checkin_availability(water_v, milk, coffee, coffe_pick)
            if len(is_enough) != 0:
                message = ', '.join(is_enough)
                print(f"Sorry there is not enough {message}")
            else:    
                money = give_me_money()
                in_change = round(change(money, coffe_pick), 2)
                if in_change >= 0:
                    print(f"Here is ${in_change} in change")
                    print(f"Here is your {coffe_pick} ☕️  Enjoy!")
                    R_money += money - in_change
                    water_v -= MENU[coffe_pick]["ingredients"]["water"]
                    coffee -= MENU[coffe_pick]["ingredients"]["coffee"]
                    if coffe_pick != 'espresso':
                        milk -= MENU[coffe_pick]["ingredients"]["milk"]
                else:
                    print("Sorry that's not enough money. Money refunded")
    elif coffe_pick == 'report':
        print(f"Water: {water_v}ml")
        print(f"Milk: {milk}ml")
        print(f"Coffe: {coffee}g")
        print(f"Money: ${round(R_money, 2)}")
    elif coffe_pick == 'off':
        working_machine = False

