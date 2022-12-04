import os
import random
import time

def initialize():
    guessed_numbers = 0
    while True:
        number = random.randint(1, 1000)
        count = 0
        correct = False
        
        print("I've just generated a random number, now you have to guess it")
        while correct != True:
            try:
                guess = int(input("Enter the number: "))
                if guess > 1000:
                    raise ValueError
            except ValueError:
                print("Type an int number smaller than 1000")
                continue

            if guess == number:
                correct = True
                print("Correct, well done")
            
            elif guess < number:
                print("The number is bigger")

            elif guess > number:
                print("The number is smaller")
            
            count += 1

        guessed_numbers += 1
        
        print("You took " + str(count) + " attempts !!! ")
        print(f"Till now, you've guessed {guessed_numbers} numbers")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")