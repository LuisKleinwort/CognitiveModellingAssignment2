import random

from python_actr import *


class TowerEnvironment:
    def __init__(self):
        self.A = list(range(3, 0, -1))  # disks on Tower A
        self.B = []
        self.C = []
        self.print_towers()

    def move_disk(self, from_, to):
        disk = getattr(self, from_).pop()
        getattr(self, to).append(disk)
        print(f"Disk {disk} was moved from peg {from_} to peg {to}.")
        self.print_towers()

    def print_towers(self):
        print(f"Peg A has disks {self.A}, Peg B has disks {self.B}, Peg C has disks {self.C}")


class TowerModel(ACTR):
    from itertools import permutations
    focus = Buffer()
    env = TowerEnvironment()

    def init():
        focus.set('do_action last_from:None last_to:None')

    def do_action(focus="do_action last_from:?last_from last_to:?last_to"):
        possible_moves = [(from_, to) for (from_, to) in permutations(['A', 'B', 'C'], 2)
                            if (getattr(env, from_)           # If there is a disk on 'from' tower
                                and (not getattr(env, to)
                                     or getattr(env, to)[-1] > getattr(env, from_)[-1]
                                     )  # and is a valid move (no disk or disk bellow is bigger)
                                )]
        if possible_moves:
            # Don't undo last move (unless its our only option)
            last_move_reveresed = last_to, last_from
            if len(possible_moves) > 1 and last_move_reveresed in possible_moves:
                possible_moves.remove(last_move_reveresed)
            from_, to = random.choice(possible_moves)
            env.move_disk(from_, to)
            last_from = from_
            last_to = to
        focus.set('check_if_done last_from:?last_from last_to:?last_to')

    def chech_if_done(focus="check_if_done last_from:?last_from last_to:?last_to"):
        if env.C == [3, 2, 1]:
            focus.set("finished")
        else:
            focus.set("do_action last_from:?last_from last_to:?last_to")

model = TowerModel()
model.env = model.env

model.run()
