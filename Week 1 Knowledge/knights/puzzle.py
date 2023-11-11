from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# Each character is either a knight or a knave
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
)

knowledge0.add(Implication(AKnight, And(AKnight, AKnave)))
knowledge0.add(Implication(AKnave, Not(And(AKnight, AKnave))))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))
)

knowledge1.add(Implication(AKnight, And(AKnave, BKnave)))
knowledge1.add(Implication(AKnave, Not(And(AKnave, BKnave))))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))
)

knowledge2.add(Implication(AKnight, And(AKnight, BKnight)))
knowledge2.add(Implication(AKnave, Not(And(AKnight, BKnight))))
knowledge2.add(Implication(BKnight, Not(And(AKnight, BKnight))))
knowledge2.add(Implication(BKnave, Not(And(AKnave, BKnave))))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
)

knowledge3.add(Implication(AKnight, Or(AKnight, AKnave)))
knowledge3.add(Implication(AKnave, Not(Or(AKnight, AKnave))))
knowledge3.add(Implication(BKnight, AKnave))
knowledge3.add(Implication(BKnave, Not(AKnave)))
knowledge3.add(Implication(BKnight, CKnave))
knowledge3.add(Implication(BKnave, Not(CKnave)))
knowledge3.add(Implication(CKnight, AKnight))
knowledge3.add(Implication(CKnave, Not(AKnight)))


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
