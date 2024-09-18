__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

# You can manipulate these settings to change how the game is played.

game_settings = {

   "agentFiles": ("myrl_agent.py", "value_agent.py", "valueplus_agent.py"), # agent files that play the game,
                                                        # (replace human_agent with my_agent.py when 
                                                        # your agent is ready)

   "cardValues": (1,2,3,4,5,6),  # value of the cards to bid with      

   "itemValues": (-2,-1,1,2,3,4), # values of the items to bid on (must be same length as cardValues)

   "totalNumberOfGames": 100,    # total number of games played

   "verbose": True,

   "seed": 0,                     # seed for random choices of bids in the game, None for random seed

}


# If main is run, create an instance of the game and run it
if __name__ == "__main__":
   from raj import RajGame

   game = RajGame(card_values=game_settings['cardValues'],
                  item_values=game_settings['itemValues'],
                  num_players=len(game_settings['agentFiles']),
                  verbose=game_settings['verbose'])
   
   game.run(agentFiles=game_settings['agentFiles'],
         num_games=game_settings['totalNumberOfGames'],
         seed=game_settings['seed'])