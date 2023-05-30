# ASSIGNMENT

# Requirements

Project is written in python 3.11, with use of poetry for dependency management.
To set up project:

```poetry shell```

```poetry install```

# Structure

Project is divided into 3 main parts:

* main loop, for interacting with user
* Random number generator protocols
* Abstraction of functionality of slot machine

## main.py

This file contains arg parser used for interacting with program.
If no arguments are passed, program will run in interactive mode, an interactive game of slot machines .
example:

```poetry run python main.py```

or,

```make game```

To run simulate:

```poetry run python main.py --simulate --revolutions <n>```

or,

```make simulate```

### Game 
Game is based on curses Terminal User Interface. User is provided with information about controls (q to quit, space to spin), amount of credits available and current state of slot machine.

### Simulation
Simulation is run in parallel according to machine specification, or as set using ```number_of_workers``` parameter in simulate function. Progress is showed live using tqdm progress bar. At the end there is sum of bet and sum of wins displayed.


## Slot machine
Slot machine abstraction is enclosed in SlotMachine class. Design is generic, size and number of reels can be set in constructor. Number of symbols can also be changed, easily, but it requires adding int-> symbol mapping and mapping of prizes. 
Game logic at this point is hardcoded, but can be easily changed by modifying ```_evaluate_points``` method (ideally this part of logic could be extracted and passed as dependency injection, similarly to RNG part). 
Game state is kept inside SlotMachine object. In order to play, method ```play``` need to be called on object, it represents one spin in a game.
Random number generator is passed as a dependency injection.

## Random number generator
Random number generator is abstracted as protocol, where it is required to implement ```get_random_number``` method. This method should return random number in range m to n (where m and n can be passed while calling method).
Only SecretRandomIntGenerator is implemented at this point, which is based on ```secrets``` module. It may not be the best way to generate random numbers, but it is cryptographically secure and should be good enough for sake of supplying working example.

From the lack of time I decided to stop research there, if needed i can supply better implementation and refactor code to higher standard. And maybe supply more advanced analysis of outcome in simulation, which i think may be interesting.