__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"


import numpy as np
import sys
import readchar

class bcolors:
   RED = '\033[1;30;41m'
   GREEN = '\033[1;30;42m'
   YELLOW = '\033[1;30;43m'
   BLUE = '\033[1;30;44m'
   PURPLE = '\033[1;30;45m'
   CYAN = '\033[1;30;46m'
   ENDC = '\033[0m'

def print_colour_value(d,c):
   if c == 'B':
      sys.stdout.write(f"{bcolors.BLUE}%d{bcolors.ENDC}" % d)
   elif c == 'R':
      sys.stdout.write(f"{bcolors.RED}%d{bcolors.ENDC}" % d)
   elif c == 'G':
      sys.stdout.write(f"{bcolors.GREEN}%d{bcolors.ENDC}" % d)
   elif c == 'Y':
      sys.stdout.write(f"{bcolors.YELLOW}%d{bcolors.ENDC}" % d)
   elif c == 'C':
      sys.stdout.write(f"{bcolors.CYAN}%d{bcolors.ENDC}" % d)
   elif c == 'P':
      sys.stdout.write(f"{bcolors.PURPLE}%d{bcolors.ENDC}" % d)
   else:
       sys.stdout.write("%d" % d)
   sys.stdout.flush()

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

   def __init__(self, card_values, item_values):
      """
      :param item_values: list of ints, values of items to bid on
      :card_values: list of ints, cards agent bids with
      """

      self.card_values = card_values
      self.item_values = item_values

      cards = np.unique(self.card_values)
      cards = np.sort(cards)
      colours = ['Y','G','C','B','P','R']
      colstep = int(np.floor(len(colours)/len(cards)))
      if colstep < 1:
         colstep = 1
      self.colours = dict()
      k = 0
      for i in range(len(cards)):
         self.colours[cards[i]] = colours[k]
         k += colstep
         if k >= len(colours):
            k %= len(colours)

   def AgentFunction(self, percepts):
      """Returns the bid value of the next bid

            :param percepts: a tuple of four items: bidding_on, items_left, my_cards, opponent_cards

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

      # Extract different parts of percepts.
      bidding_on = percepts[0]
      items_left = percepts[1]
      my_cards = percepts[2]
      bank = percepts[3]
      opponents_cards = percepts[4:]

      sys.stdout.write("  Items left: [")
      for d in items_left:
         sys.stdout.write("%d " % d)
      sys.stdout.write("\b]\n\r")

      # Print out the available cards
      sys.stdout.write("  Opponent hands:")
      for cards in opponents_cards:
         sys.stdout.write("[")
         for d in cards:
            print_colour_value(d,self.colours[d])
         sys.stdout.write("] ")

      # Print out the available cards
      sys.stdout.write("\n\n\r  Player's hand: [")
      for d in my_cards:
         print_colour_value(d,self.colours[d])

      print("]\n\r     Bidding on: %d" % bidding_on)

      sys.stdout.write("\n\r            Bid: ")

      # Show the blanks for where guesses are supposed to go
      sys.stdout.write("_")
      # Back the cursor to the start of the row (blanks will stay on the screen)
      #sys.stdout.write("\b")
      sys.stdout.flush()

      # Get the input
      action = None
      while True:
         c = readchar.readchar()
         if c=='\x03':
            # Ctrl-C exits the entire program
            sys.exit(-1)
         elif c=='\x7f':
            # Backspace removes last character written
            action = None
            sys.stdout.write("\b_")
            sys.stdout.flush()

         elif (c=='\r' or c=='\n'):
            if action is not None:
               break

         if c.isdigit():
            c = int(c)
            if c in my_cards:
               action = c
               sys.stdout.write("\b")
               print_colour_value(action,self.colours[action])

      sys.stdout.write("\r\n")
      sys.stdout.flush()

      # Return the board guess as action
      return action
