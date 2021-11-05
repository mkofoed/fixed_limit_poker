"""Random player"""
import random
from typing import Sequence

import utils.handValue
from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation


# your bot class, rename to match the file name
class MikkBot(BotInterface):

    # change the name of your bot here
    def __init__(self, name="PokeIt"):
        """init function"""
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        """
            This function gets called whenever it's your bots turn to act.
                Parameters:
                    action_space (Sequence[Action]): list of actions you are allowed to take at the current state.
                    observation (Observation): all information available to your bot at the current state. See environment/Observation for details
                returns:
                    action (Action): the action you want you bot to take. Possible actions are: FOLD, CHECK, CALL and RAISE
            If this function takes longer than 1 second, your bot will fold
        """


        hand_type = utils.handValue.getHandType(observation.myHand)
        board_type = utils.handValue.getBoardHandType(observation.boardCards)
        hand_and_board_type = utils.handValue.getHandType(observation.myHand, observation.boardCards)
        hand_percent = utils.handValue.getHandPercent(observation.myHand)

        if hand_percent[0] > 0.8:
            return Action.RAISE
        if hand_percent[0] > 0.4:
            return Action.CALL
        return Action.FOLD
