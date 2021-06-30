class rps:
    id = 0
    def __init__(self, p1, p2, p1_move, p2_move) -> None:
        self.p1, self.p2 = p1, p2
        self.p1_move, self.p2_move = p1_move, p2_move
        self.id = rps.id
        rps.id += 1

    def _winner(self) -> str:
        """Returns the winner of the game"""