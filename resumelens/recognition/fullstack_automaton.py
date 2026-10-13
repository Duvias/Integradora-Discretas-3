from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol

LANGUAGES = ["JAVASCRIPT", "TYPESCRIPT"]
FRONTEND = ["REACT", "ANGULAR", "VUE"]
BACKEND = ["NODE_JS", "DJANGO", "SPRING_BOOT"]
DATABASES = ["POSTGRESQL", "MYSQL", "MONGODB"]

def build_fullstack_dfa():
    dfa = DeterministicFiniteAutomaton()
    s = [State("s" + str(i)) for i in range(6)]   # s0 ... s5
    dfa.add_start_state(s[0])
    dfa.add_final_state(s[5])
    
    for x in LANGUAGES:
        dfa.add_transition(s[0], Symbol(x), s[1])
        dfa.add_transition(s[1], Symbol(x), s[1])
    for x in FRONTEND:
        dfa.add_transition(s[1], Symbol(x), s[2])
        dfa.add_transition(s[2], Symbol(x), s[2])
    for x in BACKEND:
        dfa.add_transition(s[2], Symbol(x), s[3])
        dfa.add_transition(s[3], Symbol(x), s[3])
    for x in DATABASES:
        dfa.add_transition(s[3], Symbol(x), s[4])
        dfa.add_transition(s[4], Symbol(x), s[4])
        
    dfa.add_transition(s[4], Symbol("GIT"), s[5])
    return dfa

FULLSTACK_DFA = build_fullstack_dfa()

def is_fullstack(sequence):
    return FULLSTACK_DFA.accepts([Symbol(x) for x in sequence])