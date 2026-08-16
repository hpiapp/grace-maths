import random
import unittest

from quiz_logic import Question, build_question_bank, check_answer, make_quiz, parse_numbers, primes_between


class QuizLogicTests(unittest.TestCase):
    def test_primes_between_is_inclusive(self):
        self.assertEqual(primes_between(50, 60), (53, 59))
        self.assertEqual(primes_between(1, 10), (2, 3, 5, 7))

    def test_prime_input_formats(self):
        question = Question("prime", "", (53, 59), "")
        for answer in ("53, 59", "59 53", "53 and 59", "53;59"):
            self.assertTrue(check_answer(question, answer))

    def test_wrong_or_invalid_answers(self):
        question = Question("prime", "", (53, 59), "")
        self.assertFalse(check_answer(question, "53"))
        self.assertFalse(check_answer(question, "53 and banana"))
        self.assertIsNone(parse_numbers(""))

    def test_cube_answers(self):
        question = Question("cube", "", (1728,), "")
        self.assertTrue(check_answer(question, "1728"))
        self.assertFalse(check_answer(question, "12"))

    def test_question_banks(self):
        self.assertEqual(len(build_question_bank("Prime numbers")), 10)
        self.assertEqual(len(build_question_bank("Cube numbers")), 12)
        self.assertEqual(len(build_question_bank("Mixed")), 22)

    def test_quiz_length_and_no_immediate_repeat(self):
        quiz = make_quiz("Cube numbers", 20, random.Random(7))
        self.assertEqual(len(quiz), 20)
        self.assertTrue(all(left != right for left, right in zip(quiz, quiz[1:])))


if __name__ == "__main__":
    unittest.main()
