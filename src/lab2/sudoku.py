import multiprocessing
import threading
import time
import pathlib 
import typing as tp
import random
T = tp.TypeVar("T")

def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)

def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid

def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()

def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    result = []
    for i in range(0, len(values), n):
        result.append(values[i:i+n])
    return result

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [col[pos[1]] for col in grid]

def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [grid[(pos[0] // 3) * 3 + i][(pos[1] // 3) * 3 + j] for i in range(3) for j in range(3)]

def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    return [(row, col) for row in range(len(grid)) for col in range(len(grid[0])) if grid[row][col] == '.' ]

def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    return set('123456789') - (set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos))) - {'.'}

def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty_pos = find_empty_positions(grid)
    if not empty_pos:
        return grid  

    row, col = empty_pos[0]
    for value in find_possible_values(grid, (row, col)):
        grid[row][col] = value
        if solve(grid):
            return grid
        grid[row][col] = '.'  

    return None  

def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    for i in range(9):
        row = set(solution[i])
        col = set([row[i] for row in solution])
        if len(row) != 9 or len(col) != 9:
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = set()
        for x in range(i, i + 3):
            for y in range(j, j + 3):
                block.add(solution[x][y])
        if len(block) != 9:
            return False

    return True

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [['.' for x in range(9)] for y in range(9)]
    while not check_solution(grid):
        solve(grid)

    count = 0
    while count < 81 - min(N, 81):
        row, col = random.randint(0,8), random.randint(0,8)
        if grid[row][col] != ".":
            grid[row][col] = "."
            count += 1

    return grid
def run_solve(file):
    grid = read_sudoku(file)
    start = time.time()
    solve(grid)
    end = time.time()
    print(f'{file}: {end-start}')
if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        p = multiprocessing.Process(target=run_solve, args=(fname,))
        p.start()        
        '''
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
        '''