import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from game.wordle import WordleGame

class TestWordleGame(unittest.TestCase):
    def test_is_valid_guess(self):
        game = WordleGame(word_list=["apple"])
        self.assertTrue(game.is_valid_guess("apple"))
        self.assertFalse(game.is_valid_guess("app"))  # 长度不足
        self.assertFalse(game.is_valid_guess("apples"))  # 长度过长
        self.assertFalse(game.is_valid_guess("app1e"))  # 包含数字

    def test_process_guess_correct(self):
        game = WordleGame(word_list=["apple"])
        game.target_word = "apple"
        result = game.process_guess("apple")
        self.assertTrue(all(status == "correct" for _, status in result))

    def test_process_guess_present(self):
        game = WordleGame(word_list=["apple"])
        game.target_word = "apple"
        result = game.process_guess("pleap")
        # 所有字母都存在但位置错误
        assert all(status in ["present", "correct"] for _, status in result)
        assert sum(1 for _, status in result if status == "correct") == 0

    def test_process_guess_absent(self):
        game = WordleGame(word_list=["apple"])
        game.target_word = "apple"
        result = game.process_guess("xyzzy")
        assert all(status == "absent" for _, status in result)

    def test_game_over_conditions(self):
        game = WordleGame(word_list=["apple"], max_attempts=2)
        game.target_word = "apple"
        game.process_guess("abcde")
        assert game.is_game_over() is False
        game.process_guess("fghij")
        assert game.is_game_over() is True  # 达到最大尝试次数

        game = WordleGame(word_list=["apple"])
        game.process_guess(game.target_word)
        assert game.is_game_over() is True  # 猜对单词

    def test_is_won(self):
        game = WordleGame(word_list=["apple"])
        game.target_word = "apple"
        game.process_guess("abcde")
        assert game.is_won() is False
        game.process_guess("apple")
        assert game.is_won() is True

    def test_letter_status_updates(self):
        self.game = WordleGame(word_list=["apple", "ample"], target_word="apple")
        self.game.process_guess("ample")
        self.assertEqual(self.game.letter_status['A'], 'correct')
        self.assertEqual(self.game.letter_status['M'], 'absent')
        self.assertEqual(self.game.letter_status['P'], 'correct')
        self.assertEqual(self.game.letter_status['L'], 'correct')
        self.assertEqual(self.game.letter_status['E'], 'correct')

    def test_multiple_guesses_status_priority(self):
        self.word_list = ["apple", "ample", "crane"]
        self.target_word = "apple"
        self.game = WordleGame(self.word_list, target_word=self.target_word)
        self.game.process_guess("crane")  # A: present, E: present
        self.game.process_guess("ample")   # A: correct, P: present, L: correct, E: correct
        self.assertEqual(self.game.letter_status['A'], 'correct')  # correct优先于present
        self.assertEqual(self.game.letter_status['E'], 'correct')  # correct优先于present
        self.assertEqual(self.game.letter_status['C'], 'absent')   # 保持absent
        game = WordleGame(word_list=["apple", "ample"])
        self.game.process_guess("ample")   # A: correct, P: present, L: correct, E: correct
        self.assertEqual(self.game.letter_status['A'], 'correct')  # correct优先于present
        self.assertEqual(self.game.letter_status['E'], 'correct')  # correct优先于present
        self.assertEqual(self.game.letter_status['C'], 'absent')   # 保持absent