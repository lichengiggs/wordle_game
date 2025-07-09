# Wordle 游戏

## 项目介绍
这是一个基于Python开发的Wordle游戏，支持命令行(CLI)和网页(Web)两种玩法。

## 安装依赖
```bash
pip install -r requirements.txt
```

## 玩法说明

### 1. 命令行版本
```bash
python ui/cli.py
```

### 2. 网页版本 (Flask)
#### 启动服务器
```bash
# 假设Flask入口文件为web/app.py
python web/app.py
```

#### 访问游戏
打开浏览器访问: http://localhost:5000

#### 网页端操作
1. 在输入框中输入5个字母的英文单词
2. 点击"提交"按钮或按回车键
3. 颜色说明:
   - 🟩 字母正确且位置正确
   - 🟨 字母正确但位置错误
   - ⬜ 字母不存在于目标单词中
4. 最多可尝试6次，猜对或用完次数后游戏结束

## 项目结构
- `ui/cli.py`: 命令行版本入口
- `web/app.py`: Flask网页版入口
- `data/words.txt`: 词汇表文件
- `requirements.txt`: 项目依赖