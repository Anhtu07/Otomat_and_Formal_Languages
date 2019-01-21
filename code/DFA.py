from helper import DisjointSet
from graphviz import Source
from State import State

class DFA:
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
            for c in alphabet:
                table[s][c] = None
        for line in lines[4:]:
            s, c, d = line.split(' ')
            s = int(s)
            d = int(d)
            table[states[s]][c] = states[d]
        return cls(states, alphabet, init_state, final_states, table)
    
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
            string = string + ' ' + '"' + e.name + '"'
        string += ';\nnode [shape = circle];\n'
        string += '"'+self.init_state.name+'"'+"[fillcolor=gray, style=filled];"
        while len(s) != 0:
            state = s.pop()
            for c in self.alphabet:
                if self.table[state][c] is not None and (state, c) not in edge_set:
                    edge_set.add((state, c))
                    string = string + '\n'+'"'+state.name+'"'+' -> '+'"'+self.table[state][c].name+'"'+' [label = "' + c + '"];'
                    s.append(self.table[state][c])
        string += '}'
        s = Source(string, filename="dfa.gv", format="png")
        s.render()

    def rename_states(self):
        for index, s in enumerate(self.Q):
            s.name = str(index)
    
    def remove_unreachable_states(self):
        stack = [self.init_state]
        reachable_states = set()
        reachable_states.add(self.init_state)
        while stack:
            state = stack.pop()
            for c in self.alphabet:
                if self.table[state][c] not in reachable_states and self.table[state][c] is not None:
                    reachable_states.add(self.table[state][c])
                    stack.append(self.table[state][c])
        self.Q = [state for state in self.Q if state in reachable_states]
        self.final_states = [state for state in self.final_states if state in reachable_states]
    
    def minimize(self, p=False):
        def combine_state(states):
            name = ','.join(sorted([e.name for e in states]))
            return State(name)
        def order(a, b):
            return (a, b) if a.name < b.name else (b, a)

        self.remove_unreachable_states()
        table = {}
        for i, s1 in enumerate(self.Q):
            for s2 in self.Q[i+1:]:
                table[order(s1, s2)] = (s1 in self.final_states) != (s2 in self.final_states)
        found = True
        while found:
            found = False
            for i, s1 in enumerate(self.Q):
                for s2 in self.Q[i+1:]:
                    if table[order(s1, s2)]:
                        continue
                    for c in self.alphabet:
                        t1 = self.table[s1][c]
                        t2 = self.table[s2][c]
                        if t1 is not None and t2 is not None and t1 != t2:
                            print(table)
                            marked = table[order(t1, t2)]
                            found = (found or marked)
                            table[(s1, s2)] = marked
                            if marked:
                                break
                            
        d = DisjointSet(self.Q)
        for k, v in table.items():
            if not v:
                d.union(k[0], k[1])
        new_finals = []
        new_states = [combine_state(x) for x in d.get()]
        new_init = new_states[d.find_set(self.init_state)]
        
        for index, s in enumerate(d.get()):
            for item in s:
                if item in self.final_states:
                    new_finals.append(new_states[index])
                    break
        new_table = dict()
        for i, state in enumerate(new_states):
            new_table[state] = dict()
            for c in self.alphabet:
                old_s = d.get()[i][0]
                old_ds = self.table[old_s][c]
                if old_ds is None:
                    new_table[state][c] = None
                    continue
                new_ds = d.find_set(old_ds)
                new_table[state][c] = new_states[new_ds]
        return DFA(new_states, [a for a in self.alphabet], new_init, new_finals, new_table)

    def to_regex(self):
        from Regex import Regex
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
        def concat(a, b):
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
        def union(a, b):
            if a == '' and b == '':
                return ''
            elif a == '':
                return b
            elif b == '':
                return a
            else:
                return a + '+' + b
        B = ['' for _ in range(len(self.Q))]
        for final in self.final_states:
            final_index = self.Q.index(final)
            B[final_index] = 'ε'
        A = [['' for _ in range(len(self.Q))] for _ in range(len(self.Q))]
        for index, state in enumerate(self.Q):
            for c in self.alphabet:
                if self.table[state][c] is not None:
                    A[index][self.Q.index(self.table[state][c])] = c
        for n in range(len(self.Q)-1, -1, -1):
            B[n] = concat(star(A[n][n]), B[n])
            for j in range(n):
                A[n][j] = concat(star(A[n][n]), A[n][j])
            for i in range(n):
                B[i] = union(B[i], concat(A[i][n], B[n]))
                for j in range(n):
                    A[i][j] = union(A[i][j], concat(A[i][n], A[n][j]))
        return Regex(B[0], self.alphabet)
                    


if __name__ == '__main__':
    text = '''0 1 2 3
a b
0
2
0 b 1
0 a 3
1 a 2
3 a 2'''

    dfa = DFA.from_text(text)
    #dfa.draw()
    d = dfa.minimize()
    d.draw()
    #print(dfa.to_regex())
