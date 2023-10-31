from enum import StrEnum
from fractions import Fraction

Vector = list[Fraction]

Matrix = list[Vector]

BasisVariableIndex = tuple[int, int]

BasisVariables = list[BasisVariableIndex]


class Sign(StrEnum):
    EQ = '='
    GTE = '>='
    LTE = '<='


class LPPConstraintDenormalized:
    def __init__(self, coefficients: Vector, sign: Sign, result: Fraction):
        self.coefficients = coefficients
        self.sign = sign
        self.result = result


LPPConstraintsDenormalized = list[LPPConstraintDenormalized]


class LPPConstraint:
    def __init__(self, coefficients: Vector, result: Fraction):
        self.coefficients = coefficients
        self.result = result


LPPConstraints = list[LPPConstraint]


class LPP:
    def __init__(self, outcome: str, coefficients: Vector, constraints: LPPConstraints):
        assert outcome in ['min', 'max']

        self.outcome = outcome
        self.coefficients = coefficients
        self.constraints = constraints


def fraction_from_string(value: str) -> Fraction:
    if '/' in value:
        fraction_raw = value.split('/')
        numerator = int(fraction_raw[0])
        denominator = int(fraction_raw[1])
        return Fraction(numerator, denominator)
    else:
        return Fraction.from_float(float(value))


def zero_vector(n: int) -> Vector:
    return [Fraction(0) for _ in range(n)]


def normalize_constraints(constraints: LPPConstraintsDenormalized) -> LPPConstraints:
    to_form_count = len([constraint for constraint in constraints if constraint.sign != "="])
    formed_count = 0

    normalized_constraints = []

    for constraint in constraints:
        constraint_append_coefficients = []
        match constraint.sign:
            case Sign.EQ:
                constraint_append_coefficients = zero_vector(to_form_count)
            case Sign.LTE:
                constraint_append_coefficients = (zero_vector(formed_count) +
                                                  [1] +
                                                  zero_vector(to_form_count - formed_count - 1))
            case Sign.GTE:
                constraint_append_coefficients = (zero_vector(formed_count) +
                                                  [-1] +
                                                  zero_vector(to_form_count - formed_count - 1))

        normalized_coefficients = constraint.coefficients + constraint_append_coefficients
        normalized_constraint = LPPConstraint(normalized_coefficients, constraint.result)
        normalized_constraints.append(normalized_constraint)

    return normalized_constraints


def read_constraints_denormalized() -> LPPConstraintsDenormalized:
    constraints = []

    while True:
        constraint_raw = input().strip()
        if len(constraint_raw) == 0:
            break

        constraint_parts = constraint_raw.split(' ')
        constraint_coefficients = constraint_parts[:-2]
        constraint_coefficients = [
            fraction_from_string(constraint_coefficient)
            for constraint_coefficient in constraint_coefficients
        ]
        constraint_sign = Sign(constraint_parts[-2])
        constraint_result = fraction_from_string(constraint_parts[-1])

        constraint = LPPConstraintDenormalized(constraint_coefficients, constraint_sign, constraint_result)
        constraints.append(constraint)

    return constraints


def read_lpp() -> LPP:
    function = input().strip()

    outcome = function.split(' ')[-1]

    coefficients = function.split(' ')[:-1]
    coefficients = [fraction_from_string(coefficient) for coefficient in coefficients]

    constraints = normalize_constraints(read_constraints_denormalized())

    return LPP(outcome, coefficients, constraints)


def coefficient_to_polynom_string(i: int, coefficient: Fraction) -> str:
    if coefficient == 1:
        return f"+ x{i + 1}"
    elif coefficient > 0:
        return f"+ {coefficient}*x{i + 1}"
    elif coefficient < 0:
        return f"- {abs(coefficient)}*x{i + 1}"
    else:
        return ''


def coefficients_to_polynom_string(coefficients: Vector) -> str:
    return ' '.join([
        coefficient_to_polynom_string(i, coefficient) for i, coefficient in enumerate(coefficients) if coefficient != 0
    ])


def print_lpp(problem: LPP):
    print(f"f(X) = {coefficients_to_polynom_string(problem.coefficients)} -> {problem.outcome}")

    for constraint in problem.constraints:
        print(f"{coefficients_to_polynom_string(constraint.coefficients)} = {constraint.result}")


def is_unit_vector(vector: Vector) -> bool:
    one_found = False
    for item in vector:
        if item == 1:
            if one_found:
                return False
            else:
                one_found = True
        elif item != 0:
            return False

    return True


def get_matrix_basis(matrix) -> BasisVariables:
    columns = rotate_matrix(matrix)

    return [
        (column.index(1), column_index)
        for column_index, column in enumerate(columns)
        if is_unit_vector(column)
    ]


def constraints_to_matrix(constraints: LPPConstraints) -> Matrix:
    return [
        constraint.coefficients + [constraint.result] for constraint in constraints
    ]


def rotate_matrix(matrix: Matrix) -> Matrix:
    return list(zip(*matrix))


# TODO: Refactor it -> _solve_step
# def find_min_indices(arr, is_min=False):
#     if is_min:
#         filtered = list(filter(lambda x: x != 0 and x > 0, arr))
#     else:
#         filtered = list(filter(lambda x: x != 0 and x < 0, arr))
#     if len(filtered) == 0:
#         return []
#     min_val = min(map(abs, filtered))
#     min_indices = [i for i, x in enumerate(arr) if abs(x) == min_val and x != 0]
#
#     return min_indices
#
# def solve_step(
#         basic_equation: list[int],
#         is_min: bool,
#         matrix: list[list[int]],
#         picked_vars: list[tuple[int, int]],
# ):
#     """
#     picked_vars - индексы взятых базисных переменных (строка, колонка)
#     return: [need_stop: bool, matrix, picked_vars]
#     """
#     row_length = len(matrix[0])  # учитывается b
#     цэшки = init_array(len(matrix))
#     for var_coordinate in picked_vars:
#         цэшки[var_coordinate[0]] = basic_equation[var_coordinate[1]]
#
#     print_matrix(matrix)
#     # находим дельту Сб_i * x_i - initial_i
#     deltas = init_array(row_length, value=0)
#     for row_idx, row in enumerate(matrix):
#         for idx, value in enumerate(row):
#             deltas[idx] += цэшки[row_idx] * value
#     for idx in range(row_length - 1):
#         deltas[idx] -= basic_equation[idx]
#     print([round(x, 3) for x in deltas])
#
#     # находим тету для нужных дельт (дельта по минимальному модулю)
#     what_deltas = find_min_indices(deltas[:-1:], is_min)
#
#     # TODO: сделать красиво
#     if len(what_deltas) == 0:
#         # print_matrix(matrix)
#         return [True, None, None, None]
#     tetas = []
#     for var_idx in what_deltas:
#         teta = []
#         for row in matrix:
#             if row[var_idx] < 0 or row[-1] < 0:
#                 teta.append(float("inf"))
#                 continue
#             teta.append(row[-1] / row[var_idx])
#         tetas.append(teta)
#
#     # выбираем следущую базовую переменную
#     next_basic = None
#     # выбор если базовый вариант
#     for i in range(len(what_deltas)):
#         column_idx = what_deltas[i]
#         row_idx = tetas[i].index(min(tetas[i]))
#         next_basic = (row_idx, column_idx)
#
#     next_basic_value = matrix[next_basic[0]][next_basic[1]]
#     print(next_basic)
#     print(next_basic_value)
#
#     # заменяем X базовую
#     new_picked_vars = [next_basic
#                        if x[0] == next_basic[0]
#                        else x
#                        for x in picked_vars]
#
#     new_matrix = [[0] * row_length for x in range(len(matrix))]
#     # преобразовываем матрицу для новой базовой
#     for row_idx, row in enumerate(matrix):
#         for idx, value in enumerate(row):
#             if row_idx == next_basic[0]:
#                 if idx == next_basic[1]:
#                     new_matrix[row_idx][idx] = 1
#                 else:
#                     new_matrix[row_idx][idx] = value / next_basic_value
#             else:
#                 if idx != next_basic[1]:
#                     # пересчёт
#                     new_matrix[row_idx][idx] = (
#                                                        next_basic_value * value
#                                                        - matrix[row_idx][next_basic[1]] * matrix[next_basic[0]][
#                                                            idx]
#                                                ) / next_basic_value
#
#     return [False, new_matrix, new_picked_vars]


class LPPSimplexSolver:
    def __init__(self, problem: LPP):
        self.problem = problem

    def _solve_step(self, matrix: Matrix, basis: BasisVariables) -> list:
        # TODO: Finish refactoring
        return []

    def solve(self) -> list:
        constraints_matrix = constraints_to_matrix(problem.constraints)
        constraints_matrix_basis = get_matrix_basis(constraints_matrix)
        return self._solve_step(constraints_matrix, constraints_matrix_basis)


if __name__ == "__main__":
    problem = read_lpp()
    print_lpp(problem)

    problem_solver = LPPSimplexSolver(problem)
    solution = problem_solver.solve()
    print(solution)
