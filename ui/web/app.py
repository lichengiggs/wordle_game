import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask, render_template, request, session, redirect, url_for
from game.wordle import WordleGame
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于会话管理的密钥

# 确保中文显示正常
app.config['JSON_AS_ASCII'] = False

# 加载单词列表
with open(Path(__file__).parent.parent.parent / 'data/words.txt', 'r', encoding='utf-8') as f:
    WORD_LIST = [word.strip().upper() for word in f.readlines()]

@app.route('/', methods=['GET', 'POST'])
def index():
    # 初始化游戏
    if 'game_state' not in session:
        new_game = WordleGame(WORD_LIST)
        session['game_state'] = new_game.to_dict()
        session['guesses'] = []
        session['game_over'] = False
        session['win'] = False

    # 处理猜测提交
    if request.method == 'POST' and not session.get('game_over', False):
        guess = request.form.get('guess', '').strip().upper()
        game = WordleGame.from_dict(session['game_state'], WORD_LIST)

        if game.is_valid_guess(guess):
            result = game.process_guess(guess)
            session['guesses'].append({'guess': guess, 'result': result})
            session['game_state'] = game.to_dict()
            session['game_over'] = game.is_game_over()
            session['win'] = game.is_won()

            if session['game_over']:
                return redirect(url_for('result'))

    # 获取字母状态用于键盘显示
    game = WordleGame.from_dict(session['game_state'], WORD_LIST)
    letter_status = game.get_letter_status()

    return render_template('index.html', game=game, guesses=game.guesses, letter_status=letter_status)

@app.route('/result')
def result():
    if 'game_state' not in session:
        return redirect(url_for('index'))

    game = WordleGame.from_dict(session['game_state'], WORD_LIST)
    return render_template('result.html', game=game, target=game.target_word, guesses=game.guesses, won=game.is_won())

@app.route('/reset')
def reset():
    # 清除会话数据以开始新游戏
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)