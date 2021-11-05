"""Random player"""
import random
from typing import Sequence

import utils.handValue
from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage, HandType
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


        stage = observation.stage
        i_start = observation.myPosition == 0
        opponent_start = observation.myPosition == 1

        raise_weight = 50
        call_check_weight = 50
        fold_weight = 0

        i_start = observation.myPosition == 0
        opponent_start = observation.myPosition == 1

        initial_hand_type = utils.handValue.getHandType(observation.myHand)
        initial_hand_percent = 1 - utils.handValue.getHandPercent(observation.myHand)[0]
        if stage in [Stage.FLOP, Stage.TURN, Stage.RIVER, Stage.SHOWDOWN]:
            hand_and_board_type = utils.handValue.getHandType(observation.boardCards)
            hand_and_board_percent = 1 - utils.handValue.getHandPercent(observation.myHand, observation.boardCards)[0]

            if hand_and_board_type in [HandType.FOUROFAKIND, HandType.FLUSH, HandType.STRAIGHTFLUSH, HandType.FULLHOUSE, HandType.STRAIGHT]:
                raise_weight += 100
                fold_weight -= 100

        # INITIAL CARDS
        if observation.stage == Stage.PREFLOP:
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
        else:
            if hand_and_board_percent > 0.95:
                return Action.RAISE
            elif hand_and_board_percent > 0.8:
                raise_weight += 50
            elif hand_and_board_percent > 0.6:
                raise_weight += 5
                call_check_weight += 5
            elif hand_and_board_percent > 0.4:
                call_check_weight += 5
                fold_weight += 5
            else:
                fold_weight += 10

        # OPPONENT HISTORY
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        # Get the last action the opponent have done
        opponent_last_action = opponent_actions_this_round[-1] if len(opponent_actions_this_round) > 0 else None

        if opponent_last_action is None:
            # opponent didn't do anything yet for us to counter, just raise
            raise_weight += 5
        elif opponent_last_action in [Action.CHECK, Action.CALL]:
            # opponent checked, try to steal the pot with a raise
            raise_weight += 10
        elif opponent_last_action == Action.RAISE:
            # opponent raise, probably has good cards so fold
            fold_weight += 5

        # PREFLOP
        if i_start:
            if observation.stage == Stage.PREFLOP:
                if initial_hand_percent > 0.2:
                    fold_weight -= 1000000
                else:
                    fold_weight -= 100

        # SUIT
        suits = utils.handValue.getHighestSuitCount(observation.myHand, observation.boardCards)
        if suits[0] == 5:
            return Action.RAISE
        if suits[0] == 4:
            raise_weight += 10
            call_check_weight += 5
            fold_weight -= 10

        # STRAIT
        strait = utils.handValue.getLongestStraight(observation.myHand, observation.boardCards)
        if strait[0] == 5:
            return Action.RAISE
        if strait[0] == 4:
            raise_weight += 10
            call_check_weight += 5
            fold_weight -= 10

        if raise_weight < 0:
            raise_weight = 0
        if call_check_weight < 0:
            call_check_weight = 0
        if fold_weight < 0:
            fold_weight = 0

        # GET ACTION
        choice = random.choices([Action.RAISE, Action.CALL, Action.FOLD], [raise_weight, call_check_weight, fold_weight], k=1)
        return choice[0]
