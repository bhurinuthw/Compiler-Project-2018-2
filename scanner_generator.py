class DFA:
    def __init__(self, Q, Sigma, delta, q0, F, type):
        self.name = type
        self.Q = Q  # set of states
        self.Sigma = Sigma  # alphabet (set of input characters)
        self.delta = delta  # transition function
        self.q0 = q0  # starting state
        self.F = F  # set of accepting states

        # add missing transitions
        for q in Q:  # for each state
            for c in Sigma:  # for each character
                if (q, c) not in delta:
                    delta[(q, c)] = 'err'

    def accept(self, string):
        # delta(delta(delta(delta(q0,s0),s1),s2),...) = q_last
        # if q_last is in F -> accept
        # otherwise -> reject
        q = self.q0
        for c in string:
            if q == 'err':
                return False
            q = self.delta[(q, c)]
        return q in self.F

class NFA:
    def __init__(self, Q, Sigma, delta, q0, F, type):
        self.name = type
        self.Q = Q  # set of states
        self.Sigma = Sigma  # alphabet (set of input characters)
        self.delta = delta  # transition function
        self.q0 = q0  # starting state
        self.F = F  # set of accepting states

        # add missing transitions
        Q.add('err')
        for q in Q:  # for each state
            for c in Sigma:  # for each character
                if (q, c) not in delta:
                    delta[(q, c)] = {'err'}

    def closure(self, q):
        working_set = {q}
        reached = set()
        while len(working_set) > 0:
            q = working_set.pop()
            reached.add(q)

            # if there is an empty string transition
            if (q, '') in self.delta:
                # add all next state candidates to the working set if they are not reached
                working_set = working_set.union(
                    {next_state for next_state in self.delta[(q, '')] if next_state not in reached})
        return reached

    def accept(self, string):
        current_states = self.closure(self.q0)  # start from closure of the starting state
        for c in string:
            next_states = set()  # possible next state
            for q in current_states:
                # delta(state, c) -> set of states
                for next_state in self.delta[(q, c)]:
                    closure_next_state = self.closure(next_state)
                    next_states = next_states.union(closure_next_state)
            current_states = next_states
        return any(q in self.F for q in current_states)

    # NFA to DFA
    def convert_to_DFA(self):
        Q_DFA = set()
        delta_DFA = dict()

        q0_DFA = tuple(sorted(list(self.closure(self.q0))))

        working_set = {q0_DFA}
        while len(working_set) > 0:
            current_states = working_set.pop()
            Q_DFA.add(current_states)
            for c in self.Sigma:
                next_states = set()  # possible next state
                for q in current_states:
                    # delta(state, c) -> set of states
                    for next_state in self.delta[(q, c)]:
                        closure_next_state = self.closure(next_state)
                        next_states = next_states.union(closure_next_state)
                newstate = tuple(sorted([s for s in next_states if s != 'err']))
                if newstate not in Q_DFA:
                    working_set.add(newstate)
                delta_DFA[(current_states, c)] = newstate

        F_DFA = set(q for q in Q_DFA if any(qf in q for qf in self.F))

        return DFA(Q_DFA, self.Sigma, delta_DFA, q0_DFA, F_DFA, self.name)

def regex_Extractor(fileName):
    pass

def tokenize(input_string, DFA):
    print(DFA.name)

def create_automaton(regex):
    pass

if __name__ == '__main__':
    Q = {0, 1, 2}  # set of states
    Sigma = {'a', 'b', 'c'}  # alphabet (set of input characters)
    delta = {(0, 'a'): 0,  # transition function
                (0, 'b'): 1,
                (1, 'a'): 1,
                (1, 'b'): 1,
                (1, 'c'): 2
                }
    q0 = 0  # starting state
    F = {2}  # set of accepting states

    delta_NFA2 = {
        (0, ''): {2},
        (0, 'a'): {0, 1},
        (1, 'a'): {1},
        (1, 'b'): {1},
        (1, 'c'): {2},
        (2, ''): {1}
    }

    N2 = NFA(Q, Sigma, delta_NFA2, q0, F, "tester")
    print(N2.accept('abcabaabac'))

    D2 = N2.convert_to_DFA()
    print(D2.accept('bbc'))

    tokenize('abcabaabac', D2)
