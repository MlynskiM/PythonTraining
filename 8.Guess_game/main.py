from art import logo
import random

print(logo)
player_try = 0
attempts = 0

Numbers = []
for i in range(0,101):
    Numbers.append(i)

def random_number():
  thinking_about = random.choice(Numbers)
  return thinking_about

think = random_number()

def check(g, t):
  info = ""
  if g > t:
    info = "  Too High"
  elif g < t:
    info = "  Too Low "
  elif g == t:
    info = f"You got it! The answer was {t}"
  return info
  
def dif_check(d):
  a = 0
  if d == "hard":
    a = 5
  elif d == "easy":
    a = 10
  return a




print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ")

attempts = dif_check(difficulty)

print(f"You have {attempts} attempts remaining to guess that number.")

while player_try != attempts:
  guess = int(input("Make a guess: "))
  result = check(guess, think)
  print(result)
  if result == f"You got it! The answer was {think}":
    break
  player_try += 1
  if player_try < attempts:
    print("Guess again.")

if player_try == attempts:
  print("You've run out of guesses, you lose.")


  

