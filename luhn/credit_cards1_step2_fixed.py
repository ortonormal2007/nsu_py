#!/usr/bin/env python

# credit_cards1 (обязательная)
#
# Напишите программу для генерирования и проверки 
# валидности номеров кредитных карт трёх видов:
#   - MasterCard 16 цифр
#   - AmericanExpress 15 цифр
#   - Visa 13, 16 или 19 цифр

# Шаг 2. Реализуйте класс MasterCard, как описано ниже

import pytest
from random import randint, choice

def calc_luhn(n):
    odd = sum(int(x) for x in str(n)[-1::-2])
    even = sum(sum(int(y) for y in str(int(x) * 2)) for x in str(n)[-2::-2])
    return (odd + even) % 10


class MasterCard():
    def __init__(self, number):
        # Принимает на вход строку, избавляется от пробелов,
        # преобразует в число, сохраняет в поле класса
        self.number = 0
        if len(number) > 0:
            self.number = int(number.replace(' ', ''))


    def is_valid(self):
        #Is this a VISA???? 


        # Проверяет длину строки (должно быть 13, 16 или 19) и 
        # код Луна (должен быть 0)

        return len(str(self.number)) in (13, 16, 19) and calc_luhn(self.number) == 0

        # if calc_luhn(self.number) == 0 and len(str(self.number)) in (13, 16, 19):
        #     return True
        # else:
        #     return False


    @staticmethod
    def generate():
        # Случайным образом выбирается длина, затем случайным же 
        # образом генерируются цифры так, чтобы «сошёлся» код Луна.
        # Возвращается объект класса MasterCard с полученным номером.
        # Рекомендуется использовать choice и randint из random.
        # @staticmethod - это так называемый декоратор, он делает метод
        # статическим, такой метод можно вызывать на классе: MasterCard.generate(), 
        # а не только на объекте класса: MasterCard().generate().
        # Используется, например, для альтернативных конструкторов (как здесь).
        mrcrd_length = (16,)


        def num_gen():
            curr_length = choice(mrcrd_length)
            curr_length -= 1
            return 10 * randint(10 ** (curr_length - 1), (10 ** curr_length) - 1)


        number = num_gen()   
        difference = calc_luhn(number)
        if  difference == 0:
            return MasterCard(str(number))
        else:
            return MasterCard(str(number + (10 - calc_luhn(number))))



        

    def __str__(self):
        # Возвращает номер карты в виде строки
        return str(self.number)

def test_calc_luhn():
    assert calc_luhn(1) == 1
    assert calc_luhn(23) == 7
    assert calc_luhn(23678) == 7
    assert calc_luhn(23978) == 0

# str????

def test_str():  assert str(MasterCard('1234 5678').number) == '12345678'

def test0():  assert MasterCard('').is_valid() == False
def test1():  assert MasterCard('23978').is_valid() == False
def test2():  assert MasterCard('1234 5678 9012 3456').is_valid() == False
def test3():  assert MasterCard('5578 2350 9610 0287').is_valid() == True
def test4():  assert MasterCard('5578 2350 9610 2087').is_valid() == False

def test9():
    # Генерирует номер карты и проверяет его валидность
    for i in range(1000):
        card = MasterCard.generate()
        assert card.is_valid() == True

if __name__ == '__main__':
    # При таком способе вызова каждый assert вместо просто да/нет будет
    # выдавать более детальную информацию, если что-то пошло не так.
    pytest.main([__file__])
#    pytest.main(['__file__ + '::test3'])    # запускает только третий тест
#    pytest.main(['-s', __file__ + '::test3'])   # то же + возможность отладки ipdb

