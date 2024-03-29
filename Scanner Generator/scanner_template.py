
########

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

def tokenize(input_string, DFA_list):
    token = []
    temp = ""
    lastAccept = None
    count = 0
    proceed = True
    while(count != len(input_string)):
        temp = temp + input_string[count]
        #print(count)
        #print(temp)
        for DFA in DFA_list:
            try:
                if(DFA.accept(temp)):
                    lastAccept = DFA.name
                    proceed = True
                    break
                else:
                    proceed = False
            except(KeyError):
                pass
            
        if(proceed == False and lastAccept is not None):
            token.append((lastAccept, temp[:-1]))
            temp = ""
            lastAccept = None
            proceed = True
        else:
            count += 1

    token.append((lastAccept, temp))
    return token

if __name__ == '__main__':

    print("REGEX Rules: ",end = "")

    DFA_list = []

    for each_regex in regex_list:
        temp = NFA(each_regex[0],each_regex[1],each_regex[2],each_regex[3],each_regex[4],each_regex[5])
        DFA_list.append(temp.convert_to_DFA())
        print(each_regex[5], end = " ")

    while(True):
        inp = input("\nPlease enter string to tokenize: ")
        inp = inp.split()
        temp = []
        print()
        for sets in inp:
            temp = temp + tokenize(sets, DFA_list)
        print(temp)

    #'aabab ba aaaaababababbabacacbabababababacacacacacababababbabacabab'
