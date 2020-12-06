from art import logo

def calc(operation_type, n1, n2):
  """ Function takes numbers and make operation on them"""
  result = 0
  if operation_type == '+':
    result = n1 + n2
  elif operation_type == '-':
    result =  n1-n2
  elif operation_type == '*':
    result =  n1*n2
  elif operation_type == '/':
    result =  n1/n2
  return result

operations = {
  "+": 1,
  "-": 2,
  "*": 3,
  "/": 4,
}


print(logo)



def calculation():
  """Recursion function """
  number_1 = float(input("What's the first number?: "))
  should_calculate = True
  while should_calculate:
    for i in operations:
      print(i)
    operation = input("Pick an operation: ")
    number_2 = float(input("What's the next number?: "))
    result = calc(operation_type = operation, n1 = number_1, n2 = number_2)
    print(f"{number_1} {operation} {number_2} = {result}")

    print(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation: ")
    decision = input()

    if decision == 'y':
      print(f"Your first number is : {result}")
      number_1 = result
    elif decision == 'n':
      should_calculate = False
      calculation()

calculation()

