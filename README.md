# WeChat → ChatGPT

这个仓库现在改用 **WeChat EXP**，不再依赖 WeFlow。

上游项目：
https://github.com/sunhanaix/pc_wechat_exp

当前固定版本：
- v2.10.20260928
- Windows x64 EXE
- SHA-256: `000BC70437123D68C953D35D0F95DC0C12C2A5757686BD8F0F04717A9663BB6B`

## 你怎么用

### 第一次

1. 确保 Windows 微信已经登录。
2. 双击 `一键安装.bat`。
3. 安装脚本会从上游 GitHub Release 下载官方 EXE，并校验 SHA-256。
4. 双击 `微信聊天给GPT.bat`。

WeChat EXP 会在本机启动，网页地址是：

`http://127.0.0.1:5000`

第一次需要先做一次「一键备份」。

### 以后

直接双击：

`微信聊天给GPT.bat`

脚本会启动 WeChat EXP，并打开「聊天导出」页面。

推荐导出格式：

- 少量/普通聊天：TXT
- 聊天很多、希望保留结构：ChatLab JSON
- 超大聊天：ChatLab JSONL

导出完后，把文件直接拖到 ChatGPT 里即可。

## 隐私

- 微信聊天和备份只保存在你自己的电脑。
- 本仓库不会上传聊天记录到 GitHub。
- `backup/`、`output/`、`exports/`、下载的 EXE 等都被 `.gitignore` 排除。
- 请只处理你有权访问和分析的聊天数据。

## 为什么换掉 WeFlow

WeChat EXP 当前提供可直接下载的 Windows EXE，并且原生支持：

- WeChat 4.x
- Windows 10/11
- 一键备份
- 聊天查看
- TXT / HTML / ChatLab JSON / JSONL 导出
- 本地 Web UI
- CLI 导出
- 图片、语音等媒体处理

所以它更适合当前“微信聊天 → 导出文件 → 给 ChatGPT 分析”的目标。

## 上游版本说明

本仓库只负责简化启动流程，不修改 WeChat EXP 本体。
如果上游更新微信兼容性，后续可以再升级这里固定的版本。
