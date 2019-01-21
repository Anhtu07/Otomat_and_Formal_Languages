from graphviz import Source
from State import State

class NFA:
    def __init__(self, Q, alphabet, init_state, final_states, table):
        self.Q = Q
        self.alphabet = alphabet
        self.init_state = init_state
        self.final_states = final_states
        self.table = table
    
    @classmethod
    def from_text(cls, text):
        text = text.strip()
        lines = text.split('\n')
        Q = lines[0].split(' ')
        states = []
        for q in Q:
            state = State(q)
            states.append(state)
        alphabet = lines[1].split(' ')
        init_state = states[int(lines[2])]
        final_states = [states[int(index)] for index in lines[3].split(' ')]
        table = dict()
        for s in states:
            table[s] = dict()
            for c in alphabet + ['ε']:
                table[s][c] = set()
        for line in lines[4:]:
            s, c, d = line.split(' ')
            s = int(s)
            d = d.split(',')
            d = [states[int(index)] for index in d]
            if c != 'empty':
                table[states[s]][c] = table[states[s]][c].union(set(d))
            else:
                table[states[s]]['ε'] = table[states[s]]['ε'].union(set(d))
        return cls(states, alphabet, init_state, final_states, table)

    @classmethod
    def init_table(cls, states, alphabet):
        table = dict()
        alphabet = alphabet if 'ε' in alphabet else alphabet + ['ε']
        for s in states:
            table[s] = dict()
            for c in alphabet:
                table[s][c] = set()
        return table

    @classmethod
    def single_char(cls, alphabet, c):
        state_1 = State()
        state_2 = State()
        states = [state_1, state_2]
        init_state = state_1
        final_states = [state_2]
        table = cls.init_table(states, alphabet)
        table[state_1][c].add(state_2)
        nfa = NFA(states, alphabet, init_state, final_states, table)
        return nfa

    @classmethod
    def union(cls, nfa_1, nfa_2):
        alphabet = nfa_1.alphabet
        nfa_2.init_state
        table = {**nfa_1.table, **nfa_2.table}
        new_init = State()
        new_final = State()
        table[new_init] = dict()
        table[new_final] = dict()
        alphabet_with_e = alphabet if 'ε' in alphabet else alphabet + ['ε']
        for c in alphabet_with_e:
            table[new_init][c] = set()
            table[new_final][c] = set()
        table[new_init]['ε'].add(nfa_1.init_state)
        table[new_init]['ε'].add(nfa_2.init_state)
        table[nfa_1.final_states[0]]['ε'].add(new_final)
        table[nfa_2.final_states[0]]['ε'].add(new_final)
        states = [new_init]
        states.extend(nfa_1.Q)
        states.extend(nfa_2.Q)
        states.append(new_final)
        return NFA(states, alphabet, new_init, [new_final], table)

    @classmethod
    def concatenation(cls, nfa_1, nfa_2):
        alphabet = nfa_1.alphabet
        alphabet_with_e = alphabet if 'ε' in alphabet else alphabet + ['ε']
        final_state = nfa_1.final_states[0]
        n_init_state = nfa_2.init_state
        for state in nfa_1.Q:
            for c in alphabet_with_e:
                if final_state in nfa_1.table[state][c]:
                    nfa_1.table[state][c].remove(final_state)
                    nfa_1.table[state][c].add(n_init_state)
        temp = {}
        for c in alphabet_with_e:
            temp[c] = nfa_1.table[final_state][c].union(nfa_2.table[n_init_state][c])
        table = nfa_1.table
        for state in nfa_2.Q:
            table[state] = nfa_2.table[state]
        table[n_init_state] = temp
        states = nfa_1.Q
        states.remove(final_state)
        states.extend(nfa_2.Q)
        return NFA(states, alphabet, nfa_1.init_state, nfa_2.final_states, table)

    @classmethod
    def star(cls, nfa):
        alphabet = nfa.alphabet
        init_state = State()
        final_state = State()
        table = nfa.table
        table[init_state] = dict()
        table[final_state] = dict()
        alphabet_with_e = alphabet if 'ε' in alphabet else alphabet + ['ε']
        for c in alphabet_with_e:
            table[init_state][c] = set()
            table[final_state][c] = set()
        table[init_state]['ε'].add(nfa.init_state)
        table[init_state]['ε'].add(final_state)
        table[nfa.final_states[0]]['ε'].add(final_state)
        table[nfa.final_states[0]]['ε'].add(nfa.init_state)
        states = [init_state]
        states.extend(nfa.Q)
        states.append(final_state)
        return NFA(states, alphabet, init_state, [final_state], table)


    def draw(self):
        string = """digraph G{
label = """ + '"' + '' + '"' + """
rankdir = LR;
node [shape = circle];
node [shape = doublecircle]; 
"""
        s = [self.init_state]
        edge_set = set()
        for e in self.final_states:
            string = string + ' ' + "\""+e.name+"\""
        string += ';\nnode [shape = circle];\n'
        string += "\""+self.init_state.name+"\"[fillcolor=gray, style=filled];"
        alphabet = self.alphabet if 'ε' in self.alphabet else self.alphabet + ['ε']
        while len(s) != 0:
            state = s.pop()
            for c in alphabet:
                if len(self.table[state][c]) != 0 and (state, c) not in edge_set:
                    edge_set.add((state, c))
                    for des in self.table[state][c]:
                        if c != 'ε':
                            string = string + '\n'+'"'+state.name+'"'+' -> '+'"'+des.name+'"'+' [label = "' + c + '"];'
                        else:
                            string = string + '\n'+'"'+state.name+'"'+' -> '+'"'+des.name+'"'+' [label = "' + 'ε' + '"];'
                    s.extend(list(self.table[state][c]))
        string += '}'
        s = Source(string, filename="nfa.gv", format="png")
        s.render()

    def rename_states(self):
        for index, s in enumerate(self.Q):
            s.name = str(index)
            
    def move(self, states, character):
        result = set()
        for s in states:
            result.update(self.table[s][character])
        return result
    
    def e_closure(self, states):
        result = set()
        for s in states:
            result.add(s)
            stack = [s]
            while len(stack) != 0:
                c_s = stack.pop()
                closure = self.table[c_s]['ε']
                for c in closure:
                    if c not in result:
                        stack.append(c)
                        result.add(c)
        return result
    
    
    def to_dfa(self):
        from DFA import DFA
        def combine_state(states):
            name = ','.join(sorted([e.name for e in states]))
            return State(name)
        states = []
        closures = []
        marked = []
        final_states = []
        e_closure = self.e_closure((self.init_state,))
        init_state = combine_state(e_closure)
        states.append(init_state)
        closures.append(e_closure)
        marked.append(False)
        table = dict()
        while False in marked:
            for i in range(len(marked)):
                if marked[i] == False:
                    current_state = states[i]
                    closure = closures[i]
                    marked[i] = True
                    break
            current_dict = dict()
            table[current_state] = current_dict
            print(self.alphabet)
            for c in self.alphabet:
                move = self.move(closure, c)
                #print('Move:', closure, c, move)
                current_closure = self.e_closure(move)
                #print('Closure:', current_closure)
                if len(current_closure) != 0 and current_closure not in closures:
                    new_state = combine_state(current_closure)
                    states.append(new_state)
                    closures.append(current_closure)
                    marked.append(False)
                    current_dict[c] = new_state
                elif len(current_closure) != 0:
                    for state_index in range(len(states)):
                        if current_closure == closures[state_index]:
                            current_dict[c] = states[state_index]
                else:
                    current_dict[c] = None
        for i in range(len(states)):
            for s in self.final_states:
                if s in closures[i]:
                    final_states.append(states[i])
        return DFA(states, self.alphabet, init_state, final_states, table)
    
    def merge_next(self, next_nfa):
        if len(self.final_states) > 1:
            raise Exception("Lỗi")
        final_state = self.final_states[0]
        n_init_state = next_nfa.init_state
        for state in self.Q:
            for c in self.alphabet:
                if self.table[state][c] == final_state:
                    self.table[state][c] = n_init_state
        temp = {}
        for c in self.alphabet:
            temp[c] = self.table[final_state][c].union(next_nfa.table[n_init_state][c])
        self.table = {**self.table, **next_nfa}
        del self.table[final_state]
        self.table[n_init_state] = temp
        self.Q.remove(final_state)
        self.Q.extend(next_nfa.Q)
        self.final_states = next_nfa.final_states
    
    def to_regex(self):
        from Regex import Regex
        '''
        def char_format(a):
            if len(a) > 1:
                return '(' + a + ')'
            else:
                return a
        def star(a):
            if a != '':
                return char_format(a) + '*'
            else:
                return 'ε'
        def concat2(a, b):
            if a == '' or b == '':
                return ''
            else:
                if a == 'ε' and b == 'ε':
                    return 'ε'
                elif a !=  'ε' and b == 'ε':
                    return a
                elif a == 'ε' and b != 'ε':
                    return b
                else:
                    return char_format(a) + '.' + char_format(b)
        def concat3(a, b, c):
            if a == 'ε':
                return concat2(b, c)
            elif b == 'ε':
                return concat2(a, c)
            elif c == 'ε':
                return concat2(a, b)
            return char_format(a) + '.' + char_format(b) + '.' +  char_format(c)
        gnfa_table = [['' for _ in range(len(self.Q) + 2)] for _ in range(len(self.Q) + 2)]
        for i1, state in enumerate(self.Q):
            for c in self.alphabet:
                for i2, des_state in enumerate(self.Q):
                    if des_state in self.table[state][c]:
                        if gnfa_table[i1+1][i2+1] == '':
                            gnfa_table[i1+1][i2+1] = c
                        else:
                            gnfa_table[i1+1][i2+1] += ('+' + c)
        gnfa_table[0][self.Q.index(self.init_state)+1] = 'ε'
        for state in self.final_states:
            gnfa_table[self.Q.index(state)+1][-1] = 'ε'
        n = len(self.Q)
        for i, _ in enumerate(self.Q):
            for j in range(i+2, n+2):
                if gnfa_table[0][i+1] != '' and gnfa_table[i+1][j] != '':
                    regex = concat3(gnfa_table[0][i+1], star(gnfa_table[i+1][i+1]), gnfa_table[i+1][j])
                    if gnfa_table[0][j] != '':
                        gnfa_table[0][j] = gnfa_table[0][j] + '+' + regex
                    else:
                        gnfa_table[0][j] = regex
        return Regex(gnfa_table[0][n+1], self.alphabet)
        '''
        return self.to_dfa().to_regex()
    
    def to_grammar(self):
        from Grammar import ReGrammar
        char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$"
        V_T = self.alphabet
        V_N = [char[i] for i, _ in enumerate(self.Q)]
        S = char[self.Q.index(self.init_state)]
        P = dict()
        for idx, q in enumerate(self.Q):
            P[char[idx]] = set()
            for a in self.alphabet:
                for d in self.table[q][a]:
                    P[char[idx]].add(a + char[self.Q.index(d)])
        for idx, q in enumerate(self.final_states):
            P[char[self.Q.index(q)]].add('ε')
        return ReGrammar(V_N, V_T, P, S)
                 

if __name__ == '__main__':
    text = '''1 2 3 4 5
a b
0
4
0 a 2
0 empty 1
1 a 3
2 b 3
1 a 4
3 a 4
3 b 4'''
    nfa = NFA.from_text(text)
    nfa.draw()
    print(nfa.to_grammar().to_string())
    

    