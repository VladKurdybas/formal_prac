import tex

import os


def table_to_latex(lr_table, words):
    document = tex.Document()

    document.add(tex.Section('Грамматика'))
    rules = tex.Enumeration(0)
    for rule in lr_table.rules:
        rules.add('$' + rule.l + ' ' + tex.right_arrow + ' ' +
                  (tex.epsilon if not rule.r else rule.r) + '$')
    document.add(rules)

    document.add(tex.Section('Таблица переходов'))
    for s, followers in sorted(lr_table.follows.items()):
        document.add('$Follow(%s) = \{ %s \}$' % (s, ', '.join(sorted([
            '\$' if s == '$' else tex.epsilon
            if s == 'ε' else s for s in followers]))))
    document.add(tex.empty_line)
    table = tex.Table(len(lr_table.cols()) + 2)
    table.add_row(['\\textnumero', 'Правило'] + list(map(tex.screen, lr_table.cols())))
    for i in range(len(lr_table.table_rows)):
        rule, dot = lr_table.table_rows[i]
        row = [i, '$' + rule.l + ' ' + tex.right_arrow + ' '
               + rule.r[:dot] + ' \cdot ' + rule.r[dot:] + '$']
        for col in lr_table.cols():
            cell = ', '.join(['$%s$' % ('r_%d' % int(c[1:]) if isinstance(c, str)
                                        else str(c)) for c in lr_table.table[i][col]])
            if cell and not lr_table.before_epsilon_removal[i][col]:
                cell = tex.red(cell)
            row.append(cell)
        table.add_row(row)
    document.add(table)
    document.add(tex.empty_line)
    document.add(tex.red('Красным') + ' обозначены переходы, появившиеся после устранения $'
                 + tex.epsilon + '$-переходов.')

    for word in words:
        document.add(tex.Section('Разбор ' + tex.italic(word)))
        table = tex.Table(3)
        table.add_row(['Индекс', 'Символ', 'Стек'])
        table.add_row(['', '', 0])
        stack = [0]
        ind = 0
        match = None
        for c in word + '$':
            print_once = [ind, tex.screen(c)]
            while True:
                row = stack[-1]
                if not lr_table.table[row][c]:
                    match = False
                    break
                rule = lr_table.table[row][c][0]
                if c == '$' and rule == 'r0':
                    match = True
                    break
                if isinstance(rule, int):
                    stack.extend([c, rule])
                    table.add_row(print_once +
                                  [' '.join([tex.screen(str(s)) for s in stack])])
                    break
                rule_number = int(rule[1:])
                to_pop = list(lr_table.rules[rule_number].r)
                while to_pop:
                    stack.pop()
                    if not stack or stack[-1] != to_pop[-1]:
                        match = False
                        break
                    stack.pop()
                    to_pop.pop()
                rule_letter = lr_table.rules[rule_number].l
                r = stack[-1]
                if not lr_table.table[r][rule_letter]:
                    match = False
                    break
                stack.extend([rule_letter, lr_table.table[r][rule_letter][0]])
                table.add_row(print_once +
                              [' '.join([tex.screen(str(s)) for s in stack])])
                print_once[0] = ''
            ind += 1
            if match is not None:
                break
        document.add(table)
        document.add(tex.empty_line)
        verdict = tex.red('не входит') if not match else tex.green('входит')
        document.add('Вердикт: ' + tex.bold(verdict))

    with open('answer.tex', 'w') as f:
        f.write(str(document))
    os.system('pdflatex answer.tex > /dev/null')
    print('Response saved to answer.pdf')
    deleter()


def deleter():
    path_tex = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'answer.tex')
    os.remove(path_tex)
