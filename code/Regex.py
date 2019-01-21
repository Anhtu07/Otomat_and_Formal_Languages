from State import State
from collections import deque

class Regex:
    op = ['.', '+', '*']
    p = ['(', ')']
    pre = [2, 1, 2]
    def __init__(self, string, alphabet):
        self.string = string
        self.parsed_string = self.parse()
        self.alphabet = alphabet

    def __repr__(self):
        return self.string
    
    def parse(self):
        s = self.string.replace(' ', '')
        queue = deque()
        stack = list()
        for w in s:
            if w not in self.op+self.p:
                queue.append(w)
            else:
                if w == '(':
                    stack.append(w)
                elif w == ')':
                    while len(stack) != 0 and stack[-1] != '(':
                        queue.append(stack.pop())
                    stack.pop()
                else:
                    while len(stack) != 0 and ((stack[-1] in self.op and self.pre[self.op.index(stack[-1])] > self.pre[self.op.index(w)]) or (stack[-1] == '*')):
                        queue.append(stack.pop())
                    stack.append(w)
        queue.extend(stack[::-1])
        return queue
    
    
    def to_nfa(self):
        from NFA import NFA
        stack = list() 
        for w in self.parsed_string:
            if w not in self.op:
                nfa = NFA.single_char(self.alphabet, w)
                nfa.rename_states()
                stack.append(nfa)
            elif w == '+':
                nfa_2 = stack.pop()
                nfa_1 = stack.pop()
                stack.append(NFA.union(nfa_1, nfa_2))
            elif w == '.':
                nfa_2 = stack.pop()
                nfa_1 = stack.pop()
                stack.append(NFA.concatenation(nfa_1, nfa_2))
            elif w == '*':
                nfa_1 = stack.pop()
                stack.append(NFA.star(nfa_1))
        result = stack.pop()
        return result

if __name__ == '__main__':
    string = 'ε+a*.b'
    alphabet = ['a', 'b']
    regex = Regex(string, alphabet)
    nfa = regex.to_nfa()
    nfa.rename_states()
    nfa.draw() 
    dfa = nfa.to_dfa()
    dfa.minimize()
    dfa.draw()
    # dfa.rename_states()