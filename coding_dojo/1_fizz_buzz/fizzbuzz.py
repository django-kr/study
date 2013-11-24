# -*- coding: utf-8 -*-
import unittest

def checkfizz(number):
    return cls.checknumber(number, fizz=True)


class FizzBuzzTest(unittest.TestCase):

    def test_fizz_print_when_3(self):
        self.assertTrue(checkfizz(3))

    def test_fizz_do_not_print_when_2(self):
        self.assertFalse(checkfizz(2))

    def test_fizz_when_divide_3(self):
        fizz_numbers = range(1, 100)
        fizz_numbers = filter(lambda x: x % 3 is 0, fizz_numbers)
        for fizz_number in fizz_numbers:
            self.assertTrue(checkfizz(fizz_number))

if __name__ == '__main__':
    unittest.main()
