# -*- coding: utf-8 -*-
"""
Discussion 工具
发评论到 GitHub Discussion
"""

from .github import GitHubClient
from datetime import datetime

def post_to_discussion(owner, repo, token, discussion_number, content):
    """发评论到 Discussion"""
    client = GitHubClient(token=token, owner=owner, repo=repo)
    return client.add_discussion_comment(discussion_number, content)

def format_daily_post(date, image_urls):
    """格式化每日图片帖子
    
    Args:
        date: 日期字符串，如 "2026-03-18"
        image_urls: 图片 URL 列表
    
    Returns:
        Markdown 格式的内容
    """
    beijing_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"## 🦞 龙虾趣图 - {date}\n\n"
    content += f"*更新时间: {beijing_time}*\n\n"
    
    for i, url in enumerate(image_urls, 1):
        content += f"### 图片 {i}\n"
        content += f"![龙虾趣图 {i}]({url})\n\n"
    
    content += "---\n"
    content += f"*由 Clawimgs Monitor 自动推送*"
    
    return content

def format_single_image_post(date, image_url, image_index=1):
    """格式化单张图片帖子
    
    Args:
        date: 日期字符串
        image_url: 图片 URL
        image_index: 图片序号
    
    Returns:
        Markdown 格式的内容
    """
    beijing_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"## 🦞 龙虾趣图 - {date} (图{image_index})\n\n"
    content += f"![龙虾趣图]({image_url})\n\n"
    content += f"*更新时间: {beijing_time}*"
    
    return content
