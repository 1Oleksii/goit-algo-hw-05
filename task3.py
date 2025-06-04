import gdown
import timeit

# Завантаження файлів з Google Drive за ID
url1 = 'https://drive.google.com/uc?id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh'
url2 = 'https://drive.google.com/uc?id=18BfXyQcmuinEI_8KDSnQm4bLx6yIFS_w'

# Коментар: Завантажуємо і зберігаємо як локальні файли
gdown.download(url1, 'article1.txt', quiet=False)
gdown.download(url2, 'article2.txt', quiet=False)

# Читаємо текст із файлів
with open("article1.txt", "r", encoding="latin1") as f:
    text1 = f.read()
with open("article2.txt", "r", encoding="latin1") as f:
    text2 = f.read()

# Коментар: Підрядки для пошуку
existing_substring = "the"  # Існуючий підрядок
nonexistent_substring = "qwerty12345"  # Вигаданий підрядок

# Алгоритм Кнута-Морріса-Пратта ---
def kmp_search(text, pattern):
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Алгоритм Рабіна-Карпа ---
def rabin_karp(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    h = pow(d, m-1) % q
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for s in range(n - m + 1):
        if p == t:
            if text[s:s + m] == pattern:
                return s
        if s < n - m:
            t = (t - h * ord(text[s])) % q
            t = (t * d + ord(text[s + m])) % q
            t = (t + q) % q
    return -1

# Алгоритм Боєра-Мура ---
def boyer_moore(text, pattern):
    def bad_char_heuristic(pattern):
        bad_char = [-1] * 256
        for i in range(len(pattern)):
            bad_char[ord(pattern[i])] = i
        return bad_char

    m = len(pattern)
    n = len(text)
    bad_char = bad_char_heuristic(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    return -1

# Функція для заміру часу ---
def measure_time(search_func, text, pattern):
    return timeit.timeit(lambda: search_func(text, pattern), number=1)

algorithms = {
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp,
    "Boyer-Moore": boyer_moore
}

# Збережемо результати для аналізу
results = {
    "article1": {},
    "article2": {},
}

for name, func in algorithms.items():
    # Вимірювання часу для article 1
    time1_exist = measure_time(func, text1, existing_substring)
    time1_fake = measure_time(func, text1, nonexistent_substring)

    # Вимірювання часу для article 2
    time2_exist = measure_time(func, text2, existing_substring)
    time2_fake = measure_time(func, text2, nonexistent_substring)

    print(f"\n=== {name} ===")
    print(f"Article 1 — існуючий: {time1_exist:.6f} сек")
    print(f"Article 1 — вигаданий: {time1_fake:.6f} сек")
    print(f"Article 2 — існуючий: {time2_exist:.6f} сек")
    print(f"Article 2 — вигаданий: {time2_fake:.6f} сек")

    # Зберігаємо середній час для кожного тексту
    results["article1"][name] = (time1_exist + time1_fake) / 2
    results["article2"][name] = (time2_exist + time2_fake) / 2

# Функція для визначення найшвидшого алгоритму
def find_fastest(results_dict):
    return min(results_dict, key=results_dict.get), results_dict[min(results_dict, key=results_dict.get)]

# Визначаємо найшвидші для кожного тексту
fastest_article1, time_article1 = find_fastest(results["article1"])
fastest_article2, time_article2 = find_fastest(results["article2"])

# Визначаємо найшвидший загальний (за сумою часу обох текстів)
total_times = {name: results["article1"][name] + results["article2"][name] for name in algorithms.keys()}
fastest_total, time_total = find_fastest(total_times)

print("\n--- Результати ---")
print(f"Найшвидший алгоритм для Article 1: {fastest_article1} ({time_article1:.6f} сек)")
print(f"Найшвидший алгоритм для Article 2: {fastest_article2} ({time_article2:.6f} сек)")
print(f"Найшвидший алгоритм загалом: {fastest_total} ({time_total:.6f} сек)")
