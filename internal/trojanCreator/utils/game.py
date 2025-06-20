import os
import random

def clearScreen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def main() -> None:
    guessed_numbers = 0
    while True:
        guess = 0
        number = random.randint(1, 1000)
        count = 0
        
        print("I've just generated a random number, now you have to guess it")
        while guess != number:
            guess = int(input("Enter the number: "))
            if guess > 1000:   
                print("Type an int number smaller than 1000")
                continue

            if guess == number:
                print("Correct, well done")
            
            elif guess < number:
                print("The number is bigger")

            elif guess > number:
                print("The number is smaller")
            
            count += 1

        guessed_numbers += 1
        
        print("You took " + str(count) + " attempts !!! ")
        print(f"Till now, you've guessed {guessed_numbers} numbers")
        input("Press enter to guess the next number")
        clearScreen()