from const import NOT, OR


def sortClause(clause):
    '''
    Return clause in alphabetical order
    '''
    for i in range(1, len(clause)):
        # Turn flag off
        swapped = False
        # loop to compare array elements
        for j in range(1, len(clause) - i):
            # Extract name of literals
            if type(clause[j]) == str:
                valueOfJ = clause[j]
            else:
                valueOfJ = clause[j][1]

            if type(clause[j + 1]) == str:
                valueOfJ_1 = clause[j + 1]
            else:
                valueOfJ_1 = clause[j + 1][1]
            # Compare two adjacent elements
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


def str_to_struct(str):
    if len(str.split(OR)) == 1:
        if '-' in str:
            return [NOT, str
                    .replace(' ', '')
                    .replace('\n', '')
                    .replace('-', '')]
        else:
            return str.replace(' ', '').replace('\n', '')
    # EXtract literal from input
    literals = str.split(OR)
    for index in range(len(literals)):
        if '-' in literals[index]:
            literals[index] = [NOT, literals[index]
                               .replace(' ', '')
                               .replace('\n', '')
                               .replace('-', '')]
        else:
            literals[index] = (literals[index]
                               .replace(' ', '')
                               .replace('\n', ''))
    # Sort literal before return
    ans = [OR]
    for literal in literals:
        ans.append(literal)
    return ans


def struct_to_str(line):
    ans = ''
    if type(line) == list:
        if len(line) > 0:
            if line[0] == OR:
                for literal in line[1:]:
                    ans += literal_to_str(literal)
                    ans += ' {} '.format(OR)
                ans = ans[:-4]
                return ans
            else:
                return '-' + line[1]
        else:
            return '{}'
    return line


def literal_to_str(literal):
    if type(literal) == str:
        return literal
    return '-' + literal[1]
