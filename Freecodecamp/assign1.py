def arithmetic_arranger(problems, show=False):
    n = len(problems)

    while True:

        if n > 5:
            ans = "\n\tToo many problems"
            break
        elif not isValidOperator(problems):
            ans = "\n\tOperator must be '+' or '-'"
            break
        elif not areOperandsNumber(problems):
            ans = "\n\tNumbers must only contain digits"
            break
        elif not operandsLen(problems):
            ans = "\n\tNumbers cannot be more than four digits"
            break

        topvals = []
        bottomvals = []
        dashes = []
        sums_lines = []
        for problem in problems:
            line = problem.split()
            m = len(line[0])
            n = len(line[2])
            
            sum_line = None
            if line[1] == '+':
                addit = int(line[0]) + int(line[2])
                sum_line = str(addit)
            elif line[1] == '-':
                subtr = int(line[0]) - int(line[2])
                sum_line = str(subtr)

            if m >= n:
                linestop = '  ' + line[0].rjust(m)
                topvals.append(linestop)
                linesbottom = line[1] + ' ' + line[2].rjust(m)
                bottomvals.append(linesbottom)
                das = (m+2)*'-'
                dashes.append(das)
                sums_lines.append(sum_line.rjust(m+2))
            else:
                linestop = '  '+line[0].rjust(n)
                topvals.append(linestop)
                linesbottom = line[1]+' '+line[2].rjust(n)
                bottomvals.append(linesbottom)
                das = (n+2)*'-'
                dashes.append(das)
                sums_lines.append(sum_line.rjust(n+2))

        if show:
            topval = (' '*4).join(topvals)
            bottomval = (' '*4).join(bottomvals)
            dash = (' '*4).join(dashes)
            sums = (' '*4).join(sums_lines)
            ans = topval + '\n' + bottomval + '\n' + dash + '\n' + sums
            break
        else:
            topval = (' '*4).join(topvals)
            bottomval = (' '*4).join(bottomvals)
            dash = (' '*4).join(dashes)
            ans = topval + '\n' + bottomval + '\n' + dash
            break

    return ans


def isValidOperator(problems):
    er = 0
    q = True
    for problem in problems:
        if '*' in problem:
            er += 1
        elif '/' in problem:
            er += 1
        else:
            continue

    if er > 0:
        q = False

    return q


def areOperandsNumber(problems):
    er = 0
    q = True
    for problem in problems:
        lines = problem.split()
        if lines[0].isdigit() and lines[2].isdigit():
            continue
        else:
            er += 1

    if er > 0:
        q = False

    return q


def operandsLen(problems):
    er = 0
    q = True
    for problem in problems:
        lines = problem.split()
        if (len(lines[0]) > 4) or (len(lines[2]) > 4):
            er += 1

    if er > 0:
        q = False

    return q


quest = ["236 + 2", "36 - 477", "12 - 36", "22 + 6", "1 - 9999"]
a = arithmetic_arranger(quest, True)
print(a)