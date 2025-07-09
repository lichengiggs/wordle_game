import random
from pathlib import Path

class WordleGame:
    def __init__(self, word_list, target_word=None, max_attempts=6):
        self.word_list = word_list
        self.word_length = 5  # 设置单词长度为5
        self.max_attempts = max_attempts
        self.guesses = []
        self.letter_status = {}
        if target_word is None:
            self.target_word = self._select_target_word()
        else:
            self.target_word = target_word

    @classmethod
    def from_dict(cls, data, word_list):
        game = cls(
            word_list=word_list,
            target_word=data['target_word'],
            max_attempts=data.get('max_attempts', 6)
        )
        game.guesses = data.get('guesses', [])
        game.letter_status = data.get('letter_status', {})
        return game
    
    def _select_target_word(self) -> str:
        """从单词库中随机选择目标单词"""
        word_path = Path(__file__).parent.parent / "data" / "words.txt"
        with open(word_path, 'r') as f:
            words = [word.strip().lower() for word in f if len(word.strip()) == self.word_length]
        return random.choice(words) if words else "apple"

    def is_valid_guess(self, guess: str) -> bool:
        """验证猜测是否有效"""
        return len(guess) == self.word_length and guess.isalpha()

    def process_guess(self, guess: str) -> list[tuple[str, str]]:
        """处理猜测并返回每个字母的状态: correct, present, absent"""
        # Convert guess to lowercase to match target word case
        guess = guess.lower()
        
        # Initialize result with 'absent' for all positions
        result = []
        target_list = list(self.target_word)
        matched = ['#'] * len(target_list)
        
        # First pass: check for correct positions
        for i in range(len(guess)):
            if guess[i] == target_list[i]:
                result.append((guess[i], 'correct'))
                matched[i] = guess[i]
                target_list[i] = '#'  # Mark as matched
            else:
                result.append((guess[i], 'absent'))
                
        # Second pass: check for present letters
        for i in range(len(guess)):
            if result[i][1] == 'absent':
                if guess[i] in target_list:
                    result[i] = (guess[i], 'present')
                    pos = target_list.index(guess[i])
                    target_list[pos] = '#'  # Mark as matched
        
        # Update letter status for keyboard display
        # 定义状态优先级: correct > present > absent
        status_priority = {'correct': 2, 'present': 1, 'absent': 0}
        
        # 更新字母状态（确保所有字母都被记录，包括缺失的）
        for letter, status in result:
            current_priority = status_priority[status]
            letter_upper = letter.upper()
            # 如果字母不在状态字典中，直接添加
            if letter_upper not in self.letter_status:
                self.letter_status[letter_upper] = status
            else:
                existing_priority = status_priority[self.letter_status[letter_upper]]
                if current_priority > existing_priority:
                    self.letter_status[letter_upper] = status
        
        self.guesses.append({'word': guess, 'result': result})
        return result

    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        return len(self.guesses) >= self.max_attempts or (len(self.guesses) > 0 and self.guesses[-1]['word'] == self.target_word)

    def is_won(self) -> bool:
        """检查玩家是否获胜"""
        return len(self.guesses) > 0 and self.guesses[-1]['word'] == self.target_word

    def to_dict(self):
        """Convert game state to dictionary for session storage"""
        return {
            'max_attempts': self.max_attempts,
            'target_word': self.target_word,
            'guesses': self.guesses,
            'letter_status': self.letter_status
        }
    
    def get_letter_status(self):
        return self.letter_status