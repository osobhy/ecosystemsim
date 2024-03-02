# Ecosystem Simulation: Predators & Preys
Simulation of Ecosystems: a Predator Prey Simulation

This project is a simulation of predators (red circles) and preys (green circles) in an ecosystem with food for prey (pink circles). 
The graphical interface depends on the module graphics.py by Zelle, please ensure it is installed before attempting to run the program.

# Simulation rules:

   I.    All animals move around randomly in a user-controlled environment and are spawned with 60 health points (predators spawn with 40 for balancing
         reasons).

   II.   All animals lose their energy by 0.1 each movement.
   
   III.  Preys depend on plants (indicated by pink circles) for eneregy, predators depend on preys.
   
   IV.   A predator eats a prey if they meet in close vicinity, a distance of 10, which increases said predator's energy by half of
         eaten prey's energy.
   
   V.    Prey eats food if it is in distance 12 from it
   
   VI.   Animals have a 70% chance of reproduction if their energy levels are equal to/above 85 and are in distance of 20 with
         another animal of the same kind to produce an offspring. 
   
   VII.  Animals die if their energy reaches zero.
   
   VIII. A prey gets all stored energy from the food it eats, food's energy is randomized from 2 to 6

# What the user can modify:
   
   I.    The runtime steps of the simulation, a.k.a its duration. (Suggested: 500)
   
   II.   The initial number of Preys and Predators to spawn at the beginning of the simulation. (Suggested: 40-300)
   
   III.  The probability of food spawning at the beginning of the simulation. (Suggested: 5-30%)
   
   IV.   The size of the simulation's graphical interface in pixels. (Suggested width x height ranges from 200x200 to 800x800)

# Reported output:
   - At the end of the program, an output is shown into the command console with the number of dead preys and predators, and 
     their respective reproductions.

# To keep in mind:
   - It takes a little long for predators to die (as the only thing that kills them is death by losing energy through motion) so
     I encourage over 500 steps!

# Known issues:
   - Screen freezes and does not respond if all animals die and there are still steps to process.
