import timeit
from functools import partial


# Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
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


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def read_file(file_url: str) -> str:
    with open(file_url, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


text_1 = read_file(r"E:\git\goit-algo-hw-05\article_1.txt")
text_2 = read_file(r"E:\git\goit-algo-hw-05\article_2.txt")


pattern_1 = "який здається найкращим у даний момент - тобто виробляється локально оптимальний вибір у надії, що він приведе"
pattern_2 = "видно з таблиці та рисунку найкращі результати по часу формування рекомендацій показали наступні структури даних"
pattern_false = "вигаданий підрядок для оцінки роботи алгоритмів пошуку підрядка"


kmp_search_text_1 = partial(kmp_search, text_1, pattern_1)
boyer_moore_search_text_1 = partial(boyer_moore_search, text_1, pattern_1)
rabin_karp_search_text_1 = partial(rabin_karp_search, text_1, pattern_1)


kmp_search_text_1_false = partial(kmp_search, text_1, pattern_false)
boyer_moore_search_text_1_false = partial(boyer_moore_search, text_1, pattern_false)
rabin_karp_search_text_1_false = partial(rabin_karp_search, text_1, pattern_false)


kmp_search_text_2 = partial(kmp_search, text_2, pattern_2)
boyer_moore_search_text_2 = partial(boyer_moore_search, text_2, pattern_2)
rabin_karp_search_text_2 = partial(rabin_karp_search, text_2, pattern_2)


kmp_search_text_2_false = partial(kmp_search, text_2, pattern_false)
boyer_moore_search_text_2_false = partial(boyer_moore_search, text_2, pattern_false)
rabin_karp_search_text_2_false = partial(rabin_karp_search, text_2, pattern_false)


call_stack = {
    "text 1 with true pattern": {
        "KMP search": kmp_search_text_1,
        "Boyer Moore Search": boyer_moore_search_text_1,
        "Rabin Karp Search": rabin_karp_search_text_1
    },
    "text 1 with false pattern": {
        "KMP search": kmp_search_text_1_false,
        "Boyer Moore Search": boyer_moore_search_text_1_false,
        "Rabin Karp Search": rabin_karp_search_text_1_false
    },
    "text 2 with true pattern": {
        "KMP search": kmp_search_text_2,
        "Boyer Moore Search": boyer_moore_search_text_2,
        "Rabin Karp Search": rabin_karp_search_text_2
    },
    "text 2 with false pattern": {
        "KMP search": kmp_search_text_2_false,
        "Boyer Moore Search": boyer_moore_search_text_2_false,
        "Rabin Karp Search": rabin_karp_search_text_2_false
    },
}

for text, stack in call_stack.items():
    print("Execution time for", text)
    for algo, func in stack.items():
        print(f"{algo}: {timeit.timeit(func, number=1)}")
