import sys
from pathlib import Path
# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))
from game.wordle import WordleGame

class WordleCLI:
    def __init__(self):
        # 加载单词列表
        word_path = Path(__file__).parent.parent / "data" / "words.txt"
        with open(word_path, 'r') as f:
            self.word_list = [word.strip().lower() for word in f if word.strip()]
        self.game = WordleGame(self.word_list)
        self.colors = {
            'correct': '\033[42m',  # 绿色背景
            'present': '\033[43m',  # 黄色背景
            'absent': '\033[47m',   # 灰色背景
            'reset': '\033[0m'      # 重置颜色
        }

    def print_welcome(self):
        print("欢迎来到Wordle游戏!")
        print(f"猜一个{self.game.word_length}字母的单词，你有{self.game.max_attempts}次机会\n")

    def print_guess_result(self, result):
        """打印带颜色的猜测结果"""
        for letter, status in result:
            print(f"{self.colors[status]}{letter.upper()}{self.colors['reset']} ", end='')
        print()

    def run(self):
        self.print_welcome()

        while not self.game.is_game_over():
            print(f"第{len(self.game.guesses) + 1}/{self.game.max_attempts}次猜测:")
            guess = input("请输入你的猜测: ").strip()

            if not self.game.is_valid_guess(guess):
                print(f"请输入{self.game.word_length}个字母的单词!")
                continue

            result = self.game.process_guess(guess)
            self.print_guess_result(result)

        if self.game.is_won():
            print(f"恭喜你猜对了! 用了{len(self.game.guesses)}次")
        else:
            print(f"游戏结束，正确答案是: {self.game.target_word.upper()}")

if __name__ == "__main__":
    cli = WordleCLI()
    cli.run()