import re


def count_words(f_name):
	# открытие файла с текстом,
	# создание словаря (key=слово, value=количество)
	with open(f_name, 'r', encoding='utf8') as book:
		w_count = {}
		pattern = r"(\b[\w'-]{4,}\b)"
		for line in book:
			wds = re.findall(pattern, line)
			wds = [wd.lower() for wd in wds]
			for wd in wds:
				w_count[wd] = w_count.get(wd, 0) + 1
	return w_count


def word_freq(filename):
	# вывод отсортированного в лексикографическом порядке
	# списка
	for word, count in sorted(count_words(filename).items()):
		print(word, count, sep=' ')


def print_top(filename):
	# вывод двадцати наиболее часто встречающихся слов
	print(*(d for d, c in sorted(count_words(filename).items(), key=lambda p: (-p[1], p[0]))[0:20]), sep='\n')


# полный путь до файла
book_name = 'C:/Users/Future visioN/Desktop/words/revizor.txt'
print('word_freq:')
word_freq(book_name)
print('_______', 'print_top:', sep='\n')
print_top(book_name)