import matplotlib.pyplot as plt


# Функция для настройки параметров графика со значениями временного ряда
def graph_settings_values():
    plt.ion()
    plt.figure(0, figsize=(10, 5))
    ax = plt.subplot()
    ax.grid()
    ax.set_xlabel('Время (сек)')
    ax.set_ylabel('Значения')
    return ax


# Функция для настройки параметров графика с кумулятивными суммами
def graph_settings_s():
    plt.figure(1, figsize=(10, 5))
    ax = plt.subplot()
    ax.grid()
    ax.set_xlabel('Время (сек)')
    ax.set_ylabel('Кумулятивные суммы')
    return ax


# Функция расчета кумулятивных сумм
def cumulative_sum(k, n, m, values):
    signs = []
    z = []
    s = []
    sigma = m / n
    for i in range(k, len(values) - 1):
        if (values[i] - values[i - k]) > 0:
            signs.append(1)
        else:
            signs.append(-1)
        z.append((signs[i - k] - sigma) * n)

    for i in range(0, k):
        s.append(m + n)

    for i in range(k, len(values) - 1):
        s.append(max(s[i - 1] + z[i - k], n + m))

    return s


# Функция расчета кумулятивных сумм при изменении дисперсии
def modified_cumulative_sum(k, sigma, n, m, values):
    signs = []
    z = []
    s = []
    subtraction = []
    square = []

    for i in range(0, len(values) - 1):
        subtraction.append(values[i + 1] - values[i])

    for i in range(0, len(subtraction)):
        square.append(subtraction[i] * subtraction[i])

    for i in range(k, len(square)):
        if (square[i] - square[i - k]) > 0:
            signs.append(-1)
        else:
            signs.append(1)
        z.append((signs[i - k] - sigma) * n)

    for i in range(0, k):
        s.append(m + n)

    for i in range(k, len(values) - 1):
        s.append(max(s[i - 1] + z[i - k], n + m))

    return s


# Функция поиска точек правых границ сегментов разладки
def find_disorders(s, h):
    disorders = []
    last_indexes = []
    max_sum_of_segment = []
    segments_lines = []

    for i in range(1, len(s) - 1):
        if s[i] > h:
            disorders.append(i)

    for i in range(0, len(disorders) - 1):
        if disorders[i + 1] - disorders[i] > 20:
            last_indexes.append(i)
    last_indexes.append(len(disorders))

    step = 0

    for i in range(0, len(last_indexes)):
        max = 0
        index = 0
        for j in range(step, last_indexes[i]):
            if s[disorders[j]] > max:
                max = s[disorders[j]]
                index = disorders[j]
        segments_lines.append(index)
        max_sum_of_segment.append(index)
        step = last_indexes[i]
    return max_sum_of_segment


# Функция поиска точек левых границ сегментов разладки
def find_begin_of_disorder(s, disorder_end, l):
    a: int = disorder_end
    while s[a] != l:
        a = a - 1
    return a


# Сегментация на основе левых и правых границ
def segmentation(disorders, values, k, s, l):
    segments = []
    segments_lines = []
    step = 0
    for i in range(step, len(disorders)):
        a: int = find_begin_of_disorder(s, disorders[i], l)
        b: int = disorders[i]
        segments.append(values[i:a])
        segments.append(values[a:b])
        step = disorders[i]

    segments_lines.append(0)

    for i in range(len(disorders)):
        # segments_lines.append(disorders[i] - k)
        segments_lines.append(find_begin_of_disorder(s, disorders[i], l))
        segments_lines.append(disorders[i])

    segments_lines.append(len(values))

    return segments, segments_lines


# Визуализация сегментов на графике временного ряда
def graph_settings_segments(ax_values, segments_lines, min, max):
    for i in range(len(segments_lines)):
        ax_values.vlines(segments_lines[i], min, max)
