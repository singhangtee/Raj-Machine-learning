# Raj-Reinforcement-learning

Raj is a simple bidding game, where players using cards with assigned values (analogous to
money) bid on cards of assigned values (equivalent to items/prizes). In an N-card game,
there are N items to bid on and each player gets N cards to bid with. The order of items
to bid on is chosen at random. Players select the card to bid with, with all the player’s
bids revealed at the same time. The player with the highest unique bid wins and takes the
item. Bids that tie don’t count – if everyone has the same bid, the item is left on the table
adding its value to the next item to bid on. Item values can be negative, in which case the
player with the lowest unique bid takes them (i.e. when the pot is negative you bid not to
get it).

**The environment**
The environment for this game is a game state for N rounds of N-bid game. The
player/agent is provided information about the total value of items to bid on, everyone’s
cards and the items still left for later bidding. The agent action is to choose the card value
from their hand to make a bid.
The agent is scored over a series of games with the average obtained value of items per
game.

**Game parameters**
For the purpose of development and testing, the game environment in this assignment
will have the following configurable parameters: a tuple of agents playing the game, tuple
listing card values (that each player starts the game with), tuple listing item values (to
bid on), number of games to play, and seed of the pseudorandom number generator (that
governs the order of items in the bidding). The number of entries in the agents tuple
determines the number of players – for this assignment it will be always three players. The
number of card values must match the number of item values.

**The agent function**
The agent function is invoked to get the agent’s next guess. Its single argument is a tuple
of percepts, which provide information about the value currently being bid on, the values
of items remaining (to bid on later), the current hand/cards of this agent as well as the
other players’. The agent function needs to return an integer, one of the values from their
hand constituting the agent’s bid. The last round of the game is played automatically
(there is no choice to be made, since each player is left with one bidding card).

**Percepts**
The percept of the Raj-playing agent is a tuple that contains several pieces of information:
* bidding on – int; value indicating the total value of items currently being bid on;
* items left – tuple; item values (not including the current bid) to bid on next.
* my cards – tuple; card values this agent is holding – the returned bid must be an integer from this set of values;
* bank – int; total values scored by this agent in this game so far.
* opponents cards – tuple; opponents’ cards; each hand is a tuple itself; in this assignment
there will be only three players, so this will be a tuple containing two
tuples.

**Actions**
The action of the agent is the choice of value from my cards, which constitutes the bid
on the current item(s). The last bid is made automatically (agents have no choice, since
they’re left with one card). To detect when a new game starts the agent can check the
length of the my cards – length of N in N card game means this is the first round.
