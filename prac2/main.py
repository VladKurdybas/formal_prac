from lr_to_latex import table_to_latex


class LR_table:
    class Rule:
        def __init__(self, s):
            self.l, self.r = s.split('->')
            if self.r == 'ε':
                self.r = ''

    def __init__(self, grammar):
        self.rules = [LR_table.Rule(rule) for rule in grammar]
        self.table_rows = list()

        for rule in self.rules:
            for dot_position in range(len(rule.r) + 1):
                self.table_rows.append((rule, dot_position))

        self.lower_letters = set()
        self.upper_letters = set()
        for rule in self.rules:
            if rule.l != 'S\'':
                self.upper_letters.add(rule.l)
            self.lower_letters |= set([letter for letter in rule.r
                                       if letter.islower()])
        self.lower_letters = list(self.lower_letters)
        self.lower_letters.sort()
        self.lower_letters.append('$')
        self.lower_letters.append('ε')
        self.upper_letters = list(self.upper_letters)
        self.upper_letters.sort()
        self.tex = str()

        self.__find_follows()
        self.__fill_table()

        self.before_epsilon_removal = [dict() for _ in range(len(self.table_rows))]
        for i in range(len(self.table_rows)):
            for j in self.cols():
                self.before_epsilon_removal[i][j] = self.table[i][j]
        self.__remove_epsilon()

    def __find_follows(self):
        self.follows = dict()
        for i in self.upper_letters:
            self.follows[i] = set()
        self.follows['S\''] = set()

        q = ['S\'$']
        max_q_size = 10000
        position = 0
        while position < len(q):
            s = q[position]
            position += 1
            for rule in self.rules:
                start = 0
                while True:
                    f = s.find(rule.l, start)
                    if f == -1:
                        break
                    start = f + len(rule.l)
                    if s[f + len(rule.l)] == '\'':
                        continue
                    if len(q) < max_q_size:
                        q.append(s[:f] + rule.r + s[start:])

            for i in range(len(s)):
                if s[i].isupper():
                    if s[i + 1] != '\'':
                        if s[i + 1].islower() or s[i + 1] == '$':
                            self.follows[s[i]].add(s[i + 1])
                    elif s[i + 2].islower() or s[i + 2] == '$':
                        self.follows[s[i] + '\''].add(s[i + 2])

        for i in self.upper_letters:
            self.follows[i] = list(self.follows[i])
        self.follows['S\''] = list(self.follows['S\''])

    def __fill_table(self):
        self.table = [dict() for _ in range(len(self.table_rows))]
        for row in self.table:
            for lower_letter in self.lower_letters:
                row[lower_letter] = list()
            for upper_letter in self.upper_letters:
                row[upper_letter] = list()

        for i in range(len(self.table_rows)):
            s, dot_position = self.table_rows[i]

            if dot_position < len(s.r):
                self.table[i][s.r[dot_position]].append(i + 1)
                if s.r[dot_position].isupper():
                    for j in range(len(self.table_rows)):
                        rule, dot = self.table_rows[j]
                        if rule.l == s.r[dot_position] and dot == 0:
                            self.table[i]['ε'].append(j)
            else:
                r = [i for i in range(len(self.rules))
                     if self.rules[i] == s][0]
                for follow in self.follows[s.l]:
                    self.table[i][follow].append('r%d' % r)

    def __dfs(self, i, row):
        if row != i:
            self.epsilon_dependency[i].append(row)
        self.__visited[row] = True
        for to in self.table[row]['ε']:
            if not self.__visited[to]:
                self.__dfs(i, to)

    def cols(self):
        return self.lower_letters + self.upper_letters

    def __remove_epsilon(self):
        kek = 0
        states = len(self.table_rows)
        self.epsilon_dependency = [list() for _ in range(states)]
        for i in range(states):
            self.__visited = [False for _ in range(states)]
            self.__dfs(i, i)

        for i in range(states):
            for j in self.epsilon_dependency[i]:
                for letter in self.cols():
                    if letter != 'ε' and not self.table[i][letter]:
                        self.table[i][letter] = self.table[j][letter]

        for i in range(states):
            for j in self.epsilon_dependency[i]:
                equals = list()
                for letter in self.cols():
                    if letter != 'ε' and self.table[i][letter] \
                            and self.table[j][letter]:
                        equals.append((self.table[i][letter][0],
                                       self.table[j][letter][0]))
                for i1, j1 in equals:
                    if i1 != j1:
                        for letter in self.cols():
                            if letter != 'ε':
                                kek += 1
                                print(kek, i1, letter)
                                t = set(self.table[i1][letter]) | \
                                    set(self.table[j1][letter])
                                self.table[i1][letter] = list(t)
                                self.table[j1][letter] = list(t)

    def check(self, s):
        stack = [0]
        for c in s + '$':
            while True:
                row = stack[-1]
                if not self.table[row][c]:
                    return False
                rule = self.table[row][c][0]
                if c == '$' and rule == 'r0':
                    return True
                if isinstance(rule, int):
                    stack.extend([c, rule])
                    break
                rule_number = int(rule[1:])
                to_pop = list(self.rules[rule_number].r)
                while to_pop:
                    stack.pop()
                    if not stack or stack[-1] != to_pop[-1]:
                        return False
                    stack.pop()
                    to_pop.pop()
                rule_letter = self.rules[rule_number].l
                r = stack[-1]
                if not self.table[r][rule_letter]:
                    return False
                stack.extend([rule_letter, self.table[r][rule_letter][0]])
        return False


if __name__ == '__main__':
    grammar = []
    words = list()
    rules = int(input())
    for i in range(rules):
        rule = input()
        grammar.append(rule)
    words_count = int(input())
    for i in range(words_count):
        words.append(input())
    table = LR_table(grammar)
    table_to_latex(table, words)
