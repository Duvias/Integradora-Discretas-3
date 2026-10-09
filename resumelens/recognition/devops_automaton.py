from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol

SCRIPTING = ["PYTHON", "BASH"]
CI_CD = ["JENKINS", "GITHUB_ACTIONS", "GITLAB_CI"]
CLOUD = ["AWS", "AZURE", "GCP"]

def build_devops_dfa():
    dfa = DeterministicFiniteAutomaton()
    q = [State("q" + str(i)) for i in range(7)]   # q0 ... q6
    dfa.add_start_state(q[0])
    dfa.add_final_state(q[6])
    for s in SCRIPTING:
        dfa.add_transition(q[0], Symbol(s), q[1])
        dfa.add_transition(q[1], Symbol(s), q[1])
    dfa.add_transition(q[1], Symbol("DOCKER"), q[2])
    dfa.add_transition(q[2], Symbol("KUBERNETES"), q[3])
    for s in CI_CD:
        dfa.add_transition(q[2], Symbol(s), q[4])   # saltarse Kubernetes
        dfa.add_transition(q[3], Symbol(s), q[4])
        dfa.add_transition(q[4], Symbol(s), q[4])
    for s in CLOUD:
        dfa.add_transition(q[4], Symbol(s), q[5])
        dfa.add_transition(q[5], Symbol(s), q[5])
    dfa.add_transition(q[5], Symbol("GIT"), q[6])
    return dfa

DEVOPS_DFA = build_devops_dfa()

def is_devops(sequence):
    return DEVOPS_DFA.accepts([Symbol(s) for s in sequence])