# FILE : nonogram.py
# DESCRIPTION: A program that solves a game called "black and solve"
# The reason I choose in the function "intersection_row" to colour
# (black or white) the squares, not to leave them neutral, is because I
# wanted to finish the board into a clear solution as close as possible.
# also, if we will keep the squares neutral by indecision, it could destroy our
# solutions, by leaving too many options open, that open the door to wrong
# future color decisions because it makes too many solutions, and eventually
# we need to decide in a logical way if the square is white or black.

import time


def constraint_satisfactions(n, blocks):
    """
    this function returns all the possible options to color the nonogram.
    it takes as an argument n = len of list, blocks = constraints
    """
    return _helper_constraint(n, blocks, [])


def _helper_constraint(n, blocks, lst):
    """
    this is a help function to the constraint function. it takes as an
    argument len of list, constraints as blocks and a list. its activating
    the next helper recursive function.
    """
    for num in blocks:
        first_list = []
        for i in range(num):
            first_list.append(1)
        lst.append(first_list)
    return _recu_constraint(n, blocks, lst, [], 0, 0, [])


def _recu_constraint(n, blocks, main_lst, res, cur_b, cur_z, listic):
    """
     this is a help function to the constraint function. it takes as an
     argument len of list, constraints as blocks and a list. the
     output of the function is a possible options to color the nonogram
     considering the wanted len and the constraints.
     """
    if len(listic) == n:
        res.append(listic[:])
        return

    if sum(blocks) > n:
        return []

    if (cur_b < (len(main_lst)) and not listic) or (cur_b < (len(main_lst)) and
                                                    (listic[-1]) == 0):
        _recu_constraint(n, blocks, main_lst, res, cur_b + 1, cur_z, listic +
                         main_lst[cur_b])
    if cur_z < n - sum(blocks):
        _recu_constraint(n, blocks, main_lst, res, cur_b, cur_z + 1,
                         listic + [0])
    return res


def row_variations(row, blocks):
    """
    this function takes a line from a nonogram, and returns a list
    which returns all the possible options to complete the coloring options
    considering the constraints
    """
    return _helper_row_variations(row, blocks, 0, row[:], [])


def _helper_row_variations(row, blocks, indx, lst, res):
    """
    this function takes a line from a nonogram, and returns a list
    which returns all the possible options to complete the coloring options
    considering the constraints.
    """
    if indx == len(lst) and len(blocks) == 0:
        res.append(lst[:])
        return res
    elif indx >= len(lst) and len(blocks) > 0:
        return res
    if lst[indx] == -1:
        if (indx >= 1 and lst[indx - 1] == 0) or indx == 0:
            if len(blocks) > 0 and 0 not in lst[indx:indx + blocks[0]] and \
                    blocks[0] <= len(lst[indx:]):
                lst[indx:indx + blocks[0]] = [1] * blocks[0]
                _helper_row_variations(row, blocks[1:], indx + blocks[0], lst,
                                       res)
                lst[indx:indx + blocks[0]] = row[indx:indx + blocks[0]]
                lst[indx] = 0
                _helper_row_variations(row, blocks, indx + 1, lst, res)
                lst[indx] = -1
                return res
        lst[indx] = 0
        _helper_row_variations(row, blocks, indx + 1, lst, res)
        lst[indx] = -1
    elif lst[indx] == 1:
        if ((indx >= 1 and lst[indx - 1] == 0) or indx == 0) and (
                len(blocks) > 0 and 0 not in lst[indx:indx + blocks[0]]):
            lst[indx:indx + blocks[0]] = [1] * blocks[0]
            _helper_row_variations(row, blocks[1:], indx + blocks[0], lst, res)
            lst[indx:indx + blocks[0]] = row[indx:indx + blocks[0]]
        else:
            return res
    elif lst[indx] == 0:
        _helper_row_variations(row, blocks, indx + 1, lst, res)
    return res


def intersection_row(rows):
    """
    this function takes a several options to put into the nonogram,
     and returns a line that has the mutual constraints to all the
     lines in order to fit the wanted nonogram.
    """
    row = []
    for i in range(len(rows[0])):
        res = set()
        for num in range(len(rows)):
            res.add(rows[num][i])
            if (0 in res and 1 in res):
                row.append(-1)
                break
            else:
                continue
        if (1 not in res and -1 not in res) or (0 in res and 1 not in res):
            row.append(0)
        if (0 not in res and -1 not in res) or (1 in res and 0 not in res):
            row.append(1)
        if 0 not in res and 1 not in res:
            row.append(-1)
    return row


def solve_easy_nonogram(constraints):
    """
    this function solves in a simple way an easy nonogram.
    this function takes as a argument constraints and returns the
    final result.
    """
    return _first_helper_easy_row(constraints, [])


def _first_helper_easy_row(constraints, new_list_row):
    """
    this function takes as an argument constraints and a list,
    and sends the possible rows to the col function.
    """
    number_of_rows = len(constraints[0])
    number_of_cols = len(constraints[1])
    for index in range(number_of_rows + 1):
        if index == number_of_rows:
            ordered_list = order_nonogram(new_list_row)
            return _helper_easy_col(constraints, ordered_list, [])
        result_row = constraint_satisfactions(number_of_cols,
                                              constraints[0][index])
        if not result_row:
            return None
        else:
            x = intersection_row(result_row)
            new_list_row.append(x)
    return new_list_row


def _helper_easy_col(constraints, nonogram, new_list_col=[]):
    """
    this function takes as an argument constraints  a list,
    nonogram, and sends the possible cols considering the last possible
    rows, and sends it back to check the cols into the row function.
    """
    number_of_cols = len(constraints[1])
    for index in range(number_of_cols + 1):
        if new_list_col == nonogram:
            new_nonogram = order_nonogram(new_list_col)
            return new_nonogram
        if index == number_of_cols:
            ordered_list = order_nonogram(new_list_col)
            return _helper_easy_row(constraints, ordered_list, [])
        result_col = row_variations(nonogram[index], constraints[1][index])
        if not result_col:
            return None
        else:
            x = intersection_row(result_col)
            new_list_col.append(x)
    return nonogram


def _helper_easy_row(constraints, nonogram, new_list_row=[]):
    """
    this function takes as an argument constraints  a list,
    nonogram, and sends the possible rows considering the last possible
    row and the last possible cols, and sends it back to check the cols
    into the col function.
    """
    number_of_rows = len(constraints[0])
    for index in range(number_of_rows + 1):
        if new_list_row == nonogram:
            return new_list_row
        if index == number_of_rows:
            ordered_list = order_nonogram(new_list_row)
            return _helper_easy_col(constraints, ordered_list, [])
        result_row = row_variations(nonogram[index], constraints[0][index])
        if not result_row:
            return None
        else:
            x = intersection_row(result_row)
            new_list_row.append(x)
    return nonogram


def order_nonogram(nonogram):
    """
    this function takes as an argument nonogram, and change the position
    of it. it changes the cols into rows and the rows into cols.
    """
    order_list = []
    for i in range(len(nonogram[0])):
        res = []
        for num in range(len(nonogram)):
            res.append(nonogram[num][i])
        order_list.append(res)
    return order_list


def solve_nonogram(constraints):
    """
    this function takes as an argument constraints  and by depending
    on the previous function it can solve any nonogram. this function
    returns all the possible solutions to the given constraints.
    """
    res = []
    nongram = solve_easy_nonogram(constraints)
    if nongram is None:
        return
    tuple_num = find_minus_one(nongram)
    if tuple_num is None:
        return [nongram]
    nongram[tuple_num[0]][tuple_num[1]] = 0
    x = _helper_easy_row(constraints, nongram, [])
    _helper_solve_nonogram(constraints, x, res)
    nongram[tuple_num[0]][tuple_num[1]] = 1
    _helper_solve_nonogram(constraints, nongram, res)
    return res


def _helper_solve_nonogram(constraints, nongram, res):
    """
    this is a helper function to the solve nonogram function.
    it takes as an argument constraints, nongram from the main
    function, and a list. it returns all the possible solutions
    to the given constraints.
    """
    if not nongram:
        return
    if (len(nongram) != 0) and (
            -1 not in (item for sublist in nongram for item in sublist)):
        res.append(nongram)
        return
    tuple_num = find_minus_one(nongram)
    nongram[tuple_num[0]][tuple_num[1]] = 0
    new_non = _helper_easy_row(constraints, nongram, [])
    if new_non is None:
        return
    _helper_solve_nonogram(constraints, new_non, res)
    nongram[tuple_num[0]][tuple_num[1]] = 1
    new_non = _helper_easy_row(constraints, nongram, [])
    _helper_solve_nonogram(constraints, new_non, res)
    return res


def find_minus_one(nongram):
    """
    this is a helper function to the solve nonogram function.
    it takes as an argument a nongram and returns each time
    the current indx of the minus one in the nongram.
    """
    for indx_line in range(len(nongram)):
        for indx_num in range(len(nongram[0])):
            if nongram[indx_line][indx_num] == -1:
                index = (indx_line, indx_num)
                return index


start = time.time()
solve_nonogram([[[1,8], [3,11], [1,14], [5,17], [7,15], [1,1,1,1,9], [1,1,1,1,3], [9], [1,1,1,1,4], [1,1,1,1,12],
             [8,17], [6,14], [1,7,1,12], [11,9], [9,7], [9,4], [8,2], [7], [7], [1,5], [1,5], [1,7,1],
            [11], [6,3], [5,2], [4,1],[7], [7], [1,5], [1,5], [1,5], [7,2], [4,1,2], [5,13], [5,14],
            [22], [2,19], [2,20],[23], [11,2,1,3], [11,2,1,2], [23], [28], [30], [30]],
            [[2], [3], [2,3,3], [4,3,3,12], [4,1,33],[2,1,9,7,5,7], [1,42], [5,1,35], [1,20,6,10],
             [2,1,13,6,10], [4,35], [3,4,3,12], [2,2,3,12], [4,3,12], [4,3,8,4], [4,3,8,4],
             [4,4,12], [4,3,12], [4,4,6,4], [5,4,6,4],[5,4,12], [4,5,6,4], [5,5,6,4],[5,6,11],
             [5,6,10], [5,5,3,4], [5,6,3], [4,6,3], [4,7,3], [4,7,3]]])
end = time.time()
print(end - start)
