import re
from collections import defaultdict as dd

# def count_words(f_name):
# 	# открытие файла с текстом,
# 	# создание словаря (key=слово, value=количество)
# 	with open(f_name, 'r', encoding='utf8') as book:
# 		w_count = {}
# 		pattern = r"(\b[\w'-]{4,}\b)"
# 		for line in book:
# 			wds = re.findall(pattern, line)
# 			wds = [wd.lower() for wd in wds]
# 			for wd in wds:
# 				w_count[wd] = w_count.get(wd, 0) + 1
# 	return w_count


# def word_freq(filename):
# 	# вывод отсортированного в лексикографическом порядке
# 	# списка
# 	for word, count in sorted(count_words(filename).items()):
# 		print(word, count, sep=' ')


# def print_top(filename):
# 	# вывод двадцати наиболее часто встречающихся слов
# 	print(*(d for d, c in sorted(count_words(filename).items(), key=lambda p: (-p[1], p[0]))[0:20]), sep='\n')


def name_patronymic(f_name):
    pattern = r"[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+вич(?:(?:ей)|(?:(?:ем)|[уаеи]?))"
    w_count = dd(int)
    with open(f_name, 'r', encoding='utf8') as book:
        for line in book:
            wds = re.findall(pattern, line)
            # print(wds)
            for wd in wds:
                w_count[wd] += 1
    for word, count in sorted(w_count.items(), key=lambda x: (-x[1], x[0])):
        print(word, sep=' ')
    print(w_count)

# полный путь до файла
book_name = 'C:/Users/Future visioN/Desktop/nsu_py/words/revizor.txt'
print('word_freq:')
name_patronymic(book_name)
# print('_______', 'print_top:', sep='\n')
# print_top(book_name)