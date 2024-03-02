# Author: Omar Sobhy
# Predator and Prey Ecosystem Simulation

# Importing the necessary modules..
from graphics import *
import random
import math

class Simulation:
    def __init__(self, numPrey, numPredator, runtime, environment, foodProbability): # Initializing the simulation with various user-controlled attributes
        self.numPrey = numPrey
        self.numPredator = numPredator
        self.runtime = runtime
        self.environment = environment
        self.foodProbability = foodProbability / 10000
        # Creating counters to keep track of dead (and reproduced) preys and predators to show them to the user after simulation finishes running.
        self.preysDied = 0
        self.predatorsDied = 0 
        self.predatorReproduced = 0
        self.preyReproduced = 0

    # To randomize food location, for every single pixel on the screen, there is going to be a user-input probability of food of 
    # energy 1 to 3 in that location.
    def foodGenerator(self):
        for i in range(self.environment.width):
            for j in range(self.environment.height):
                random_number = random.random()            # Gets a number between 0, 1.
                if random_number < self.foodProbability:   # If the number between 0, 1 is less then the user input probability, generate food.
                    foodHealth = random.randrange(2, 6, 1) # Food's energy ranges between 2 and 6.
                    food = Food(foodHealth, i, j, self.environment)      # A new food object with the prescribed attributes is created.
                    self.environment.add_food(food)                      # The new food object is added to the list of foods in the environment.
    # The function that runs the logic of the simulation 
    def run(self): # running the simulation
        self.environment.screenDraw("Predator / Prey Simulation") # This draws the screen and sets its title
        self.foodGenerator() # Function that randomly generates food throughout the grid

        # The below loop iterates over food classes that are present in the foods list present in the environment class 
        # to draw it as a pink rectangle resembling a flower (need to make it more interesting?)
        for food in self.environment.foods:
            food.foodDraw()
        
        # Creating prey & predator, adding to environment's class's list of animals
        for i in range(self.numPrey):
            preyS = Prey(60, random.randint(0, self.environment.width), random.randint(0, self.environment.height), True, self.environment)
            self.environment.add_animal(preyS)
        for i in range(self.numPredator):
            predatorS = Predator(40, random.randint(0, self.environment.width), random.randint(0, self.environment.height), True, self.environment)
            self.environment.add_animal(predatorS)

        # What happens every time step is initialized here
        for i in range(self.runtime):
            # The below loop loops through the animals list to move each one of them and they lose 0.1 energy every movement
            for animal in self.environment.animals:
                animal.move()
                animal.energy = animal.energy - 0.1
                # Graphically representing prey and predator
                # Checks if an animal is prey or predator for every animal inside the animals list then graphically represents it
                if isinstance(animal, Prey) and animal.alive: 
                    animal.preyDraw()
                elif isinstance(animal, Predator) and animal.alive: 
                    animal.predatorDraw()

                # If animal is prey, it forages. If animal is predator, it hunts prey. If animal.hunt() is called, prey is dead (animal.die()
                # is called on it)
                if isinstance(animal, Prey):
                    animal.forage(self.environment.foods)
                elif isinstance(animal, Predator):
                    animal.hunt(self.environment.animals)

                # If animal has no energy and is assigned alive, it means the animal is dead by movement
                # which means animal.die() was never called on it as it was never actually hunted
                # so this check makes sure it is dead (aka animal.alive becoming false and it being undrawn)
                if (animal.energy <= 0) and (animal.alive == True):
                    animal.die()
                # If animal.alive is false, it means it is dead by either movement or being hunted (if it's prey)
                # therefore what happens is that it gets removed from the animals list to prevent it being recreated
                # and adds to the counter of dead preys/predators to tell the user at the end
                if (animal.alive == False):
                    if isinstance(animal, Predator):
                        self.predatorsDied += 1
                        self.environment.animals.remove(animal)

                    elif isinstance(animal, Prey):
                        self.preysDied += 1
                        self.environment.animals.remove(animal)

                # If animal energy is bigger than or equal 85, there is a 70% chance of it reproducing if it is in distance ~20 with another animal
                # as a result, another animal is added to the list of new animals that has the same kind (predator/prey), then appended to the
                # original animals list.
                if animal.energy >= 70:
                        new_animals = [] # Creating a new animals list to keep track of reproduced animals
                        random_number = random.random()
                        if random_number < 0.85:
                            for animal2 in self.environment.animals:
                                new_animal = None   # Got an "UnboundLocalError" because sometimes new_animal was not associated with a value, so
                                                    # I made this check that is further checked in the conditional below
                                if isinstance(animal2, Prey) and isinstance(animal, Prey):
                                    if math.dist([animal.x, animal.y], [animal2.x, animal2.y]) <= 20: # If two animals have distance <= 20, they reproduce
                                        new_animal = animal.reproduce()
                                        animal.energy = animal.energy/2 # Energy is halved after reproduction
                                        self.preyReproduced += 1

                                if isinstance(animal2, Predator) and isinstance(animal, Predator): 
                                    if math.dist([animal.x, animal.y], [animal2.x, animal2.y]) <= 20:
                                        new_animal = animal.reproduce()
                                        animal.energy = animal.energy/2 # Energy is halved after reproduction
                                        self.predatorReproduced += 1

                                if new_animal is not None: # Check for the existence of new_animal to avoid UnboundLocalError. Was very agonizing to fix.
                                    new_animals.append(new_animal)
                        
                            for new_animal in new_animals:              # Add every animal from the new_animals list to the original animals list
                                self.environment.add_animal(new_animal) # so the simulation would iterate and represent them graphically.
        # Closing the window when simulation is done
        self.environment.win.close()
        # Printing results for the user to study
        print()
        print("Results:")
        print("Number of preys died:", self.preysDied)
        print("Number of predators died:", self.predatorsDied)
        print("Number of prey reproductions:", self.preyReproduced)
        print("Number of predator reproductions:", self.predatorReproduced)

class Environment:
    def __init__(self, width, height): # Physical attributes of the window in pixels
        self.width = width
        self.height = height
        self.animals = []     # List of animals in the environment
        self.foods = []       # list of foods in the environment
    
    # Graphically representing screen
    def screenDraw(self, win):
        self.win = win
        self.win = GraphWin(self.win, self.width, self.height) # Drawing the graphical interface
        self.win.setBackground("light green")                  # Setting the color of the background

    # Adding animals to the list
    def add_animal(self, animal):
        self.animals.append(animal)
    
    # Adding foods to the list
    def add_food(self, food):
        self.foods.append(food)

class Food:
    def __init__(self, energy, posX, posY, environment): # Defining food location and its specified energy. Taking win as an attribute 
        self.x = posX                                    # cause it is used to draw.
        self.y = posY
        self.energy = energy
        self.environment = environment
    
    def foodDraw(self): # Method to graphically represent food WITHIN the class, as per requested, haha.
        self.foodShape = Circle(Point(self.x, self.y), 3) 
        self.foodShape.setFill("pink") # Food is a pink circle with radius 3
        self.foodShape.draw(self.environment.win) 
    
    def consume(self): # If food is consumed, essentially its energy becomes zero and it is undrawn and removed from foods list
        self.energy = 0
        self.foodShape.undraw()
        self.environment.foods.remove(self)

# Below is the parent Animals class that both Predator and Prey inherit from
class Animals:
    def __init__(self, energy, posX, posY, alive, environment): # Basic animal attributes such as location, energy and state and initial lack of shape.
        self.energy = energy
        self.x = posX
        self.y = posY
        self.alive = alive
        self.shape = None
        self.environment = environment
    
    # Movement logic - equal chance of 1/4 of moving in any direction, movement step randomized from 5 to 9
    def move(self):
        if self.shape:
            self.shape.undraw()          # Undrawing old shape as to not leave a "trail".

        # Storing old values of x and y before movement
        old_x = self.x 
        old_y = self.y
        movement = random.randint(1, 4)
        if movement == 1 and self.x < self.environment.width - 10: # Making sure the animals do not move off-screen - if they get close to the screen's 
            self.x = self.x + random.randint(5,9)                  # width, this evaluates to false and therefore does not let them move in the direction
        elif movement == 2 and self.x > 5:                         # where they go off screen. I used similar logic for the rest of conditions.
            self.x = self.x - random.randint(5,9)
        elif movement == 3 and self.y < self.environment.height - 10:
            self.y = self.y + random.randint(5,9)
        elif movement == 4 and self.y > 5:
            self.y = self.y - random.randint(5,9)
        dx = self.x - old_x # Calculating the change of x and y because Zelle's movement logic depends on the change
        dy = self.y - old_y
        if self.shape:      # If that shape exists, move it dx in x direction and dy in y direction
            self.shape.move(dx, dy)

    # Death means no energy and their state of living is False - then they get undrawn.
    def die(self):
        self.energy = 0
        self.alive = False
        self.shape.undraw()
        
# Prey is a child class of Animals that has Prey-specific functions/methods
class Prey(Animals):
    def __init__(self, energy, x, y, alive, environment): # Inheriting all attributes from Animals class
        super().__init__(energy, x, y, alive, environment)

    # If food is at the exact same location as prey, it eats it.
    def forage(self, foods):
        for food in foods:
            if math.dist([self.x, self.y], [food.x, food.y]) <= 12:
                self.eat(food) 
    
    # Eating food makes Prey gain the food's energy and consumed the food
    def eat(self, food):
        self.energy = self.energy + food.energy
        food.consume()
    
    # Graphically representing prey
    def preyDraw(self):
        self.shape = Circle(Point(self.x, self.y), 5)
        self.shape.setFill("green")
        self.shape.draw(self.environment.win)

    # Reproduction returns new animal of the same kind and a set energy of 60
    def reproduce(self):
        return Prey(60, self.x, self.y, True, self.environment)

# Predator is a child class of the animals class that has Predator-specific functions/methods
class Predator(Animals):
    def __init__(self, energy, x, y, alive, environment):
        super().__init__(energy, x, y, alive, environment) # Inheriting all attributes from Animals class
        
    # A check to make sure prey is alive before eating it, then kills it. Predator gains half of prey's energy when it eats it.
    def eat(self, prey): 
        if prey.alive:
            self.energy = self.energy + prey.energy / 2
            prey.die()
    
    # If a Prey meets Predator at a distance of 10 (both conditions evaluating to True), it eats it
    def hunt(self, animals):
        for animal in animals:
            if isinstance(animal, Prey) and math.dist([self.x, self.y], [animal.x, animal.y]) <= 10:
                self.eat(animal)
    
    # Graphically representing predator
    def predatorDraw(self):
        self.shape = Circle(Point(self.x, self.y), 5)
        self.shape.setFill("red")
        self.shape.draw(self.environment.win)
    
    # Reproduction returns new animal of the same kind at the same location and a set energy of 60
    def reproduce(self):
        return Predator(60, self.x, self.y, True, self.environment)

# Getting user inputs..
while True:
    try:
        envWidth = int(input("How wide do you want your environment to be? (Suggested value 200-800) "))
        envHeight = int(input("How high do you want your environment to be? (Suggested value 200-800) "))
        numOfPrey = int(input("How many initial preys do you want there to be? (Suggested number: 40-100) "))
        numOfPredator = int(input("How many initial predators do you want there  to be? (Suggested number: 40-100) "))
        break
    except:
        print("Oops! Gotta be an integer. Try again!")

while True:
    try:
        ProbOfFood = float(input("What do you want the probablity of food existence to be in %? (Suggested value between 5-35%) "))
        break
    except:
        print("Oops! That is an invalid number.")

while True:
    try:
        runtimeSteps = int(input("How many steps do you want to simulate? (Suggested steps: 500) "))
        break
    except:
        print("Oops! Gotta be an integer.")

Environment1 = Environment(envWidth, envHeight)
Simulation1 = Simulation(numOfPrey, numOfPredator, runtimeSteps, Environment1, ProbOfFood)
Simulation1.run()