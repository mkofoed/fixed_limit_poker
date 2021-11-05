from bots.MikkBot import MikkBot
from environment.observers.LoggingObserver import LoggingObserver
from environment.FixedLimitPoker import FixedLimitPoker
from bots import TemplateBot, CounterBot, PercentBot
import pandas as pd
import itertools


def debug():
    observers = [LoggingObserver()]
    env = FixedLimitPoker([
        # Change the bots here to change the participants
        CounterBot(),
        MikkBot()
    ], observers=observers, punishSlowBots=False)
    env.reset()
    env.reset(rotatePlayers=True)


def benchmark():
    bots = [
        # Change the bots here to change the participants
        CounterBot(),
        PercentBot(),
        MikkBot(),
        # TemplateBot(),
    ]
    combinations = list(itertools.combinations(bots, 2))
    roundsPerPair = 1000
    cols = [x.name for x in bots]
    stats = pd.DataFrame(0, columns=cols, index=cols + ["sum", "pr. round"])
    for c in combinations:
        room = FixedLimitPoker(c, punishSlowBots=False)
        for _ in range(roundsPerPair):
            room.reset(rotatePlayers=True)
            p1 = room.players[0]
            p2 = room.players[1]
            stats[p1.bot.name][p2.bot.name] += p1.reward
            stats[p1.bot.name]["sum"] += p1.reward
            stats[p2.bot.name][p1.bot.name] += p2.reward
            stats[p2.bot.name]["sum"] += p2.reward
    for bot in bots:
        stats[bot.name]["pr. round"] = stats[bot.name]["sum"] / \
            (roundsPerPair*(len(bots)-1))
    print(stats)


#benchmark()
debug()
