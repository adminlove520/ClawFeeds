
# 📢 RSS Monitor - OPENCLAWMEME 版

> Telegram 频道 @OPENCLAWMEME 图片自动监控推送工具

**当前版本：V2.0.0**

---

## ✨ 核心特性

- **Telegram RSS 监控**：通过 RSSHub 监控 Telegram 频道更新
- **自动图片提取**：自动从 RSS 中提取图片 URL
- **GitHub Discussion 推送**：自动发评论到指定 Discussion（支持图片展示）
- **多平台推送支持**：Discord、钉钉、飞书、Telegram
- **抗封锁机制**：429 自动重试、循环监控模式

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/adminlove520/Clawimgs_monitor.git
cd Clawimgs_monitor
```

### 2. 配置 RSS

编辑 `rss.yaml`：

```yaml
"OPENCLAWMEME":
  "rss_url": "https://rss-hub-iota-rosy.vercel.app/telegram/channel/OPENCLAWMEME"
  "website_name": "OPENCLAWMEME"
```

### 3. 配置推送

编辑 `config.yaml`：

```yaml
# GitHub 配置
github:
  token: "ghp_xxxxxxxxxxxxxxxxxxxx"
  owner: "adminlove520"
  repo: "Clawimgs_monitor"

# 推送配置
push:
  github_discussion:
    switch: "ON"
    discussion_owner: "ythx-101"
    discussion_repo: "openclaw-qa"
    discussion_number: 32  # 创建好Discussion后填入编号
    mode: "each"  # "each" 每张图片发一条，"daily" 每天汇总发一条
```

### 4. 运行

```bash
pip install -r requirements.txt
python Rss_monitor.py
```

### 5. 开机自启

```bash
# Windows
schtasks /create /tn "ClawimgsMonitor" /tr "python C:\path\to\Clawimgs_monitor\Rss_monitor.py" /sc minute /mo 5 /f
```

---

## 📝 配置说明

### rss.yaml

| 配置项 | 说明 |
|--------|------|
| website_name | 网站名称（用于日志） |
| rss_url | RSSHub URL |

### config.yaml

#### GitHub 配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| token | GitHub Token | - |
| owner | 仓库所有者 | - |
| repo | 仓库名 | - |

#### GitHub Discussion 推送

| 配置项 | 说明 |
|--------|------|
| switch | ON/OFF |
| discussion_owner | Discussion 所在仓库 owner |
| discussion_repo | Discussion 所在仓库名 |
| discussion_number | Discussion 编号 |
| mode | "each" 每张图片发一条，"daily" 每天汇总 |

---

## 🔧 部署方式

### 方式一：本地运行

```bash
python Rss_monitor.py
```

### 方式二：开机自启

**Windows**:
```powershell
schtasks /create /tn "ClawimgsMonitor" /tr "python C:\path\to\Rss_monitor.py" /sc minute /mo 5 /f
```

**Linux (systemd)**:
```ini
[Unit]
Description=Clawimgs Monitor
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/Rss_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📂 项目结构

```
.
├── Rss_monitor.py          # 主程序入口
├── rss.yaml               # RSS 源配置
├── config.yaml             # 推送配置
├── utils/
│   ├── notify.py          # 推送逻辑
│   ├── rss.py             # RSS 解析
│   ├── config.py          # 配置加载
│   ├── db.py             # 数据库
│   ├── github.py         # GitHub API
│   └── discussion.py     # Discussion 工具
└── requirements.txt
```

---

## 📜 许可证

MIT License

---

🦞 小溪的作品 - 帮哥哥守护 OPENCLAWMEME 图片！
