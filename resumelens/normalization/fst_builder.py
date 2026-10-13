from pyformlang.fst import FST

def build_fst(rules):
    """rules = {"CANONICAL": ["variant1", "variant2"], ...}  (variants in lowercase)
    Each variant becomes its own path of states, one state per letter.
    Every letter writes nothing ([]) except the last one, which writes the
    canonical name. The last state of each path is final."""
    fst = FST()
    fst.add_start_state("q0")
    counter = 1
    for canonical, variants in rules.items():
        for variant in variants:
            current = "q0"
            for i in range(len(variant)):
                letter = variant[i]
                next_state = "q" + str(counter)
                counter += 1
                if i == len(variant) - 1:
                    output = [canonical]
                else:
                    output = []
                fst.add_transition(current, letter, next_state, output)
                current = next_state
            fst.add_final_state(current)
    return fst