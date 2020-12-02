import random
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

player_pick = int(input('What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n'))

value_array = []

if(player_pick == 0):
  print(rock)
  value_array = [0]
elif(player_pick == 1):
  print(paper)
  value_array = [1]
elif(player_pick == 2):
  print(scissors)
  value_array = [2]
else:
  print("You pick wrong number !!! ")

computer_pick = random.randint(0, 2)
print("\n Computer pick: ")
print(computer_pick)
if(computer_pick == 0):
  print(rock)
  value_array.append(0)
elif(computer_pick == 1):
  print(paper)
  value_array.append(1)
elif(computer_pick == 2):
  print(scissors)
  value_array.append(2)


winning_combination = [[0,2], [1,0], [2,1]]
loosing_combination = [[0,1],[1,2],[2,0]]
draw_combination = [[1,1],[2,2],[0,0]]

if(winning_combination[0]== value_array or winning_combination[1]== value_array or winning_combination[2]== value_array ) :
  print("You Won !")
elif(loosing_combination[0]== value_array or loosing_combination[1]== value_array or loosing_combination[2]== value_array ) :
  print("You Lost !")
elif(draw_combination[0]== value_array or draw_combination[1]== value_array or draw_combination[2]== value_array ) :
  print("Draw!!")
else:
  print("err")
