# AutoGal - AI驱动的Ren'Py游戏生成 Agentic工作流

AI-powered Ren'Py visual novel generator. Input natural language, output playable game.

## 项目结构

```
my_game_agent/
├── src/autogal/              # 主包 (src layout)
│   ├── __init__.py
│   ├── __main__.py           # CLI入口
│   ├── core/                 # 核心层
│   │   ├── config.py         # 配置管理
│   │   ├── constants.py      # 常量
│   │   ├── exceptions.py     # 异常
│   │   └── domain/           # 数据模型
│   │       ├── scenario.py   # 剧本
│   │       ├── character.py  # 角色
│   │       ├── asset.py      # 资产
│   │       └── project.py    # 项目配置
│   ├── agents/               # Agent层
│   │   ├── base.py           # 基类
│   │   ├── writer/           # 剧本生成
│   │   ├── artist/           # 图像生成
│   │   ├── coder/            # 项目构建
│   │   └── orchestrator.py   # 协调器
│   ├── providers/            # Provider层
│   │   ├── llm/              # LLM抽象
│   │   └── image/            # 图像抽象
│   ├── builders/             # Ren'Py构建器
│   └── utils/                # 工具
│
├── tests/                    # 测试
├── templates/                # Ren'Py模板
├── pyproject.toml
├── requirements.txt
└── .env.example
```

## 快速开始

```bash
# 安装
pip install -e .

# 配置
cp .env.example .env
# 编辑 .env，填入 API Key

# 运行
autogal "一个赛博朋克咖啡馆相遇故事"
```

## 支持的API

| 类型 | Provider |
|------|----------|
| LLM | 通义千问、OpenAI、Claude |
| 图像 | 通义万相、DALL-E |

## 开发阶段

- [x] 阶段一: MVP核心引擎
- [ ] 阶段二: FastAPI后端
- [ ] 阶段三: 前端界面
- [ ] 阶段四: 部署

MIT License
