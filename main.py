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


# алгос
# 1) приводим к каноническому виду
# 2) берём первые базисные переменные
# 3) перебираем все
# если одно из b < 0 то это не ответ


def pick_basic_var(
        matrix: list[list[int]],
        picked_vars: list[tuple[int, int]],
        picked: tuple[int, int]
):
    """
    picked_vars - индексы взятых базисных переменных
    picked - индекс новой базисной переменной
    """
    row_length = len(matrix[0])
    new_matrix = [[0]*row_length for x in range(len(matrix))]
    print(new_matrix)
    
    for row in matrix:
        for index, value in enumerate(row):
            print(index, value)


def choose_some():
    return (0,0)


def to_matrix(conditions: list[list]):
    matrix = []
    for condition in conditions:
        row = [x for x in condition if isinstance(x, int)]
        matrix.append(row)
    return matrix


def solve_system(system):
    initial, min_max, conditions = system
    matrix = to_matrix(conditions)
    pick_basic_var(matrix, [], (0,1))
    print(matrix)


if __name__ == "__main__":
    system = read_system()
    # print_system(system)
    solve_system(system)
