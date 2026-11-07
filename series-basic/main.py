"""Алгоритмическая обработка числового ряда дебитов скважины (вариант А)."""

WINDOW_SIZE = 3  # ширина окна скользящей средней (суток)

def generate_rate_series(student_n: int) -> list[float]:
    """Формирует индивидуальный ряд из 10 суточных замеров дебита по номеру N."""
    base = 40.0 + 2.0 * student_n
    step = float((student_n % 5) + 1)
    offsets = [0.0, 2.0, -1.0, 3.0, 0.0, 1.0, 4.0, 2.0, -2.0, 5.0]
    series: list[float] = []
    for k in offsets:
        series.append(round(base + k * step, 2))
    return series

def calc_mean(series: list[float]) -> float:
    """Вычисляет среднее арифметическое числового ряда."""
    if len(series) == 0:
        raise ValueError("Нельзя вычислить среднее для пустого списка")
    total = 0.0
    for val in series:
        total += val
    return total / len(series)

def calc_median(series: list[float]) -> float:
    """Вычисляет медиану ряда (работает для чётной и нечётной длины)."""
    n = len(series)
    if n == 0:
        raise ValueError("Нельзя вычислить медиану для пустого списка")
    ordered = sorted(series)  # создаём отсортированную копию, не ломая хронологию!
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    else:
        return (ordered[mid - 1] + ordered[mid]) / 2.0

def calc_range(series: list[float]) -> tuple[float, float, float]:
    """Возвращает кортеж (минимум, максимум, размах вариации) без встроенных min/max."""
    if len(series) == 0:
        raise ValueError("Пустой список")
    min_val = series[0]
    max_val = series[0]
    for val in series[1:]:
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val, max_val - min_val

def calc_moving_average(series: list[float], window: int) -> list[float]:
    """Вычисляет простую скользящую среднюю (SMA) с окном window."""
    if window <= 0 or window > len(series):
        raise ValueError(f"Некорректный размер окна: {window}")
    sma_values: list[float] = []
    for i in range(len(series) - window + 1):
        window_slice = series[i : i + window]
        avg = calc_mean(window_slice)
        sma_values.append(round(avg, 2))
    return sma_values


def main() -> None:
    print("АЛГОРИТМИЧЕСКАЯ ОБРАБОТКА РЯДА ДЕБИТОВ СКВАЖИНЫ")
    print("=" * 54)
    raw_n = input("Введите ваш номер по журналу N: ").strip()
    student_n = int(raw_n) if raw_n.isdigit() and int(raw_n) > 0 else 5
    
    rates = generate_rate_series(student_n)
    mean_val = calc_mean(rates)
    median_val = calc_median(rates)
    min_v, max_v, range_v = calc_range(rates)
    sma_list = calc_moving_average(rates, WINDOW_SIZE)
    
    print(f"\nИсходный ряд (10 суток): {rates}")
    print(f"Отсортированный ряд: {sorted(rates)}")
    print("\nСТАТИСТИЧЕСКИЕ ПОКАЗАТЕЛИ РЯДА")
    print("-" * 54)
    print(f"Среднее арифметическое: {mean_val:8.2f} м³/сут")
    print(f"Медиана ряда: {median_val:8.2f} м³/сут")
    print(f"Минимум / Максимум: {min_v:8.2f} / {max_v:.2f} м³/сут")
    print(f"Размах вариации R: {range_v:8.2f} м³/сут")
    
    print(f"\nТАБЛИЦА СГЛАЖИВАНИЯ (Скользящая средняя SMA, окно k = {WINDOW_SIZE})")
    print("-" * 54)
    print(f"{'Сутки':<8}{'Факт Q, м³/сут':>16}{'Окно среза':>16}{'SMA(3), м³/сут':>14}")
    print("-" * 54)
    for idx, q_val in enumerate(rates):
        day = idx + 1
        if day < WINDOW_SIZE:
            print(f"{day:<8}{q_val:>16.2f}{'—':>16}{'— (накопление)':>14}")
        else:
            sma_idx = idx - WINDOW_SIZE + 1
            win_str = f"[{day - 2}..{day}]"
            print(f"{day:<8}{q_val:>16.2f}{win_str:>16}{sma_list[sma_idx]:>14.2f}")

    # =========================================================================
    # БЛОК ВЫПОЛНЕНИЯ ОБЯЗАТЕЛЬНЫХ УПРАЖНЕНИЙ (РАЗДЕЛ 8)
    # =========================================================================
    print("\n" + "="*20 + " ВЫПОЛНЕНИЕ ОБЯЗАТЕЛЬНЫХ УПРАЖНЕНИЙ " + "="*20)

    # --- Упражнение 1. Нечётная vs чётная длина ряда (проверка медианы) ---
    rates_odd = rates.copy()
    rates_odd.append(60.0)  # временно добавляем 11-й элемент
    print(f"\n[Упражнение 1] Ряд нечётной длины (11 элементов): {rates_odd}")
    print(f"               Отсортированный: {sorted(rates_odd)}")
    print(f"               Новая медиана: {calc_median(rates_odd):.2f} м³/сут")

    # --- Упражнение 2. Устойчивость медианы к выбросу (Аварийный всплеск) ---
    rates_emrg = rates.copy()
    rates_emrg[-1] = 500.0  # симулируем сбой датчика на 10-е сутки
    print(f"\n[Упражнение 2] Ряд с аварийным выбросом 500.0 на 10-е сутки:")
    print(f"               До выброса  | Среднее: {mean_val:.2f} | Медиана: {median_val:.2f} | Размах: {range_v:.2f}")
    print(f"               После выброса | Среднее: {calc_mean(rates_emrg):.2f} | Медиана: {calc_median(rates_emrg):.2f} | Размах: {calc_range(rates_emrg)[2]:.2f}")

    # --- Упражнение 3. Влияние ширины окна сглаживания (k = 2 против k = 5) ---
    sma_2 = calc_moving_average(rates, window=2)
    sma_5 = calc_moving_average(rates, window=5)
    print(f"\n[Упражнение 3] Длина списка SMA(2): {len(sma_2)} (Формула n-k+1: 10-2+1 = {10-2+1})")
    print(f"               Длина списка SMA(5): {len(sma_5)} (Формула n-k+1: 10-5+1 = {10-5+1})")

    # --- Упражнение 4. Опасность сортировки «на месте» (.sort() вместо sorted()) ---
    print(f"\n[Упражнение 4] Демонстрация теории: метод .sort() меняет список навсегда по ссылке.")
    print("               В коде используется функция sorted(), сохраняющая исходный хронологический порядок дней.")

    # --- Упражнение 5. Суммарная добыча и доля пиковых суток ---
    q_sum = sum(rates)
    peak_share = (max_v / q_sum) * 100
    print(f"\n[Упражнение 5] Суммарный объём добычи за 10 суток (Q_sum): {q_sum:.2f} м³")
    print(f"               Доля максимальных суток ({max_v:.2f} м³) от общей добычи: {peak_share:.2f}%")

    # --- Упражнение 6. Подсчёт числа суток выше среднего уровня (Фильтрация ряда) ---
    above_mean_days = [day_idx + 1 for day_idx, val in enumerate(rates) if val > mean_val]
    print(f"\n[Упражнение 6] Суток строго выше среднего уровня ({mean_val:.2f} м³/сут): {len(above_mean_days)} шт.")
    print(f"               Номера этих суток: {above_mean_days}")

    # --- Упражнение 7. Защита от вырожденных случаев (Краевые сценарии) ---
    print(f"\n[Упражнение 7] Проверка краевых сценариев для функции calc_moving_average:")
    print(f"               При k = 1 длина SMA: {len(calc_moving_average(rates, 1))} элементов")
    print(f"               При k = len(rates) (окно 10) длина SMA: {len(calc_moving_average(rates, len(rates)))} элемент")
    try:
        calc_moving_average(rates, 20)  # Окно больше длины списка (ошибка)
    except ValueError as e:
        print(f"               При k = 20 успешно перехвачено исключение: {e}")
    print("=" * 76)

if __name__ == "__main__":
    main()