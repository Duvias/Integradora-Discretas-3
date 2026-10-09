from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol

DATA = ["PANDAS", "NUMPY"]
ML = ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH"]
STORAGE = ["SQL", "POSTGRESQL", "MYSQL", "MONGODB"]

def build_ml_nfa():
    nfa = NondeterministicFiniteAutomaton()
    r = [State("r" + str(i)) for i in range(6)]   # r0 ... r5
    nfa.add_start_state(r[0])
    nfa.add_final_state(r[5])
    
    nfa.add_transition(r[0], Symbol("PYTHON"), r[1])
    
    for x in DATA:
        nfa.add_transition(r[1], Symbol(x), r[1])   # quedarse: vienen más librerías
        nfa.add_transition(r[1], Symbol(x), r[2])   # o avanzar: esta fue la última
        
    for x in ML:
        nfa.add_transition(r[2], Symbol(x), r[2])
        nfa.add_transition(r[2], Symbol(x), r[3])
        
    for x in STORAGE:
        nfa.add_transition(r[3], Symbol(x), r[3])
        nfa.add_transition(r[3], Symbol(x), r[4])
        
    nfa.add_transition(r[4], Symbol("GIT"), r[5])
    return nfa

ML_NFA = build_ml_nfa()

def is_ml_engineer(sequence):
    return ML_NFA.accepts([Symbol(x) for x in sequence])