import time
import os
from multiprocessing import Pool


def element(i, j, A, B):
    """Вычисляет элемент C[i][j] — скалярное произведение строки i матрицы A
    и столбца j матрицы B."""
    N = len(A[0])
    res = 0
    for k in range(N):
        res += A[i][k] * B[k][j]
    return (i, j, res)


# ──────────────────────────────────────────────
# Генерация матриц побольше для наглядности
# ──────────────────────────────────────────────
SIZE = 50

matrix_a = [[(i + j) % 10 for j in range(SIZE)] for i in range(SIZE)]
matrix_b = [[(i * j) % 10 for j in range(SIZE)] for i in range(SIZE)]


def sequential_multiply(A, B):
    """Последовательное перемножение."""
    rows = len(A)
    cols = len(B[0])
    result = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            _, _, val = element(i, j, A, B)
            result[i][j] = val
    return result


def pool_multiply(A, B, num_processes):
    """Параллельное перемножение через Pool."""
    rows = len(A)
    cols = len(B[0])
    result = [[0] * cols for _ in range(rows)]

    # TODO 3: Создайте пул процессов и используйте pool.starmap()
    args = [(i, j, A, B) for i in range(rows) for j in range(cols)]
    
    with Pool(processes=num_processes) as pool:
        results_list = pool.starmap(element, args)
    
    for (i, j, val) in results_list:
        result[i][j] = val

    return result


if __name__ == '__main__':
    cpu_count = os.cpu_count()
    print(f"Размер матриц: {SIZE}x{SIZE}")
    print(f"Доступно ядер CPU: {cpu_count}\n")

    # Последовательное вычисление
    t = time.time()
    seq_result = sequential_multiply(matrix_a, matrix_b)
    time_seq = time.time() - t
    print(f"Последовательно: {time_seq:.4f} сек")

    # TODO 4: Сравнение времени при разном числе процессов
    for n in [1, 2, 4]:
        t = time.time()
        par_result = pool_multiply(matrix_a, matrix_b, n)
        elapsed = time.time() - t
        print(f"Pool ({n} процессов): {elapsed:.4f} сек")
        
        # Проверка корректности результата
        assert par_result == seq_result, f"Результаты не совпадают при {n} процессах!"
        print("✓ Результаты совпадают\n")

