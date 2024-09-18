# Introduction

Raj is a simple bidding game, where players using cards with assigned values (analogous to
money) bid on cards of assigned values (equivalent to items/prizes). In an N-card game,
there are N items to bid on and each player gets N cards to bid with. The order of items
to bid on is chosen at random. Players select the card to bid with, with all the player’s
bids revealed at the same time. The player with the highest unique bid wins and takes the
item. Bids that tie don’t count – if everyone has the same bid, the item is left on the table
adding its value to the next item to bid on. Item values can be negative, in which case the
player with the lowest unique bid takes them (i.e. when the pot is negative you bid not to
get it).

# My approach towards reinforcement learning

I utilized Temporal Difference Q-learning with softmax exploration to train an agent to learn to play Raj effectively. This method allows the agent to balance exploration of new strategies and exploitation of known successful strategies by probabilistically selecting actions based on their estimated values.

# Performance of my reinforcement learning agent 
![image](https://github.com/user-attachments/assets/8e728fe0-95e4-4c33-91ae-c6f3d23b1bd7)
![image](https://github.com/user-attachments/assets/38f1b5ff-3d20-4a8b-a4e3-e44167b943f3)

I have a win rate of 86% against (value_agent, valueplus_agent) and 63% against (random_agent, valueplus_agent). However, I only have a 46% win rate against (random_agent,random_agent) with the remaining 54% almost evenly split between being second place and being dead last. For the score, my agent has a higher score against every opponent in every scenario.

# Engine files
Download cosc343Raj.zip.  Extract it into your project folder.  You get several files:
* human_agent.py - agent that provides text based interface for human player
* my_rlagent.py - Reinforcement learning agent
* raj.py -the main game file - you run this script to run the game
* random_agent.py - agent that makes random bids
* settings.py - contains game settings, which you can change to run the game under various configurations
* value_agent.py - agent playing fixed strategy of betting the same value as the item (if possible)
* valueplus_agent.py - agent playing fixed strategy of betting next higher value over the one matching (if possible) the item value
* view-policy.py - prints out everything in policy.pkl in terminal for easy viewing
* policy.pkl - my best performing model that was trained using my_rlagent. If this file exists, my_rlagent will use the policy in this file to play the game. Delete this file to retrain the model
* The set of files gives you a completely working Python code for running the Raj game. You can also modify settings.py to reconfigure the game (for instance to change the agent script that is used to play the game).
  
# Running the code
You can run the simulation as it is, without changing any code. The default settings.py sets up a 6-bid game to be played by myrl_agent.py against value_agent.py and valueplus_agent.py on the item values (-2,-1,1,2,3,4) and with card values (1,2,3,4,5,6); played 100 time using random seed=0 (meaning, the same order of bids will be chosen when running raj.py multiple times). 

# Changing the game settings via settings.py
The file settings.py contains a (Python) dictionary object called "game_settings", with various entries.  You can change the game setting by modifying the values of those entries.
You can select the agents to play the game by setting the "agentFiles" entry - the agent scripts must be in the same folder as raj.py.
You can modify bidding card values by changing the "cardValues" entry; this must be a tuple of positive integers; the lenght of this tuple specifies the number of bids.
You can modify item values by changing the "itemValues" entry; it must be a tuple of integers, the length of this tuple specifies the number of bids (it must match the length of "cardValues".
You can change the total number of games played when running raj.py by setting the "toatNumberOfGames" entry.
You can make the game engine less verbose if you set the "verbose" entry to False.
You can change the "seed" for the choice of items selected for bidding; you can also set the "seed" to None, in which case the choice of solutions will be different on different runs of raj.py.

# How the code works
The script raj.py looks through settings.py and instantiate the game of Raj.  Then the game engine imports the RajAgent class from the agent files provided in game_settings['agentFiles'], instantiating RajAgent object from each agent.  Then, the script runs game_settings['totalNumberOfGames'] games.  For a given run of the game, the engine picks pesudo-random (according to game_settings['seed']) order of items to bid on and asks the agents to make their bids.  The engine calls the AgentFunction method of the respective players' RajAgent objects , passing in information about the value currently bidding on, agent's cards in-hand, items left ot bid on.  The AgentFunction is expected to return an integer value, which constitutes the agent's bid.  The engine checks that returned value against agent's hand (can't bid values you don't have).  The engine collects bids from all the players and resolves the bidding - winner of bidding on positive value gets that item added to their bank, loser of the bidding on negative value gets that item value added to thier bank.  In case of a tie, no one gets anything and the item value is added to the next bid.  In 3 or more player games, highest unique bid wins if other players tie (even if that bid is lower than the bids of those who tied).  The game is played game_settings['totalNumberofGames'] times tallying the avereage score per game.

# The environment
The environment for this game is a game state for N rounds of N-bid game. The
player/agent is provided information about the total value of items to bid on, everyone’s
cards and the items still left for later bidding. The agent action is to choose the card value
from their hand to make a bid.
The agent is scored over a series of games with the average obtained value of items per
game.

# Game parameters
For the purpose of development and testing, the game environment in this assignment
will have the following configurable parameters: a tuple of agents playing the game, tuple
listing card values (that each player starts the game with), tuple listing item values (to
bid on), number of games to play, and seed of the pseudorandom number generator (that
governs the order of items in the bidding). The number of entries in the agents tuple
determines the number of players – for this project it will be always three players. The
number of card values must match the number of item values.

# The agent function
The agent function is invoked to get the agent’s next guess. Its single argument is a tuple
of percepts, which provide information about the value currently being bid on, the values
of items remaining (to bid on later), the current hand/cards of this agent as well as the
other players’. The agent function needs to return an integer, one of the values from their
hand constituting the agent’s bid.

# Percepts
The percept of the Raj-playing agent is a tuple that contains several pieces of information:
* bidding on – int; value indicating the total value of items currently being bid on;
* items left – tuple; item values (not including the current bid) to bid on next.
* my cards – tuple; card values this agent is holding – the returned bid must be an integer from this set of values;
* bank – int; total values scored by this agent in this game so far.
* opponents cards – tuple; opponents’ cards; each hand is a tuple itself; in this project
there will be only three players, so this will be a tuple containing two tuples.

# Actions
The action of the agent is the choice of value from my cards, which constitutes the bid
on the current item(s). The last bid is made automatically (agents have no choice, since
they’re left with one card). To detect when a new game starts the agent can check the
length of the my cards – length of N in N card game means this is the first round.
