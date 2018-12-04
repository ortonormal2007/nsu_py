#!/usr/bin/env python

# credit_cards1 (обязательная)
#
# Напишите программу для генерирования и проверки 
# валидности номеров кредитных карт трёх видов:
#   - MasterCard 16 цифр
#   - AmericanExpress 15 цифр
#   - Visa 13, 16 или 19 цифр

# Шаг 3. Реализуйте класс AmericanExpress, как описано ниже

import pytest
from random import randint, choice


def calc_luhn(n):
    odd = sum(int(x) for x in str(n)[-1::-2])
    even = sum(sum(int(y) for y in str(int(x) * 2)) for x in str(n)[-2::-2])
    return (odd + even) % 10


class CreditCard:
    crd_length = 0
    def __init__(self,number):
    # Выделите общую функциональность для классов MasterCard и AmericanExpress
    # в базовый класс CreditCard, оставив особенности в полях или методах 
    # дочерних классов. Сделайте это так, чтобы родительский класс не знал
    # об особенностях реализации дочерних классов (например, длина
    # номера карты MasterCard должна храниться в классе MasterCard).
        # print(repr(number), len(number), type(number))
        if len(number) > 0:
            self.number = int(number.replace(' ', ''))
        else:
            self.number = 0


    def is_valid(self):
        return len(str(self.number)) == self.crd_length and calc_luhn(self.number) == 0
        # if calc_luhn(self.number) == 0 and len(str(self.number)) == self.__class__.crd_length:
        #     return True
        # else:
        #     return False


    def __str__(self):
        return str(self.number)


    @classmethod
    def generate(cls):
        # @classmethod - это декоратор, который который превращает метод
        # в нечто среднее между обычным и статическим методом.
        # В отличие от статического, classmethod имеет доступ 
        # к полям дочернего класса (но не объекта), а также к статическим и 
        # классовым его методам (но не обычным методам).
        def num_gen():
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


def test_calc_luhn():
    assert calc_luhn(1) == 1
    assert calc_luhn(23) == 7
    assert calc_luhn(23678) == 7
    assert calc_luhn(23978) == 0


# VISA??????
# def test_str():  assert Visa('1234 5678').number == '12345678'

def test_str():  assert str(CreditCard('1234 5678').number) == '12345678'

def test0():  assert MasterCard('').is_valid() == False
def test1():  assert MasterCard('23978').is_valid() == False
def test2():  assert MasterCard('1234 5678 9012 3456').is_valid() == False
def test3():  assert MasterCard('5578 2350 9610 0287').is_valid() == True
def test4():  assert MasterCard('5578 2350 9610 2087').is_valid() == False
def test5():  assert AmericanExpress('3473 170111 86210').is_valid() == True
def test6():  assert AmericanExpress('3473 170011 86210').is_valid() == False
def test7():  assert AmericanExpress('5578 2350 9610 0287').is_valid() == False

def test9():
    # Генерирует номер карты и проверяет его валидность
    for i in range(1000):
        card = MasterCard.generate()
        print(type(card.number))
        assert card.is_valid() == True
        assert AmericanExpress(str(card.number)).is_valid() == False

if __name__ == '__main__':
    # При таком способе вызова каждый assert вместо просто да/нет будет
    # выдавать более детальную информацию, если что-то пошло не так.
    pytest.main([__file__])
#    pytest.main(['__file__ + '::test3'])    # запускает только третий тест
#    pytest.main(['-s', __file__ + '::test3'])   # то же + возможность отладки ipdb


