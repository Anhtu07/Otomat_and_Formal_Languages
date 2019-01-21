from collections import defaultdict
from copy import copy


def count(string, array):
    res = 0
    for a in array:
        res += string.count(a)
    return res
class ReGrammar:
    def __init__(self, V, T, P, S='S'):
        self.P = P
        self.V = V
        self.T = T
        for v in self.V + self.T:
            if len(v) > 1:
                raise Exception('Xin hãy chọn chữ cái có độ dài = 1')
        self.S = S
    
    @classmethod
    def from_text(cls, text):
        text = text.strip()
        lines = text.split('\n')
        V = lines[0].split(' ')
        T = lines[1].split(' ')
        S = lines[2]
        P = defaultdict(list)
        for line in lines[3:]:
            line_splitted = line.split('->')
            v = line_splitted[0].strip()
            P[v].extend([r.strip() for r in line_splitted[1].split('|')])
        return cls(V, T, P, S)

    def is_left_linear(self):
        f = True
        for key in self.P.keys():
            for r in self.P[key]:
                if (count(r, self.V) == 1 and r[0] not in self.V) or count(r, self.V) > 1:
                    f = False
                    break
        return f
    
    def is_right_linear(self):
        f = True
        for key in self.P.keys():
            for r in self.P[key]:
                if (count(r, self.V) == 1 and r[-1] not in self.V) or count(r, self.V) > 1:
                    f = False
                    break
        return f

    def is_regular_grammar(self):
        return self.is_left_linear() or self.is_right_linear()

    def to_right_linear(self):
        if not self.is_left_linear:
            raise Exception("Không chuyển được =(")
        elif self.is_right_linear:
            return copy(self)
        new_P = defaultdict(list)
        new_start = False
        for key in self.P.keys():
            for rule in self.P[key]:
                if self.S in rule:
                    new_start = True
                    break
        P = copy(self.P)
        V = self.V[:]
        if new_start:
            S = 'S_0'
            V.append('S_0')
            P['S_0'].append(self.S)
        else:
            S = self.S
        for key in P.keys():
            for rule in P[key]:
                if count(rule, V) == 0 and key == S:
                    new_P[key].append(rule)
                elif count(rule, V) == 0:
                    new_P[S].append(rule + key)
                elif key == S and rule[0] in V:
                    new_P[rule[0]].append(rule[1:] if rule[1:] != '' else 'ε')
                elif rule[0] in V:
                    new_P[rule[0]].append((rule[1:] if rule[1:] != '' else 'ε') + key)
                else:
                    new_P[key].append(rule)
        reg = ReGrammar(V, self.T, new_P, self.S)
        reg.S = S
        return reg
    
    def to_string(self):
        string_result = ' '.join(self.V) + '\n' + ' '.join(self.T) + '\n' + self.S + '\n'        
        for key in self.P.keys():
            if len(self.P[key]) > 0:
                string_result += (key + ' -> ' + '|'.join(self.P[key]) + '\n')
        return string_result
    
    def to_nfa(self):
        from NFA import NFA
        from State import State
        if not self.is_regular_grammar():
            raise Exception('Văn phạm này không phải văn phạm chính quy')
        if self.is_left_linear():
            self = self.to_right_linear()
        alphabet = self.T
        Q = []
        for v in self.V:
            state = State()
            state.name = v
            Q.append(state)
            if v == self.S:
                init_state = state
        final_state = State()
        final_state.name = 'ε'
        Q.append(final_state)
        final_states = [final_state]
        middle_states = []
        table = defaultdict(dict)
        for s in Q:
            for c in alphabet + ['ε']:
                table[s][c] = set()
        for key in self.P.keys():
            for rule in self.P[key]:
                if rule[-1] in self.V:
                     for s in Q:
                         if s.name == key:
                             start = s
                         if s.name == rule[-1]:
                             des = s
                             w = rule[:-1]
                             
                else:
                    for s in Q:
                        if s.name == key:
                             start = s
                        if s.name == 'ε':
                            des = s
                            w = rule
                path = [start]
                for _ in range(len(w) - 1):
                    n_state = State()
                    path.append(n_state)
                    middle_states.append(n_state)
                    for c in alphabet + ['ε']:
                        table[n_state][c] = set()
                path.append(des)
                for idx, c in enumerate(w):
                    table[path[idx]][c].add(path[idx+1])
        Q.extend(middle_states)
        nfa = NFA(Q, alphabet, init_state, final_states, table)
        nfa.rename_states()
        return nfa
        

        
if __name__ == '__main__':
    text = '''S A T
a b
T
A -> ababS|aA
S -> bS|ε
T -> aA'''
    reg = ReGrammar.from_text(text)
    print(reg.P)
    right = reg.to_right_linear()
    print(right.P)
    print(right.to_string())
    nfa = reg.to_nfa()
    print(nfa.table)
    nfa.draw()
    