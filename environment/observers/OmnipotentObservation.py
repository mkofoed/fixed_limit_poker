
rom environment.PlayerObservation import PlayerObservation
from environment.Constants import SUITS, Stage
from typing import Dict, Sequence, List
from json import dumps
from pyfancy.pyfancy import pyfancy


class OmnipotentObservation:
    boardCards: List[str]
    stage: Stage
    totalPot: int
    stagePot: int
    players: List[PlayerObservation]
    hands: Dict[str, Sequence[str]]

    def __init__(self) -> None:
        self.boardCards = []
        self.players = []
        self.stage = Stage.PREFLOP
        self.totalPot = 0
        self.stagePot = 0
        self.hands = dict()

    def __str__(self):
        header = pyfancy().red(f"{self.stage:<14}").get()
        pots_str = f"TotalPot: {self.totalPot:>3} StagePot: {self.stagePot:>3}"
        pots = pyfancy().green(pots_str).get()

        player_hands_list = [f"'{ph[0]}': {' '.join(ph[1])}" for ph in self.hands.items()]
        player_hands = pyfancy().yellow(" ".join(player_hands_list)).get()
        current_board = " ".join(self.boardCards)
        community = pyfancy().blue(f'Community: {current_board}').get()
        return f"{header} | {pots} | {player_hands} | {community}"