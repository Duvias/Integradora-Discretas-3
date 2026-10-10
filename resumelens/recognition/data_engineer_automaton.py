from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon

LANGS = ["PYTHON", "SCALA"]
PROCESSING = ["SPARK", "HADOOP", "KAFKA"]
DATABASES = ["POSTGRESQL", "MYSQL", "MONGODB"]
CLOUD = ["AWS", "AZURE", "GCP"]

def build_data_engineer_enfa():
    enfa = EpsilonNFA()
    p = [State("p" + str(i)) for i in range(8)]   # p0 ... p7
    enfa.add_start_state(p[0])
    enfa.add_final_state(p[7])
    for s in LANGS:
        enfa.add_transition(p[0], Symbol(s), p[1])
        enfa.add_transition(p[1], Symbol(s), p[1])
    enfa.add_transition(p[1], Symbol("SQL"), p[2])
    for s in PROCESSING:
        enfa.add_transition(p[2], Symbol(s), p[3])
        enfa.add_transition(p[3], Symbol(s), p[3])
    enfa.add_transition(p[3], Symbol("AIRFLOW"), p[4])
    enfa.add_transition(p[3], Epsilon(), p[4])      # Airflow is optional
    for s in DATABASES:
        enfa.add_transition(p[4], Symbol(s), p[5])
        enfa.add_transition(p[5], Symbol(s), p[5])
    enfa.add_transition(p[5], Epsilon(), p[6])      # cloud is optional
    for s in CLOUD:
        enfa.add_transition(p[6], Symbol(s), p[6])
    enfa.add_transition(p[6], Symbol("GIT"), p[7])
    return enfa

DATA_ENGINEER_ENFA = build_data_engineer_enfa()

def is_data_engineer(sequence):
    return DATA_ENGINEER_ENFA.accepts([Symbol(s) for s in sequence])