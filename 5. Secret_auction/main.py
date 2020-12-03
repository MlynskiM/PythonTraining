import os
from art import logo
#HINT: You can call clear() to clear the output in the console.
print(logo)
print("Welcome to the secret auction program.")

secret_list = []

should_continue = True
while should_continue:
  name_key = input("What is your name?: ")
  bid_key = input("What's your bid?: ")
  new_bid = {
    "name": name_key,
    "bid": bid_key,
  }
  secret_list.append(new_bid)
  decision = input("Are there any other bidders? Type'yes' or 'no'").lower()

  if decision == 'no':
    should_continue = False

  os.system('cls')



winner = ""
for i in range(0, len(secret_list)):
   if secret_list[i]["bid"] > secret_list[i-1]["bid"]:
     winner = secret_list[i]["name"]
   elif secret_list[i]["bid"] == secret_list[i-1]["bid"] :
    winner = secret_list[i]["name"],secret_list[i-1]["name"]
   else:
    winner = secret_list[i-1]["name"]

print(f"The winner is {winner}")