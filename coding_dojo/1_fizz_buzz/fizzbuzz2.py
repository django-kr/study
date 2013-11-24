# -*- coding: utf-8 -*-
import unittest

def is_fizz(number):
    if number == 0:
        return False
    if number%3 == 0:
        return True
    else:
        return False

def is_buzz(number):
    if number == 0:
        return False
    if number%5 == 0:
        return True
    else:
        return False

def trans_fizz_buzz(number):
    if is_fizz(number):
        return 'fizz'
    if is_buzz(number):
        return 'buzz'
    return number

class FizzBuzzTest(unittest.TestCase):
    def setUp(self):
        print "setUp"

    def tearDown(self):
        print "tearDown"

    def test_fizz_return_true_when_input_is_3(self):
        self.assertTrue(is_fizz(3))

    def test_fizz_return_false_when_input_is_4(self):
        self.assertFalse(is_fizz(4))

    def test_fizz_return_true_when_input_is_6(self):
        self.assertTrue(is_fizz(6))

    def test_fizz_return_false_when_input_is_0(self):
        self.assertFalse(is_fizz(0))

    def test_fizz_return_true_when_input_can_be_devided_by_3(self):
        fizz_numbers = range(1, 100)
        fizz_numbers = filter(lambda x: x%3 == 0, fizz_numbers)
        for number in fizz_numbers:
            self.assertTrue(is_fizz(number))

    def test_buzz_return_true_when_input_can_be_devided_by_5(self):
        buzz_numbers = range(1, 100)
        buzz_numbers = filter(lambda x: x%5 == 0, buzz_numbers)
        for number in buzz_numbers:
            self.assertTrue(is_buzz(number))

    def test_print_fizz_buzz_in_1_to_100_range_loop(self):
        fizz_buzz_expect_result = [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz']
        fizz_buzz_input_number = [1,2,3,4,5,6,7,8,9,10]

        for index in range(10):
            result = trans_fizz_buzz(fizz_buzz_input_number[index])
            self.assertEqual(result, fizz_buzz_expect_result[index])

    def blah_test_blah(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()