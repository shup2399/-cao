# WeChat → ChatGPT

一个尽量简单的 Windows 小工具：从本机 WeFlow HTTP API 读取微信聊天记录，整理成适合直接上传给 ChatGPT 的 JSON / Markdown 文件。

> 隐私：聊天记录只保存在你的电脑。本仓库不会自动上传聊天数据到 GitHub。

## 使用前准备

1. Windows 10/11 x64，微信 4.0+。
2. 安装并运行 WeFlow。
3. WeFlow → 设置 → API 服务 → 启动服务。
4. 记下 WeFlow 的 Access Token（API 默认地址为 `http://127.0.0.1:5031`）。
5. 双击 `setup.bat` 完成初始化。
6. 双击 `一键导出微信聊天.bat`。

程序会：
- 检查 WeFlow 是否在线；
- 获取会话列表；
- 让你选择联系人/群；
- 自动分页拉取聊天；
- 在本机 `private_exports/` 生成 JSON 和 Markdown；
- 尝试打开输出文件夹。

然后把生成的 `*_chatgpt.md` 或 `*_chatgpt.json` 直接拖进 ChatGPT 即可分析。

## Token

首次运行会提示输入 Token，并只写入本机 `.env.local`。该文件已经被 gitignore。

也可手工复制：

```
copy .env.example .env.local
```

然后编辑 `.env.local`。

## 数据安全

`private_exports/`、`.env.local`、聊天 JSON/CSV/TXT/HTML、媒体缓存均被忽略。不要手工强制提交真实聊天记录。

## WeFlow

本项目不包含、不重新分发 WeFlow。请从 WeFlow 官方项目安装。API 仍处于早期阶段，未来接口变化时本工具可能需要同步更新。
