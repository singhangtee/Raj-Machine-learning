__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

import os,sys
import numpy as np
import importlib.util
import time
import copy
from settings import game_settings


def time_to_str(time_in_seconds):
   timeStr = ''
   if time_in_seconds > 3600:
      hours = int(np.floor(time_in_seconds / 3600))
      timeStr += "%d h, " % hours
      time_in_seconds %= 3600

   if time_in_seconds > 60:
      minutes = int(np.floor(time_in_seconds / 60))
      timeStr += "%d min, " % minutes
      time_in_seconds %= 60

   if time_in_seconds < 1:
      timeStr += "%.3f s" % time_in_seconds
   else:
      timeStr += "%d s" % time_in_seconds

   return timeStr


# Class player is a wrapper for a player agent
class Player:
   def __init__(self, game, playerFile, jointname=False):
      self.playerFile = playerFile
      self.game = game

      # Player file must be in same folder as raj.py
      if not self.game.in_tournament:
         game_folder = os.path.dirname(os.path.realpath(__file__))
         playerFile = os.path.join(game_folder,playerFile)

      if not os.path.exists(playerFile):
         raise RuntimeError("Error! Agent file '%s' not found" % self.playerFile)

      if len(self.playerFile) > 3 and self.playerFile[-3:].lower() == '.py':
         playerModule = self.playerFile[:-3]
      else:
         raise RuntimeError("Error! Agent file %s needs a '.py' extension" % self.playerFile)


      try:

         spec = importlib.util.spec_from_file_location(playerModule, playerFile)
         self.exec = importlib.util.module_from_spec(spec)
         sys.modules["module.name"] = self.exec
         spec.loader.exec_module(self.exec)
      except Exception as e:
         raise RuntimeError(str(e))

      card_values = list(game.card_values)
      item_values = list(game.item_values)

      try:
         self.agent = self.exec.RajAgent(card_values=card_values, item_values=item_values)
      except Exception as e:
         raise RuntimeError(str(e))

      if hasattr(self.exec, 'agentName') and self.exec.agentName[0] != '<':
         self.name = self.exec.agentName
      else:
         if self.game.in_tournament and self.playerFile != 'random_agent.py':
            self.name = self.playerFile.split('/')[-2]# playerFile.split('.')[1]
         else:
            self.name = self.playerFile

      if hasattr(self.exec, 'training'):
         self.training = self.exec.training
      else:
         self.training = None

      if self.training is not None:
         if not hasattr(self.exec, 'save_filename'):
            raise RuntimeError("Error! Agent file '%s' has training attribute but no save_filename attribute" % self.playerFile)

         this_scripts_dir = os.path.dirname(os.path.realpath(__file__))
         self.save_filename = os.path.join(this_scripts_dir, self.exec.save_filename)

         if os.path.exists(self.save_filename):
            self.agent.load(self.save_filename)
            self.training = None

      if jointname and self.game.in_tournament:
         self.pname = self.playerFile.split('/')[-2]


class RajGame:

   def __init__(self,card_values,item_values, num_players, verbose=False,tournament=False):

      self.card_values = card_values
      self.item_values = item_values
      self.in_tournament = tournament

      self.verbose = verbose
      if tournament:
         self.throwError = self.errorAndReturn
      else:
         self.throwError = self.errorAndExit

      if len(card_values) != len(item_values):
         self.throwError("Error! cardValues and itemValues in settings must have the same length")

      if len(card_values) < 2:
         self.throwError("Error! cardValues and itemValues must have at least 2 values")

      if len(card_values) > 6:
         self.throwError("Error! cardValues and itemValues must have at most 6 values")

      if self.verbose:
         print("Raj game settings:")

         print(f'  Card values: {self.card_values}')
         print(f'  Item values: {self.item_values}')
         print(f'  Num players: {num_players}')

   def errorAndExit(self,errorStr):
      raise RuntimeError(errorStr)

   def errorAndReturn(self,errorStr):
      if not hasattr(self,'errorStr') or self.errorStr is None or len(errorStr) > 0:
         self.errorStr = errorStr
      return None



   def play(self,players,items):

      score = np.zeros((len(players)))
      num_bids = len(items)
      cards = []

      for _ in range(len(players)):
         cards.append(list(self.card_values))


      item_value = 0
      for i in range(num_bids):
         item_value += items[i]
         for p, player in enumerate(players):
            cards[p].sort()
         items_left  = items[i+1:].tolist()
         items_left.sort()

         if self.verbose:
            print("  Bid %d/%d, item(s) value: %d" % (i+1,num_bids, item_value))

         bids = np.zeros(shape=(len(players)),dtype='int')    
         for p, player in enumerate(players):
            percepts = (item_value, tuple(items_left), tuple(cards[p]), score[p])
            for p2 in range(len(players)):
               if p2 != p:
                  percepts += (tuple(cards[p2]),)

            try:
               #if len(items_left) > 0:
               action = player.agent.AgentFunction(percepts)
               #else:
               #   action = cards[p][0]
            except Exception as e:
               self.throwError(str(e))
               return None

            try:
               if action not in cards[p]:
                  self.throwError("Error! AgentFunction from '%s.py' returned a card that's not in players hand" % (player.playerFile))
                  return None


            except Exception as e:
               self.throwError(str(e))
               return None

            bids[p] = action

         if self.verbose:
            for p in range(len(players)):
               print("    Player %d (%s) bids %d." % (p+1, players[p].name,bids[p]))

         # Only unique bids count
         unique_bids ,counts = np.unique(bids,return_counts=True)
         I = np.where(counts==1)[0]

         if len(I) == 0:
            if self.verbose:
               print("    No unique bids, no points awarded.")
         else:
            Is = unique_bids[I]
            if item_value >= 0:
               winning_bid = Is[-1]
            else:
               winning_bid = Is[0]

            p = np.where(bids==winning_bid)[0][0]

            if self.verbose:
                print("    Player %d (%s) gets item(s) valued at %d." % (p+1, players[p].name,item_value))
            score[p] += item_value
            item_value = 0

         # Remove players cards from their hands
         for p in range(len(players)):
            cards[p].remove(bids[p])



      return score


   def run(self,agentFiles,num_games=1000,seed=None):


      if seed is None:
         seed = int(time.time())

      rnd = np.random.RandomState(seed)

      players = []
      for i, agentFile in enumerate(agentFiles):
         try:
            player = Player(game=self, playerFile=agentFile)
            players.append(player)
         except Exception as e:
            self.throwError(str(e))

      for player in players:
         if player.training is not None:


            if self.verbose:
               print("Training agent %s" % player.name)

            if hasattr(player.agent, 'train_session_start'):
               try:
                  player.agent.train_start()
               except Exception as e:
                  self.throwError(str(e))
                  return None

            for train_session in player.training:

               try:
                  opponents = list(train_session)[:-1]
                  num_train_games = train_session[-1]
               except Exception as e:
                  self.throwError(str(e))
                  return None

               if self.verbose:
                  print("  Training against %s" % str(opponents))
                  print("  Num games: %d" % num_train_games)

               other_players = []
               for opponent in opponents:
                  #if opponent == player.playerFile or opponent == 'self':
                  #   try:
                  #      other_player = player
                  #      other_players.append(other_player)
                  #   except Exception as e:
                  #      self.throwError(str(e))
                  #      return None
                  #else:
                  try:
                     other_player = Player(game=self, playerFile=opponent)
                     other_players.append(other_player)
                  except Exception as e:
                     self.throwError(str(e))

               if hasattr(player.agent, 'train_session_start'):
                  try:
                     player.agent.train_session_start()
                  except Exception as e:
                     self.throwError(str(e))
                     return None


               for n in range(num_train_games):
                  if hasattr(player.agent, 'train_game_start'):
                     try:
                        player.agent.train_game_start()
                     except Exception as e:
                        self.throwError(str(e))
                        return None

                  score = self.play([player] + other_players,items=rnd.choice(self.item_values,size=len(self.item_values),replace=False))

                  if score is None:
                     return None

                  if hasattr(player.agent, 'train_game_end'):
                     try:
                        player.agent.train_game_end(score)
                     except Exception as e:
                        self.throwError(str(e))
                        return None

               if hasattr(player.agent, 'train_session_end'):
                  try:
                     player.agent.train_session_end()
                  except Exception as e:
                     self.throwError(str(e))
                     return None

            if hasattr(player.agent, 'train_end'):
               try:
                  player.agent.train_end()
               except Exception as e:
                  self.throwError(str(e))
                  return None
            
            try:
               player.agent.save(player.save_filename)
            except Exception as e:
               self.throwError(str(e))
               return None

      if self.verbose:
         print("Game play:")
         print("  Num rounds:       %d" % num_games)



      all_boards = np.zeros((num_games, len(self.item_values)))
      for n in range(num_games):
         all_boards[n] = rnd.choice(self.item_values,size=len(self.item_values),replace=False)

      score = np.zeros((len(players)))
      game_count = 0
      tot_time = 0
      games_won = 0
      games_lost = 0
      games_middle = 0
      for n in range(num_games):
         if self.verbose:
            print("Round %d/%d" % (game_count+1,num_games))

         start = time.time()
         game_score = self.play(players,items=all_boards[n])
         end = time.time()
         if game_score is None:
            return None

         score += game_score
         game_count += 1
         if max(game_score) == game_score[0]:
            games_won += 1
         elif min(game_score) == game_score[0]:
            games_lost += 1
         else:
            games_middle += 1

         if self.verbose:
            score_str = "  Score in game %d: " % game_count
            for i in range(len(players)):
               score_str += "\n    Player %d (%s): %.2f" % (i+1, players[i].name, game_score[i])
            print(score_str)
 
            score_str = "Average score after game %d: " % game_count
            for i in range(len(players)):
               score_str += "\n  Player %d (%s): %.2f" % (i+1, players[i].name, score[i]/game_count)
            print(score_str)
         tot_time += end - start

         if game_count < num_games:
            avg_time = tot_time / game_count
            if self.verbose:
               print("Average running time per game %s." % (time_to_str(avg_time)))
               print("Time remaining %s." % (time_to_str(avg_time * (num_games-game_count))))
               print("Expected total running time %s." % (time_to_str(avg_time * num_games)))
         else:
            if self.verbose:
               print("Total running time %s." % (time_to_str(tot_time)))
               
      print("Games won: %d" % games_won, "Games lost: %d" % games_lost, "Second place: %d" % games_middle)         
      
      return score




if __name__ == "__main__":

   game = RajGame(card_values=game_settings['cardValues'],
                  item_values=game_settings['itemValues'],
                  num_players=len(game_settings['agentFiles']),
                  verbose=game_settings['verbose'])
   
   game.run(agentFiles=game_settings['agentFiles'],
         num_games=game_settings['totalNumberOfGames'],
         seed=game_settings['seed'])



