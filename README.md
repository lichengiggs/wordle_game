# Wordle 游戏

经典Wordle游戏的Python实现，支持命令行界面。

## 项目结构
```
wordle_game/
├── game/           # 游戏核心逻辑
├── ui/             # 用户界面（命令行）
├── tests/          # 单元测试
├── data/           # 单词库数据
├── venv/           # Python虚拟环境
├── requirements.txt # 项目依赖
└── README.md       # 项目文档
```

## 安装步骤
1. 克隆项目到本地
2. 进入项目目录: `cd wordle_game`
3. 创建并激活虚拟环境: `python -m venv venv && source venv/bin/activate` (macOS/Linux)
4. 安装依赖: `pip install -r requirements.txt`

## 如何玩
1. 激活虚拟环境: `source venv/bin/activate`
2. 运行游戏: `python ui/cli.py`
3. 输入5个字母的单词进行猜测，按回车键确认
4. 颜色说明:
   - 绿色: 字母正确且位置正确
   - 黄色: 字母正确但位置错误
   - 灰色: 字母不存在于目标单词中

## 运行测试
执行单元测试: `pytest tests/`