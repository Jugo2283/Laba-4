"""Математическое ядро: статистики ряда, скользящая средняя и оценка тренда."""
from well_series import config

def build_series_12d(student_n: int) -> list[float]:
    """Генерирует 12-суточный ряд дебитов для студента с номером N."""
    base = 55.0 + 2.5 * student_n
    step = float(student_n % 4) + 1.5
    return [round(base + k * step, 2) for k in config.OFFSETS_12D]

def calc_mean(series: list[float]) -> float:
    """Среднее арифметическое числового ряда."""
    if not series:
        raise ValueError("Пустой числовой ряд")
    total = 0.0
    for x in series:
        total += x
    return total / len(series)

def calc_median(series: list[float]) -> float:
    """Медиана числового ряда (без изменения исходного списка)."""
    n = len(series)
    if n == 0:
        raise ValueError("Пустой числовой ряд")
    ordered = sorted(series)
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0

def calc_extremes_and_range(series: list[float]) -> tuple[float, float, float]:
    """Возвращает (min_val, max_val, range_val) за один проход цикла."""
    if not series:
        raise ValueError("Пустой числовой ряд")
    lo = hi = series[0]
    for x in series[1:]:
        if x < lo:
            lo = x
        if x > hi:
            hi = x
    return lo, hi, round(hi - lo, 2)

def calc_sma_aligned(series: list[float], window: int) -> list[float | None]:
    """Возвращает список длины len(series), где первые (window - 1) элементов равны None,
    а остальные содержат скользящую среднюю SMA(window)."""
    if window <= 0 or window > len(series):
        raise ValueError(f"Окно {window} недопустимо для ряда длины {len(series)}")
    result: list[float | None] = [None] * (window - 1)
    for i in range(len(series) - window + 1):
        chunk = series[i : i + window]
        result.append(round(calc_mean(chunk), 2))
    return result

def detect_trend(sma_aligned: list[float | None]) -> str:
    """Определяет общий тренд по первой и последней доступной точке скользящей средней."""
    valid = [x for x in sma_aligned if x is not None]
    if len(valid) < 2:
        return "недостаточно данных"
    diff = valid[-1] - valid[0]
    if diff > 1.0:
        return f"восходящий (+{diff:.2f} м³/сут)"
    elif diff < -1.0:
        return f"нисходящий ({diff:.2f} м³/сут)"
    return f"стабильный ({diff:+.2f} м³/сут)"