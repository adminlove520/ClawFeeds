# -*- coding: utf-8 -*-
import requests
import re
import sys
import html

url = 'https://rss-hub-iota-rosy.vercel.app/telegram/channel/OPENCLAWMEME'
resp = requests.get(url, timeout=30)
entries = resp.text.split('<item>')

print(f"获取到 {len(entries)-1} 条条目")

# 取最新一条
if len(entries) > 1:
    entry = entries[1]
    # 提取 description 并解码 HTML 实体
    desc_match = re.search(r'<description>(.*?)</description>', entry, re.DOTALL)
    if desc_match:
        desc = html.unescape(desc_match.group(1))
        # 提取 img src
        img_match = re.search(r'<img src="([^"]+)"', desc)
        if img_match:
            print('✅ 图片 URL:', img_match.group(1))
        # 提取 link
        link_match = re.search(r'<link>([^<]+)</link>', entry)
        if link_match:
            print('✅ Telegram 链接:', link_match.group(1))
