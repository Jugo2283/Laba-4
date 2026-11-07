"""Консольный интерфейс аналитической станции временных рядов (вариант Б)."""
from well_series import analytics, config

def render_bar(val: float, min_v: float, max_v: float) -> str:
    """Строит текстовую полоску # пропорционально значению в диапазоне [min_v; max_v]."""
    span = max_v - min_v
    if span <= 0:
        return "#" * 10
    ratio = (val - min_v) / span
    count = 1 + int(round(ratio * (config.BAR_MAX_WIDTH - 1)))
    return "#" * count

def main() -> None:
    print("АНАЛИТИЧЕСКАЯ СТАНЦИЯ ОБРАБОТКИ ВРЕМЕННЫХ РЯДОВ (ВАРИАНТ Б)")
    print("=" * 72)
    raw = input("Введите ваш номер по журналу N: ").strip()
    student_n = int(raw) if raw.isdigit() and int(raw) > 0 else 5
    
    rates = analytics.build_series_12d(student_n)
    mean_v = analytics.calc_mean(rates)
    med_v = analytics.calc_median(rates)
    min_v, max_v, rng_v = analytics.calc_extremes_and_range(rates)
    
    sma3 = analytics.calc_sma_aligned(rates, config.SHORT_WINDOW)
    sma5 = analytics.calc_sma_aligned(rates, config.LONG_WINDOW)
    trend_str = analytics.detect_trend(sma3)
    
    print(f"\nХронологический ряд (12 сут.): {rates}")
    print("-" * 72)
    print(f"Среднее: {mean_v:.2f} | Медиана: {med_v:.2f} | Разница (Среднее - Медиана): {mean_v - med_v:+.2f}")
    print(f"Минимум: {min_v:.2f} | Максимум: {max_v:.2f} | Размах вариации R: {rng_v:.2f} м³/сут")
    print(f"Оценка тренда по SMA({config.SHORT_WINDOW}): {trend_str}")
    
    print("\nСВОДНАЯ ТАБЛИЦА СГЛАЖИВАНИЯ И ВИЗУАЛИЗАЦИИ РЯДА")
    print("-" * 72)
    print(f"{'День':<6}{'Q факт':>10}{'SMA(3)':>10}{'SMA(5)':>10}{'Откл. от SMA(3)':>16} {'Профиль дебита'}")
    print("-" * 72)
    for idx, q in enumerate(rates):
        day = idx + 1
        s3 = sma3[idx]
        s5 = sma5[idx]
        s3_str = f"{s3:10.2f}" if s3 is not None else f"{'—':>10}"
        s5_str = f"{s5:10.2f}" if s5 is not None else f"{'—':>10}"
        dev_str = f"{q - s3:+16.2f}" if s3 is not None else f"{'—':>16}"
        bar = render_bar(q, min_v, max_v)
        print(f"{day:<6}{q:>10.2f}{s3_str}{s5_str}{dev_str} {bar}")

    # =========================================================================
    # БЛОК ВЫПОЛНЕНИЯ ОБЯЗАТЕЛЬНЫХ УПРАЖНЕНИЙ ДЛЯ ВАРИАНТА Б (РАЗДЕЛ 8)
    # =========================================================================
    print("\n" + "="*20 + " ВЫПОЛНЕНИЕ ОБЯЗАТЕЛЬНЫХ УПРАЖНЕНИЙ " + "="*20)

    # --- Упражнение 1. Нечётная vs чётная длина ряда ---
    rates_odd = rates.copy()
    rates_odd.append(60.0)
    print(f"\n[Упражнение 1] Ряд нечётной длины (13 элементов): {rates_odd}")
    print(f"               Новая медиана: {analytics.calc_median(rates_odd):.2f} м³/сут")

    # --- Упражнение 2. Устойчивость медианы к выбросу ---
    rates_emrg = rates.copy()
    rates_emrg[-1] = 500.0
    print(f"\n[Упражнение 2] Ряд с аварийным выбросом 500.0 на 12-е сутки:")
    print(f"               До выброса  | Среднее: {mean_v:.2f} | Медиана: {med_v:.2f}")
    print(f"               После выброса | Среднее: {analytics.calc_mean(rates_emrg):.2f} | Медиана: {analytics.calc_median(rates_emrg):.2f}")

    # --- Упражнение 3. Влияние ширины окна сглаживания (k = 2 против k = 5) ---
    sma_2_clean = [x for x in analytics.calc_sma_aligned(rates, window=2) if x is not None]
    sma_5_clean = [x for x in analytics.calc_sma_aligned(rates, window=5) if x is not None]
    print(f"\n[Упражнение 3] Количество вычисленных точек в SMA(2): {len(sma_2_clean)} (По формуле 12-2+1 = {12-2+1})")
    print(f"               Количество вычисленных точек в SMA(5): {len(sma_5_clean)} (По формуле 12-5+1 = {12-5+1})")

    # --- Упражнение 4. Опасность сортировки «на месте» ---
    print(f"\n[Упражнение 4] Теоретический эксперимент: функция sorted() защищает хронологию от поломки методом .sort().")

    # --- Упражнение 5. Суммарная добыча и доля пиковых суток ---
    q_sum = sum(rates)
    peak_share = (max_v / q_sum) * 100
    print(f"\n[Упражнение 5] Суммарный объём добычи за 12 суток (Q_sum): {q_sum:.2f} м³")
    print(f"               Доля максимальных суток (8 день, {max_v:.2f} м³) от общей добычи: {peak_share:.2f}%")

    # --- Упражнение 6. Подсчёт числа суток выше среднего уровня ---
    above_mean_days = [day_idx + 1 for day_idx, val in enumerate(rates) if val > mean_v]
    print(f"\n[Упражнение 6] Суток строго выше среднего уровня ({mean_v:.2f} м³/сут): {len(above_mean_days)} шт.")
    print(f"               Номера этих суток: {above_mean_days}")

    # --- Упражнение 7. Защита от вырожденных случаев ---
    print(f"\n[Упражнение 7] Краевые сценарии функции calc_sma_aligned (без учета None):")
    print(f"               При k = 1 количество точек SMA: {len([x for x in analytics.calc_sma_aligned(rates, 1) if x is not None])}")
    print(f"               При k = len(rates) (окно 12) количество точек SMA: {len([x for x in analytics.calc_sma_aligned(rates, len(rates)) if x is not None])}")
    try:
        analytics.calc_sma_aligned(rates, 20)
    except ValueError as e:
        print(f"               При k = 20 успешно перехвачено исключение: {e}")
    print("=" * 76)

if __name__ == "__main__":
    main()