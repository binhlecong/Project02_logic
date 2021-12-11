from const import OR


def sortClause(clause):
    '''
    Return clause in alphabetical order
    '''
    for i in range(1, len(clause)):
        # Turn flag off
        swapped = False
        # loop to compare array elements
        for j in range(1, len(clause) - i):
            # compare two adjacent elements
            # change > to < to sort in descending order
            valueOfJ = clause[j] if isinstance(
                clause[j], str) else clause[j][1]
            valueOfJ_1 = clause[j + 1] if isinstance(
                clause[j + 1], str) else clause[j + 1][1]

            if valueOfJ > valueOfJ_1:
                # Swap elements
                temp = clause[j]
                clause[j] = clause[j + 1]
                clause[j + 1] = temp
                # Turn flag on
                swapped = True
        # Stop algorithm when there were no sort
        if not swapped:
            break


def struct_to_str(line):
    ans = ''
    if isinstance(line, list):
        if len(line) > 0:
            if line[0] == OR:
                for literal in line[1:]:
                    ans += literal_to_str(literal)
                    ans += ' '
                    ans += OR
                    ans += ' '
                ans = ans[:-4]
                return ans
            else:
                literal_to_str(line)
        else:
            return '{}'
    return literal_to_str(line)


def literal_to_str(literal):
    if isinstance(literal, str):
        return literal
    return '-' + literal[1]
