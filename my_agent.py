__author__ = "Singhang Tee"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "teesi625@student.otago.ac.nz"

import numpy as np

agentName = "minimax_agent"

class RajAgent():
    """
    A class that encapsulates the code dictating the
    behaviour of the agent playing the game of Raj.

    ...

    Attributes
    ----------
    item_values : list of ints
        values of items to bid on
    card_values: list of ints
        cards agent bids with

    Methods
    -------
    AgentFunction(percepts)
        Returns the card value from hand to bid with
    """

    def __init__(self, item_values, card_values):
        """
        :param item_values: list of ints, values of items to bid on
        :card_values: list of ints, cards agent bids with
        """

        self.card_values = card_values
        self.item_values = item_values

    def AgentFunction(self, percepts):
        """Returns the bid value of the next bid

        :param percepts: a tuple of four items: bidding_on, items_left, my_cards, opponents_cards

                , where

                bidding_on - is an integer value of the item to bid on;

                items_left - the items still to bid on after this bid (the length of the list is the number of
                            bids left in the game)

                my_cards - the list of cards in the agent's hand

                bank - total value of items in this game
                
                opponents_cards - a list of lists of cards in the opponents' hands, so in two player game, this is
                                a list of one list of cards, in three player game, this is a list of two lists, etc.


        :return: value - card value to bid with, must be a number from my_cards
        """
        bidding_on = percepts[0]
        items_left = percepts[1]
        my_cards = percepts[2]
        bank = percepts[3]
        opponents_cards = percepts[4:]
        oppo_bank = 0

        if len(my_cards) == 1:
            return my_cards[0]
        
        depth = 2
        best_value = -float('inf')
        
        for move in my_cards: 
            value = self.minimax(percepts, move, depth, False, oppo_bank)
            if value > best_value:
                best_value = value
                best_move = move
                        
        return best_move
    

    def minimax(self, percepts, my_move, depth, maxAgent, oppo_bank):
        bidding_on = percepts[0]
        items_left = percepts[1]
        my_cards = percepts[2]
        bank = percepts[3]
        opponents_cards = percepts[4:]

        if self.terminal(percepts) or depth < 0:
            return self.evaluate(percepts, oppo_bank)

        
        if maxAgent:
            bestVal = -10000

            for card in my_cards:

                for bid in items_left:
                    new_bidding_on = bid + bidding_on

                    new_percept = (new_bidding_on, percepts[1], percepts[2], percepts[3], percepts[4])
                    val = self.minimax(new_percept, card, depth, False, oppo_bank)

                    bestVal = max(bestVal, val)

            return bestVal
        
        else:
            bestVal = 10000

            for card in opponents_cards[0]:

                new_percept, oppo_bank = self.update_state(bidding_on, card, percepts, my_move, oppo_bank)
                val = self.minimax(new_percept, card, depth-1, True, oppo_bank)
                bestVal = min(bestVal, val)
            return bestVal



    def update_state(self, new_bid, card, percepts, my_move, oppo_bank):
        bidding_on, items_left, my_cards, bank, opponents_cards = percepts

        new_bank = bank
        new_oppo_bank = oppo_bank

        if my_move > card and bidding_on > 0:
            new_bank += bidding_on
        elif my_move < card and bidding_on < 0:
            new_bank += bidding_on

        if my_move > card and bidding_on < 0:
            new_oppo_bank += bidding_on
        elif my_move < card and bidding_on > 0:
            new_oppo_bank += bidding_on
        
        items_left = list(items_left)
        my_cards = list(my_cards)
        opponents_cards = list(opponents_cards)

        if new_bid in items_left:
            items_left.remove(new_bid)
        if my_move in my_cards:
            my_cards.remove(my_move)
        if card in opponents_cards:
            opponents_cards.remove(card)

        new_items_left = tuple(items_left)
        new_my_cards = tuple(my_cards)
        new_opponents_cards = tuple(opponents_cards)

        if (card != my_move):
            bidding_on = 0

        return (bidding_on, new_items_left, new_my_cards, new_bank, new_opponents_cards),new_oppo_bank
    
    
    def terminal(self, percepts):
        return len(percepts[2]) == 0


    def evaluate(self, percepts, oppo_bank):
        """
        Evaluate the game state using a heuristic function that includes the bank value.

        :param percepts: A tuple (bidding_on, items_left, my_cards, bank, opponents_cards)
        :return: A heuristic score for the current game state.
        """

        bidding_on = percepts[0]
        items_left = percepts[1]
        my_cards = percepts[2]
        bank = percepts[3]
        opponents_cards = percepts[4:]
        
        if self.terminal(percepts):
            if(oppo_bank > bank):
                return -999
            elif(oppo_bank < bank):
                return 999
            else:
                return 0
            
        # Initialize heuristic score
        score = 0

        # Initialize the count of differences
        count = 0
        sorted_my_cards = sorted(my_cards)
        sorted_opponents_cards = sorted(opponents_cards[0])

        # Iterate through the sorted list and sorted tuples
        for i in range(len(sorted_my_cards)):
                if my_cards[i] > sorted_opponents_cards[i]:
                    count += 1
                elif my_cards[i] < sorted_opponents_cards[i]:
                    count -= 1

        score += count

        bank_difference = bank - oppo_bank
        score += bank_difference * len(items_left)

        return score

