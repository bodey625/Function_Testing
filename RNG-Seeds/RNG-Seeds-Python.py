import os
import random

print("\nHello, World! and welcome to this extremely basic example program")
print("the purpose of this is to demonstrate RNG seed generation, loading " + 
      "specific RNG seeds, and incrementing RNG seeds. \n")

# Copies the operating systems provided random for use as a seed, could probably
# use the built in function of the time = seed, but this is more secure, if needed
random_data = os.urandom(8)
seed = int.from_bytes(random_data, byteorder="big")

rng = random
rng.seed(seed)

while True:
    print("The current RNG Seed is   " + str(seed))
    print("enter 0 to exit program | 1 to enter a new seed | 2 to increment seed('2 x' will print x values)")
    userInput = input()
    print()

        # Option 0: Terminates the program
    if userInput[0] == "0": 
        print("Exiting program")
        break

        # Option 1: Allows User to Set Seed
    if userInput[0] == "1":
        if userInput[2:]:
            newSeed = userInput[2:]
        else:
            print("Enter your seed:")
            newSeed = input()

        rng.seed(newSeed)
        seed = newSeed

        # Option 2: Allows user to print out random values, up to x default 1
    if userInput[0] == "2":
        x = 1
        if userInput[1:]: 
            try: 
                x = int(userInput[2:])
            except ValueError:
                print("Oi! use an integer. defaulting to 1")

        for i in range(x):
            print(rng.randint(1, 1000), end='   ')

    print('\n')
