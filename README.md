📮 Telegram 双向转发机器人

一个基于 Python的telegram-bot 的轻量级 “留言通讯” 机器人。
普通用户向机器人发送消息后，机器人会自动转发给管理员；
管理员只需要 回复机器人推送的消息，即可将内容转回对应用户，实现真正的双向沟通。

适用于：客服机器人、反馈、站点留言、沟通、等场景。


---

✨ 功能特点

📩 用户 → 管理员 的消息自动转发

🔁 管理员 → 用户 的消息通过“回复”完成回传

🖼 支持文字、图片、文件、语音等多媒体消息

🔐 使用 .env 存储敏感配置

🚀 零数据库依赖，开箱即用

🧩 代码清晰、易扩展，可根据需要加入多管理员、持久化等功能



---

🧱 环境要求

Python 3.10+

一个 Telegram Bot Token（通过 @BotFather 获取）

管理员的 Telegram 用户 ID（可使用 @getidsbot 查询）



---

📦 安装步骤

1. 克隆项目

git clone https://github.com/Lou-Xiaohei/Messaging_Telegram_Bot.git
cd Messaging_Telegram_Bot

2. 安装依赖

pip install -r requirements.txt


---

⚙️ 配置 .env

1. 编辑 .env

BOT_TOKEN=1234567890:ABCDEF_xxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_ID=123456789

说明：

BOT_TOKEN → 你的机器人 Token

ADMIN_ID → 管理员 Telegram ID（必须是纯数字）



---

▶️ 启动机器人

python bot.py

启动后可在 Telegram 中对机器人发送 /start 测试是否正常工作。


---

📘 使用说明

👤 普通用户

直接与机器人对话，发送文字、图片、文件等消息

机器人会自动将消息转发给管理员

当管理员通过机器人回复后，消息会自动返回用户


👑 管理员

会收到所有用户的消息，会附带用户信息（ID、昵称等）

只需对某条消息使用 回复（Reply）

机器人会将你的回复发送回对应的用户

无需记住用户 ID，完全自动映射



---

❗ 常见问题

❓ “Unauthorized” 或 Token 错误

请检查 .env 中的 BOT_TOKEN 是否正确，机器人是否已启用。

❓ 管理员回复后用户收不到消息

确认 ADMIN_ID 正确

程序是否正在运行

如果机器人重启过，message_id 映射丢失，需要用户重新发送一条消息以重新建立映射。



---

📁 项目结构

telegram-relay-bot/
├── bot.py            # 机器人主程序
├── requirements.txt  # 依赖列表
├── .env.example      # 环境变量示例
└── README.md         # 使用说明文档


---

🤝 扩展方向（可自行添加二开）

多管理员 / 管理群组支持

黑名单 / 反垃圾过滤

日志文件输出

Docker 容器化部署

