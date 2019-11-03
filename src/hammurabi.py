#
# hammurabi.py
#
#/******************************************************************************
# **                                                                          **
# ** Hammurabi. Translated from the original DEC BASIC                        **
# **                                                                          **
# ** adopted to Python by Andreas Grimm <andreas.grimm@gricom.eu              **
# **                                                                          **
# ** Original program 1968 by Doug Dyment (in Focal)                          **
# **              and 1971 by David H. Ahl (in DEC Basic)                     **
# **                                                                          **
# ******************************************************************************
#
# Basic version of the game: https://www.atariarchives.org/basicgames/showpage.php?page=79
import random
from infrastructure import common

_POPULATION_DEFAULT_  = 100
_LAND_DEFAULT_ = 1000
_FOOD_DEFAULT_ = 2800
_PRICE_DEFAULT_ = 20

class Player():
    def __init__(self, yearNumber, population, land, food, priceOfLand):
        self.yearNumber = yearNumber
        self.population = population
        self.land = land
        self.food = food
        self.priceOfLand = priceOfLand

    # Print player's variable
    def printPlayer(self):
        print ("-------------------------------------------")
        print ("Year:             {}".format(self.yearNumber))
        print ("Acres of land:    {}".format(self.land))
        print ("Population:       {}".format(self.population))
        print ("Stored grain:     {}".format(self.food))
        print ("Price of land:    {}\n".format(self.priceOfLand))

    # Print the report after each turn
    def printReport(self):
        print ("\nO great Hammurabi!")
        print ("You are in year {} of your ten year rule.".format(self.yearNumber))
        print ("In the previous year {} people starved to death.".format(self.starvingNumber))
        print ("In the previous year {} people entered the kingdom.".format(self.immigrantNumber))
        if self.plagueNumber > 0:
            print ("The plague killed half the people.")
        print ("The population is now {}".format(self.population))
        print ("We harvested {} bushels.".format(self.harvestNumber))
        print ("Rats destroyed {} bushels, leaving {} bushels in storage.".format(self.ratNumber, self.food))
        print ("The city owns {} acres of land.".format(self.land))
        print ("Land is currently worth {} bushels per acre.".format(self.priceOfLand))

    # Each year, there is a 15% chance of a horrible plague.
    # When this happens, half your people die.
    # Return the number of plague deaths
    def getPlagueDeath(self):
        chance = random.randint(1, 15)
        if chance == 1:
            return int(self.population / 2)
        
        return 0

    # Each person needs 20 bushels of grain to survive.
    # If you feed them more than this, they are happy, but the grain is still gone. You don't get any benefit from having happy subjects.
    # Return the number of deaths from starvation (possibly zero).
    def getStarvingDeath(self, food):
        numberFeedPeople = food / 20
        if numberFeedPeople > self.population:
            return 0

        return int(self.population - numberFeedPeople)

    # Return true if more than 45% of the people starve.
    # (This will cause you to be immediately thrown out of office, ending the game.)
    def isUprising(self):
        percentStarving = float(self.starvingNumber / self.population)
        if percentStarving > 0.45:
            return True

        return False

    # Nobody will come to the city if people are starving.
    # If everyone is well fed, compute how many people come to the city as:
    # (20 * number of acres you have + amount of grain you have in storage) / (100 * population) + 1.
    def getImmigrant(self):
        if self.starvingNumber > 0:
            return 0

        return int((20 * self.land + self.food) / (100 * self.population) + 1)

    # Choose a random integer between 1 and 6, inclusive.
    # Each acre that was planted with seed will yield this many bushels of grain.
    # (Example: if you planted 50 acres, and your number is 3, you harvest 150 bushels of grain).
    # Return the number of bushels harvested.
    def getHarvest(self, seed):
        landChance = int(self.land / 1000.0)
        chance = random.randint(1, 6)
        chance *= chance * landChance

        return seed * chance

    # There is a 40% chance that you will have a rat infestation.
    # When this happens, rats will eat somewhere between 10% and 30% of your grain.
    # Return the amount of grain eaten by rats (possibly zero).
    def getEatenByRat(self):
        chance = random.randint(0, 3)
        if (chance == 0):
            chanceEatAmount = random.randint(10, 30)
            foodEaten = self.food * float(chanceEatAmount) / 100.0
            return foodEaten
        return 0


    # The price of land is random, and ranges from 17 to 23 bushels per acre.
    # Return the new price for the next set of decisions the player has to make.
    def getNewPrice(self):
        chance = random.randint(1, 6)
        return chance + 17

    # update on every turn
    #
    def updatePlayer(self, land, food, seed):
        # update the remaining stats first, then calculate all the random elements
        self.food -= food
        self.food -= seed
        self.land += land

        self.food -= land * self.priceOfLand

        self.starvingNumber = self.getStarvingDeath(food)
        self.immigrantNumber = self.getImmigrant()
        self.plagueNumber = self.getPlagueDeath()
        self.harvestNumber = self.getHarvest(seed)

        self.population -= self.plagueNumber
        self.population -= self.starvingNumber

        self.population += self.immigrantNumber

        self.food += self.harvestNumber
        self.ratNumber = self.getEatenByRat()
        self.food -= self.ratNumber

        self.priceOfLand = self.getNewPrice()

        self.yearNumber += 1

        if self.population <0:
            self.population = 0


def main():
    myPlayer = Player(1, _POPULATION_DEFAULT_, _LAND_DEFAULT_, _FOOD_DEFAULT_, _PRICE_DEFAULT_)
    myPlayer.printPlayer()
    
    winner = True
    
    # loop for 10 years
    for counter in range(10):
        getInput(myPlayer)

        if checkEndGame(myPlayer):
            winner = False
            print ("GAME OVER")
            return

        myPlayer.printReport();
        myPlayer.printPlayer();

    if winner == True:
        print ("You have kept your people alive and 'well' for 10 years!")
        print ("You are truly great!")
        print ("CONGRATULATIONS")

    return

# Getting input from user and validating
def getInput(myPlayer):

    doubleCheck = 'N'
    
    while doubleCheck == 'N' or doubleCheck == 'n':
        foodRemaining = myPlayer.food

        invalid = True
        while invalid == True:
            land = common.Numbers.inputInt("How many acres do you wish to buy (Negative to sell)? ")

            if (myPlayer.food < (land * myPlayer.priceOfLand)):
                print ("You can't buy {} acres, you only have {} bushels!").format(land, myPlayer.food)
            else:
                invalid = False

        foodRemaining -= land * myPlayer.priceOfLand

        invalid = True
        while invalid == True:
            food = common.Numbers.inputInt("How many bushels do you wish to feed your people? ")

            if food < 0:
                print ("You can't feed people a negative amount of food!")
            elif food > foodRemaining:
                print ("You can't use {} bushels, you only have {} left!".format(food, foodRemaining))
            else:
                invalid = False

        foodRemaining -= food

        invalid = True
        while invalid == True:
            seed = common.Numbers.inputInt("How many acres do you wish to plant with seed? ")

            if seed < 0:
                print ("You can't plant a negative amount of seeds!")
            elif seed > foodRemaining:
                print ("You can't plant {} seeds, you only have {} left!".format(seed, foodRemaining))
            else:
                invalid = False

        foodRemaining -= seed

        print ("You wish to buy {} acres, feed your people {} bushels, and plant {} seeds.".format(land, food, seed))
        print ("This will leave you with {} bushels, is that correct?".format(foodRemaining))
        doubleCheck = input("Enter N to retry. ")

    myPlayer.updatePlayer(land, food, seed)

def checkEndGame(myPlayer):
    if (myPlayer.isUprising() or myPlayer.population == 0):
        print ("Due to EXTREME missmanagement, {} have starved!".format(myPlayer.starvingNumber))
        if (myPlayer.population == 0):
            print ("What a terrible ruler; you have no people left to rule!")
        else:
            print (" The remaining population has overthrown you and you have been declared the worst King in history!")

        return True

    return False

main()
