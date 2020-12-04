from art import logo
import random
from replit import clear

should_continue = True

player_cards = []
computer_cards = []
player_score = 0
computer_score = 0
computer_dec = 0

def card_pick():
  cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
  card = random.choice(cards)
  return card

def score(list_score):

  if sum(list_score) == 21 and len(list_score)== 2:
    return 0
  
  if 11 in list_score and sum(list_score) > 21:
    list_score.remove(11)
    list_score.append(1)

  return sum(list_score)


def info(pc , ps , cd):
  return  print(f"  Your cards: {pc}, current score: {ps} \n  Computer's first card:{cd}")


def final(player_list, computer_list, score_p, score_c):
  final_result = ''
  player_final_info = print(f"  Your final hand: {player_list}, final score: {score_p}")
  computer_final_info = print(f"  Computer's final hand: {computer_list}, final score: {score_c}")
  if score_p == 0:
    final_result = "Blackjack! You win"
  elif score_p >21:
    final_result = "you went over. You lose"
  elif score_p > score_c and score_c < 21:
    final_result = "You win"
  elif score_p < score_c:
    final_result = "You Lose"
  elif score_p < score_c:
    final_result = "Draw!"
  final_result_info = print(f"{final_result}")
  return player_final_info, computer_final_info, final_result_info 
    
def play():

    player_score = score(player_cards)
    computer_score = score(computer_cards)

    if len(computer_cards) == 1:
      computer_dec = computer_cards[0]
    else:
      computer_dec = computer_cards
    info(player_cards, player_score, computer_dec)
    play_more= True

    while play_more:
      decision_pn = input("Type 'y' to get another card, type 'n' to pass: ")

      if decision_pn == 'n':
        while computer_score < 17:
          computer_cards.append(card_pick())
          computer_score = score(computer_cards)
        info(player_cards, player_score, computer_dec)
        play_more= False  
      elif decision_pn == 'y':
        player_cards.append(card_pick())
        player_score = score(player_cards)
        info(player_cards, player_score, computer_dec)

        if player_score  > 21:
          while computer_score < 17:
            computer_cards.append(card_pick())
            computer_score = score(computer_cards)
          play_more= False

    final(player_cards, computer_cards, player_score, computer_score) 


while should_continue:
  decision = input("Do you want to play game of Blackjack? Type'y or 'n'")
  player_cards = []
  computer_cards = []
  clear()
  if decision == 'n':
    should_continue = False
  print(logo)
  for _ in range(2):
    player_cards.append(card_pick())
  computer_cards.append(card_pick())
  play()
  
    

  

  


