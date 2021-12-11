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
