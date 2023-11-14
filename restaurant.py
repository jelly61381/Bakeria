import random

#global variable star to keep track of points
star = 5

def update(num):
    """
    Keeps track of star rating throughout the game
    Args:
        num (int): number of points to deduct from the global variable star
    
    """
    global star
    star -= num

    if star == 0:
        print("Your Star Rating is:", star)
        print("Game Over!")
    else: 
        print("Your Star Rating is:", star)

def overBudget():
    """
    Update star rating until it is 0 if the user spends over their budget
    """
    global star
    while star != 0:
        star -= 1
    print("Your Star Rating is:", star)
    print("Game Over!")



def grocery(food):
    """
    Reads grocery text file and create dictionary where
    key is food item and value is price of the item

    Args:
        food (str): a path to the grocery file
    Returns:
        prices (dict): a dictionary where the key is the food item and the value is price of that item
    """
    prices = dict()
        
    with open(food, 'r') as foodItems:
            for line in foodItems:
                l = line.strip().split(',')

                fo = l[0]
                pr = l[1].strip().replace('$', '')

                prices[fo] = float(pr)
    return prices

def shop(file):
    """
    Reads recipe file, match the ingredients with the grocery file, ask user how much of each ingredient they want to buy, 
    and then display their total, list of ingredients and their amounts, balance, and star rating after making their selection

    Args:
        file (str): a path to the recipe file
    """

    status = False

    if star != 0:
        status = True

    #read grocery text file and matching food items necessary for recipe
    g = "grocery.txt"
    with open(file, 'r') as f:
    
        start = False
        ing = []
        #extract list of ingredients from file    
        for line in f:
            if 'Ingredients' in line:
                start = True
                continue
            if start:
                if '---' not in line:
                    ing.append(line.strip())
                else:
                    start = False

        #show how much of each ingredient is necessary for the recipe
        ingDict = {}
        for ingList in ing:
            parts = ingList.split(' ')
            num = int(parts[0])
            foodType = ' '.join(parts[1:])
            ingDict[foodType] = num
        
        #match list to grocery
        gmatch = grocery(g)

        match = {}
        for key in gmatch:
            if key in ingDict:
                match[key] = gmatch[key]

        print("You need to buy: \n")
        print(list(match.keys()))
        print()
        print("This is how much each item costs: \n")
        print(match)
        print()

        shop = {}
        original_balance = 20
        totalPrice = 0

        matchList = list(match.keys())

    print("Your budget is $20")
    #ask user how much of each ingredient they want to buy
    while status == True:
        for i in matchList:
            if star != 0:
                while True:
                    try:
                        quantity = float(input(f"How much of {i} do you want to buy? "))
                        if quantity < 0:
                            raise ValueError("Quantity must be a positive number.")
                        break
                    except ValueError as e:
                        print("Invalid number. Please enter a positive number.")

                shop[i] = quantity

                if quantity > ingDict[i]:
                    if star == 0:
                        update(0)
                        status = False
                    else:
                        print()
                        print("You bought too much " + i)
                        print("You lost one star")
                        update(1)
                        print()
                        
                elif quantity < ingDict[i]:
                    if star == 0:
                        update(0)
                        status = False
                    else:
                        print()
                        print("You bought too little " + i)
                        print("You lost one star")
                        update(1)
                        print()
                
                totalPrice += quantity * match[i]
            else:
                status = False        
        totalPrice = round(totalPrice,2)

        if star != 0:            
            print()
            print("You spent $" + str(totalPrice) + " on groceries \n")
            print("Here is what you have bought: \n")

            print(shop)
            print()

            balance = original_balance - totalPrice
            balance = round(balance,2)
            
        
            if balance < 0:
                print("You went over your budget.")
                print(f"Your balance is -${-balance}")
                overBudget()
                status = False
            else:
                print("Great Job! You stayed within budget!")
                update(0)
                print("Your balance is $" + str(balance))
                status = False
        status = False    
        
    
class Cook:
    """
    A class that represents the user and the recipes they need to make based on the "customer's" order.
        The user starts out with a 5 star rating and it decreases by 1 point every time they make a mistake.
        The game ends when they reach 0 stars.
        At the end of the game, their final star rating is displayed.

    Attributes:
        r (list of str): a list of instructions made from the recipe file

    """ 

    def __init__(self):
        """
        Initializes the attributes
        """
        self.r = list()   
    
    def recipe(self, f, n):
        """
        Reads recipe file and ask user to make the recipe.

        Args:
            f (string): a path to the recipe file
            n (int): a number that corresponds to the file name
        """
        status = False
        shop(f)

        if star > 0:
            print()
            print("Let's get cooking!\n")
            status = True

        # prints instructions as a list
        with open(f, 'r') as f:
            start = False
            for line in f:
                if 'Instructions' in line:
                    start = True
                    continue
                if start:
                    self.r.append(line.strip())

        while status == True:
            for l in self.r:
                w = l.split()
                fw = w[0]
                lineGuess = " ".join(w[1:])

                if star != 0:
                    print()
                    print("What should you do?: ___", lineGuess)
                    print()
                    print("Your options are:\nBoil / Mix / Melt / Whisk / Combine / Sprinkle / Add / Spread / Bake / Butter / Coat / Stir / Beat / Fold\n")
                    
                    #check if user input is valid word
                    while True:
                        guess = input("Your guess: ")
                        if guess.lower() in ['boil','mix', 'melt', 'whisk','combine', 'sprinkle', 'add','spread', 'bake', 'butter', 'coat', 'stir', 'beat', 'fold']:
                            break
                        else:
                            print("Invalid input. Please choose one of the provided options.")

                    print()

                    #check if user's guess matches with the first word in the line
                    if guess.lower() == fw.lower():
                        print("Correct!")
                    else:
                        if star == 0:
                            update(0)  
                            status = False
                        else: 
                            print("Incorrect. You are supposed to", l)
                            update(1)                         
            status = False
        if star != 0:
            print()
            if n == 1:
                print("Great job on making a Baked Mac and Cheese! Your final star rating is", str(star))
            elif n == 2:
                print("Great job on making a Pepperoni Pizza! Your final star rating is", str(star))
            else:
                print("Great job on making a Chocolate Soufflé! Your final star rating is", str(star))

        

    
def main():
    """Set up and play the cooking game"""
    c = Cook()
    status = False

    print("Welcome to Le's Kitchen!\nYou have been training with for quite some time now and we think you are ready to take your first order!")

    while True:
        try:
            gameSet = input("Do you want to take an order? y/n ")
            if gameSet.lower() == "y":
                break
            elif gameSet.lower() == "n":
                print("Ok. See you again next time!")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except:
            print("Invalid input. Please try again.")
    

    if gameSet == "y":
        status = True
    else:
        status = False


    while status == True:
        randChoice = random.randint(1,3)
        if randChoice == 1:
            print("\nYou have received an order to make Baked Mac and Cheese!\n")
            f = 'customer1.txt'
            return c.recipe(f,1)
            
        elif randChoice == 2:
            print("\nYou have received an order to make Pepperoni Pizza!\n")
            f = 'customer2.txt'
            return c.recipe(f,2)
        else:
            print("\nYou have received an order to make Chocolate Soufflé!\n")
            f = 'customer3.txt'
            return c.recipe(f,3)
        

if __name__ == "__main__":
    main()