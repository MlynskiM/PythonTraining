from art import logo, vs
from game_data import data
import random
from replit import clear


still_going = True
result = ''
score = 0



def random_person():
  return random.randint(0, len(data)-1)

def check(a, b):
  if data[a]["follower_count"] > data[b]["follower_count"]:
    return "A"
  else:
    return "B"


A = random_person()


while still_going:
  B = random_person()
  result = check(A, B)
  print(logo)
  if score > 0:
    print(f"You're right! Current score: {score}.")
  print(f"Compare A:{data[A]['name']}, {data[A]['description']}, from {data[A]['country']}. ")

  print(vs)

  print(f"Against B:{data[B]['name']}, {data[B]['description']}, from {data[B]['country']}.")

  type_f = input("Who has more followers? Type 'A' or 'B': ")
  if type_f == result:
    score += 1
    A = B
    clear()
  else:
    still_going = False

print(f"Sorry, that's wrong. Final score: {score}.")


  
