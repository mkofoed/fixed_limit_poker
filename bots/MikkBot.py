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

        raise_weight = 1
        call_check_weight = 1
        fold_weight = 1

        i_start = observation.myPosition == 0
        opponent_start = observation.myPosition == 1

        initial_hand_percent = 1 - utils.handValue.getHandPercent(observation.myHand)[0]
        hand_type = utils.handValue.getHandType(observation.myHand)
        board_type = utils.handValue.getBoardHandType(observation.boardCards)
        hand_and_board_type = utils.handValue.getHandType(observation.myHand, observation.boardCards)

        # INITIAL CARDS
        if initial_hand_percent > 0.95:
            raise_weight += 100
        elif initial_hand_percent > 0.8:
            raise_weight += 20
        elif initial_hand_percent > 0.6:
            raise_weight += 5
            call_check_weight += 5
        elif initial_hand_percent > 0.4:
            call_check_weight += 5
            fold_weight += 5
        else:
            fold_weight += 10

        # OPPONENT HISTORY
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        opponent_last_action = opponent_actions_this_round[-1] if len(opponent_actions_this_round) > 0 else None
        opponent_history = observation.get_opponent_history_current_stage()
        opponent_raise_percent = 0
        opponent_fold_percent = 0
        opponent_check_call_percent = 0
        if len(opponent_history) > 10:
            opponent_raise_percent = opponent_history.count(Action.RAISE) / len(opponent_history)
            opponent_fold_percent = opponent_history.count(Action.FOLD) / len(opponent_history)
            opponent_check_call_percent = (opponent_history.count(Action.CALL) + opponent_history.count(
                Action.CHECK)) / len(opponent_history)

        if opponent_start:
            if observation.stage.PREFLOP:
                if opponent_last_action == Action.RAISE:
                    if opponent_raise_percent > 0.8:
                        raise_weight += 10
                        call_check_weight += 10
                    elif opponent_raise_percent > 0.2:
                        raise_weight += 2
                        call_check_weight += 2
                    else:
                        fold_weight += 10
                if opponent_last_action == Action.FOLD:
                    if opponent_fold_percent > 0.7:
                        raise_weight += 10
                    elif opponent_fold_percent > 0.5:
                        raise_weight += 5
                        call_check_weight += 5
                    else:
                        fold_weight += 10
        if i_start:
            if observation.stage.PREFLOP:
                fold_weight -= 1000000

        # SUIT
        suits = utils.handValue.getHighestSuitCount(observation.myHand, observation.boardCards)
        if suits[0] == 5:
            return Action.RAISE
        if suits[0] == 4:
            raise_weight += 10
            call_check_weight += 5
            fold_weight -= 10

        strait = utils.handValue.getLongestStraight(observation.myHand, observation.boardCards)
        # STRAIT
        if strait[0] == 5:
            return Action.RAISE
        if strait[0] == 4:
            raise_weight += 10
            call_check_weight += 5
            fold_weight -= 10



        choice = random.choices([Action.RAISE, Action.CALL, Action.FOLD], [raise_weight, call_check_weight, fold_weight], k=1)

        if random.random() > 0.95:
            return Action.RAISE

        return choice[0]

