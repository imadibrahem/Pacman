# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    move =""
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        self.move = legalMoves[chosenIndex]
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        score = 0
        if len(newFood.asList()) < len(currentGameState.getFood().asList()):
          score += 4
       
        food_list = newFood.asList()
        food_distances = []
       
        for f in food_list :
          food_distances.append(manhattanDistance(f,newPos))

        for fd in food_distances :
          score += 1/fd
        
        for g in range (len(newGhostStates)) :
          if newScaredTimes[g] < 2 and manhattanDistance(newGhostStates[g].getPosition(),newPos) < 2:
            score -=  20-manhattanDistance(newGhostStates[g].getPosition(),newPos)
        if action == "Stop":
          score -= 1
        if self.move == "North" and action == "South":
          score -= 1
        if self.move == "South" and action == "North":
          score -= 1
        if self.move == "East" and action == "West":
          score -= 1
        if self.move == "West" and action == "East":
          score -= 1
         
        return score 

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
       

        def min_max(gameState,agent,depth):
          output = []

          if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1
          actions = gameState.getLegalActions(agent) 

          if depth == self.depth or len(actions)<1 :            
            return [self.evaluationFunction(gameState),""]
          
          for action in actions:
            g_state = gameState.generateSuccessor(agent, action)
            if agent == 0 :
              output = pacman_move(output,g_state,agent,depth,action)

            else : 
              output = ghost_move(output,g_state,agent,depth,action)
          return output
        
        def pacman_move(output,g_state,agent,depth,action):
          new_value = min_max(g_state,agent+1,depth)
          if len(output) < 1 or output[0] < new_value[0]:
            output = [new_value[0],action]
          return output 


        def ghost_move(output,g_state,agent,depth,action):
          new_value = min_max(g_state,agent+1,depth)
          if len(output) < 1 or output[0] > new_value[0]:  
            output = [new_value[0],action] 
          return output
        return min_max(gameState,0,0)[1]
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
       
        def alpha_beta(gameState,agent,depth,alpha,beta):
          output = []

          if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1
          actions = gameState.getLegalActions(agent)
          if depth == self.depth or len(actions)<1 :            
            return [self.evaluationFunction(gameState),""]
          
          for action in actions:
            g_state = gameState.generateSuccessor(agent, action)            
            if agent == 0 :             
             
              result = pacman_move(output,g_state,agent,depth,action,alpha,beta)
              output = result[0]
              alpha = result[1]
              beta = result[2]
              if len(output) > 0 and output[0] > beta:
                return output


            else : 
              
              result = ghost_move(output,g_state,agent,depth,action,alpha,beta)
              output = result[0]
              alpha = result[1]
              beta = result[2]
              if len(output) > 0 and output[0] < alpha:
                return output
             

         # print(alpha)
          #print (beta)
          return output
        
        def pacman_move(output,g_state,agent,depth,action,alpha,beta):
          new_value = alpha_beta(g_state,agent+1,depth,alpha,beta)
          if len(output) < 1 or output[0] < new_value[0]:
            output = [new_value[0],action]
          
          alpha = max(new_value[0],alpha)
             
          return [output,alpha,beta] 


        def ghost_move(output,g_state,agent,depth,action,alpha,beta):
          new_value = alpha_beta(g_state,agent+1,depth,alpha,beta)
          if len(output) < 1 or output[0] > new_value[0]:  
            output = [new_value[0],action] 
          beta = min(new_value[0],beta)
          
          return [output,alpha,beta]
        return alpha_beta(gameState,0,0,-10000000,10000000)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
          The expectimax function returns a tuple of (actions,
        """
        "*** YOUR CODE HERE ***"
        def exp_max(gameState,agent,depth):
          output = []

          if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1
          actions = gameState.getLegalActions(agent) 

          if depth == self.depth or len(actions)<1 :            
            return [self.evaluationFunction(gameState),""]
          
          for action in actions:
            g_state = gameState.generateSuccessor(agent, action)
            if agent == 0 :
              output = pacman_move(output,g_state,agent,depth,action)

            else : 
              output = ghost_move(output,g_state,agent,depth,action)
          return output
        
        def pacman_move(output,g_state,agent,depth,action):
          new_value = exp_max(g_state,agent+1,depth)
          if len(output) < 1 or output[0] < new_value[0]:
            output = [new_value[0],action]
          return output 


        def ghost_move(output,g_state,agent,depth,action):
          new_value = exp_max(g_state,agent+1,depth)
          expectVal = new_value[0]*(1.0 / len(gameState.getLegalActions(agent)))
          if len(output) > 0:
            expectVal += output[0] 

          output = [expectVal,action] 
          return output
        return exp_max(gameState,0,0)[1]

        util.raiseNotDefined()
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
      Evaluate state by  :
            * closest food
            * food left
            * capsules left
            * distance to ghost
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capPos = currentGameState.getCapsules()         
    score =  currentGameState.getScore()/2
       
    food_list = newFood.asList()
    food_distances = []
    cap_distances = []
       
    for f in food_list :
      food_distances.append(manhattanDistance(f,newPos))

    for fd in food_distances :
      score += 1/fd

    for cap in capPos:
      cap_distances.append(manhattanDistance(cap,newPos))

    for capd in cap_distances:
      score += 2/capd
    
    if capPos:
      score -= 5* len (capPos)

        
    for g in range (len(newGhostStates)) :
      if newScaredTimes[g] < 2 and manhattanDistance(newGhostStates[g].getPosition(),newPos) < 2:
        score -=  20-manhattanDistance(newGhostStates[g].getPosition(),newPos)
      
      if newScaredTimes[g] > 2:
        score +=  3/manhattanDistance(newGhostStates[g].getPosition(),newPos)
     
    return score 


# Abbreviation
better = betterEvaluationFunction
