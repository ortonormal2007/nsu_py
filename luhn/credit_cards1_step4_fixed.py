#!/usr/bin/env python

# credit_cards1 (обязательная)
#
# Напишите программу для генерирования и проверки
# валидности номеров кредитных карт трёх видов:
#   - MasterCard 16 цифр
#   - AmericanExpress 15 цифр
#   - Visa 13, 16 или 19 цифр

# Шаг 4. Реализуйте класс Visa, как описано ниже

import pytest
from random import randint, choice


def calc_luhn(n):
    odd = sum(int(x) for x in str(n)[-1::-2])
    even = sum(sum(int(y) for y in str(int(x) * 2)) for x in str(n)[-2::-2])
    return (odd + even) % 10


class CreditCard:
    crd_length = 0
    def __init__(self,number):
        if len(number) > 0:
            self.number = int(number.replace(' ', ''))
        else:
            self.number = 0


    def is_valid(self):
        def is_len():
            if isinstance(self.crd_length, (tuple, list)):
                return len(str(self.number)) in self.crd_length
            elif isinstance(self.crd_length, int):
                return len(str(self.number)) == self.crd_length

        return is_len() and calc_luhn(self.number) == 0 
        # if calc_luhn(self.number) == 0 and is_len():
        #     return True
        # else:
        #     return False


    @classmethod
    def generate(cls): 
        def num_gen():
            if isinstance(cls.crd_length, (list, tuple)):
                curr_length = choice(cls.crd_length)
            elif isinstance(cls.crd_length, int):
                curr_length = cls.crd_length
            curr_length -= 1
            return 10 * randint(10 ** (curr_length - 1), (10 ** curr_length) - 1)


        number = num_gen()
        difference = calc_luhn(number)
        if  difference == 0:
            return cls(str(number))
        else:
            return cls(str(number + (10 - calc_luhn(number))))


class MasterCard(CreditCard):
    crd_length = 16


class AmericanExpress(CreditCard):
    crd_length = 15


class Visa(CreditCard):
    # Теперь длина номера карты может принимать несколько значений.
    # Подумайте, как лучше всего адаптировать программу к такому
    # повороту событий с минимальными изменениями в существующем коде.
    crd_length = (13, 16, 19)

def test_calc_luhn():
    assert calc_luhn(1) == 1
    assert calc_luhn(23) == 7
    assert calc_luhn(23678) == 7
    assert calc_luhn(23978) == 0

def test_str():  assert str(MasterCard('1234 5678').number) == '12345678'

def test0():  assert MasterCard('').is_valid() == False
def test1():  assert MasterCard('23978').is_valid() == False
def test2():  assert MasterCard('1234 5678 9012 3456').is_valid() == False
def test3():  assert MasterCard('5578 2350 9610 0287').is_valid() == True
def test4():  assert MasterCard('5578 2350 9610 2087').is_valid() == False
def test5():  assert AmericanExpress('3473 170111 86210').is_valid() == True
def test6():  assert AmericanExpress('3473 170011 86210').is_valid() == False
def test7():  assert AmericanExpress('5578 2350 9610 0287').is_valid() == False
def test8():  assert Visa('4929 5958 3592 5180').is_valid() == True

def test9():
    # Генерирует номер карты и проверяет его валидность
    for i in range(1000):
        card = Visa.generate()
        assert card.is_valid() == True
        assert AmericanExpress(str(card.number)).is_valid() == False
        assert MasterCard(str(card.number)).is_valid() == (len(str(card.number)) == 16)

if __name__ == '__main__':
    # При таком способе вызова каждый assert вместо просто да/нет будет
    # выдавать более детальную информацию, если что-то пошло не так.
    pytest.main([__file__])
#    pytest.main(['__file__ + '::test3'])    # запускает только третий тест
#    pytest.main(['-s', __file__ + '::test3'])   # то же + возможность отладки ipdb
