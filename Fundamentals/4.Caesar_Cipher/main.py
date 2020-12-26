from art import logo

def cesar(plain_text, shift_amout,func):
  end_text = ""
  if func == "decode":
    shift_amout *= -1
  for i in plain_text:
    if i in alphabet:
      position = alphabet.index(i)
      new_position = position + shift_amout
      end_text += alphabet[new_position]
    else:
      end_text += i
  print(f"The {func}d text is: {end_text}")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

print(logo)

should_continue = True
while should_continue:

  direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
  text = input("Type your message:\n").lower()
  shift = int(input("Type the shift number:\n"))

  shift = shift % 25

    

  cesar(plain_text = text, shift_amout = shift, func = direction)

  result = input("Type 'yes' if you want to go again. Otherwise type 'no' .\n")
  if result == 'no':
    should_continue = False

print("GoodBye!!")

