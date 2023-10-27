from fractions import Fraction

# НЕ ЗАБЫТЬ РАБОТУ С ДРОБЯМИ

def read_condition():
    condition = input().strip().split(' ')
    if condition[0] == '':
        return []
    return condition

def try_parse_int(value):
    try:
        return int(value)
    except ValueError:
        return value


def to_numbers(l: list):
    return [try_parse_int(x) for x in l]

def read_system():
    initial_input = to_numbers(input().strip().split(' '))
    var_count = len(initial_input) - 1
    initial_func = initial_input[:var_count]
    min_max = initial_input[var_count]

    conditions = []
    condition_input = read_condition()
    while len(condition_input) > 0:
        conditions.append(to_numbers(condition_input))
        condition_input = read_condition()
    
    return [
        initial_func,
        min_max,
        to_canonical_form(conditions)
    ]


def to_canonical_form(conditions: list[list[str]]):
    reformed = []
    to_form_count = sum([1 if c[-2] != "=" else 0 for c in conditions])
    already_formed = 0

    for condition in conditions:
        new_condition = condition.copy()
        sign = condition[-2]
        if sign == "<=":
            new_condition[-2:-2] = [1 if already_formed == x
                                    else 0
                                    for x in range(to_form_count)]
            already_formed += 1
        elif sign == ">=":
            new_condition[-2:-2] = [-1 if already_formed == x
                                    else 0
                                    for x in range(to_form_count)]
            already_formed += 1
        else:
            new_condition[-2:-2] = [0 for x in range(to_form_count)]
        new_condition[-2] = '='
        reformed.append(new_condition)
    return reformed


def to_string(equation: list, is_condition = True):
    n = len(equation)
    if is_condition:
        n -= 2
    output = ""
    counter = 1
    while counter <= n:
        eq_num = equation[counter-1]
        if not isinstance(eq_num, int):
            counter += 1
            continue
        if counter == 1:
            output += f"{eq_num}"
        else:
            if equation[counter-1] >= 0:
                output += f" + {eq_num}"
            else:
                output += f" - {eq_num*-1}"
        counter += 1
    
    if is_condition:
        output += f" {equation[-2]} {equation[-1]}"
    return output


def print_system(system):
    initial, min_max, conditions = system
    print("f(x) = " + to_string(initial, False) + " -> " + min_max)
    for condition in conditions:
        print(to_string(condition))


def to_matrix(conditions: list[list]):
    matrix = []
    for condition in conditions:
        row = [x for x in condition if isinstance(x, int)]
        matrix.append(row)
    return matrix


def init_array(row_size, column_size = 0, value=None):
    if column_size == 0:
        return [value for _ in range(row_size)]
    return [[value for _ in range(column_size)] for _ in range(row_size)]


def find_min_indices(arr):
    # Находим минимальный по модулю элемент, исключая 0
    min_val = min(filter(lambda x: x != 0, map(abs, arr)))

    # Находим все индексы элементов с минимальным модулем
    min_indices = [i for i, x in enumerate(arr) if abs(x) == min_val and x != 0]

    return min_indices

def solve_step(
        basic_equation: list[int],
        is_min: bool,
        matrix: list[list[int]],
        picked_vars: list[tuple[int, int]],
):
    """
    picked_vars - индексы взятых базисных переменных (строка, колонка)
    """
    row_length = len(matrix[0]) # учитывается b
    new_matrix = [[0]*row_length for x in range(len(matrix))]
    цэшки = init_array(len(matrix))
    for var_coordinate in picked_vars:
        цэшки[var_coordinate[0]] = basic_equation[var_coordinate[1]]
    

    # находим дельту Сб_i * x_i - initial_i
    deltas = init_array(row_length, value=0)
    for row_idx, row in enumerate(matrix):
        for idx, value in enumerate(row):
            deltas[idx] += цэшки[row_idx] * value
    for idx in range(row_length-1):
        deltas[idx] -= basic_equation[idx]

    # находим тету для нужных дельт (дельта по минимальному модулю)
    what_deltas = find_min_indices(deltas[:-1:])
    tetas = []
    for var_idx in what_deltas:
        teta = []
        for row in matrix:
            if row[var_idx] < 0 or row[-1] < 0:
                teta.append(float("inf"))
                continue
            teta.append(row[-1]/row[var_idx])
        tetas.append(teta)

    
    # выбираем следущую базовую переменную
    next_basic = None
    for i in range(len(what_deltas)):
        column_idx = what_deltas[i]
        row_idx = tetas[i].index(min(tetas[i]))
        next_basic = (row_idx, column_idx)

    print(next_basic)

    # заменяем X базовую
    # преобразовываем и возвращаем new_matrix
    
    return [new_matrix]


def check_basic(arr):
    return arr.count(1) == 1 and all(x == 0 or x == 1 for x in arr)

def initial_basic_vars(matrix):
    row_length = len(matrix[0])
    columns = init_array(row_length, len(matrix))
    print(columns)
    for row_idx, row in enumerate(matrix):
        for column_idx, j in enumerate(row):
            columns[column_idx][row_idx] = j
    print(columns)
    
    vars = []
    for column_idx, column in enumerate(columns):
        if check_basic(column):
            one_idx = 0
            for i, value in enumerate(column):
                if value == 1:
                    one_idx = i
                    break
            vars.append((one_idx, column_idx))
    print(vars)
    return vars


def simplex_solve(system):
    initial, min_max, conditions = system
    matrix = to_matrix(conditions)
    initial_vars = initial_basic_vars(matrix)
    if min_max == "min":
        pass
    elif min_max == "max":
        pass
    elif min_max == "extr":
        pass
    # пока is_min == False => max
    result = solve_step(initial, False, matrix, initial_vars)
    print(result)


if __name__ == "__main__":
    system = read_system()
    # print_system(system)
    simplex_solve(system)
