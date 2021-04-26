class Document:
    def __init__(self):
        self.__elements = list()

    def add(self, item):
        self.__elements.append(item)

    def __repr__(self):
        return """\
\\documentclass[12pt]{article}

\\usepackage[utf8]{inputenc}
\\usepackage[english,russian]{babel}
\\usepackage{indentfirst}
\\usepackage{textcomp}
\\usepackage[dvipsnames]{xcolor}
\\usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm,bindingoffset=0cm]{geometry}

\\begin{document}\n\n""" + \
               '\n\n'.join([str(el) for el in self.__elements]) + """\n
\\end{document}"""


class Table:
    def __init__(self, cols):
        self.__cols_number = cols
        self.__rows = list()

    def add_row(self, row):
        self.__rows.append(row)

    def __repr__(self):
        return "\\begin{tabular}{" + '|l' * self.__cols_number + \
               '|}\n\\hline\n' + '\n'.join([' & '.join([str(c) for c in row]) +
                                            '\\\\ \hline' for row in self.__rows]) + \
               '\n\\end{tabular}'


class Section:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '\\section*{' + self.text + '}'


class Enumeration:
    def __init__(self, start):
        self.start = start
        self.__items = list()

    def add(self, item):
        self.__items.append(item)

    def __repr__(self):
        return """\\begin{enumerate}
\\setcounter{enumi}{%d}
""" % (self.start-1) + '\n'.join(['\item %s' % str(s) for s in self.__items]) + """
\end{enumerate}"""


def bold(text):
    return '\\textbf{'+str(text)+'}'

def underline(text):
    return '\\underline{'+str(text)+'}'

def italic(text):
    return '\\textit{'+str(text)+'}'

def red(text):
    return '\\textcolor{red}{'+str(text)+'}'

def green(text):
    return '\\textcolor{green}{'+str(text)+'}'


right_arrow = '\\rightarrow'
epsilon = '\\varepsilon'
empty_line = '\\bigbreak'

def screen(s):
    if s == '$':
        return '$\\$$'
    if s == 'ε':
        return '$' + epsilon + '$'
    return '$' + s + '$'
