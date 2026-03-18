# -*- coding: utf-8 -*-
"""
GitHub API 工具
上传文件到 Release、上传图片等
"""

import os
import requests
import base64
from urllib.parse import urljoin

GITHUB_API = "https://api.github.com"
GITHUB_GRAPHQL = "https://api.github.com/graphql"

class GitHubClient:
    def __init__(self, token=None, owner=None, repo=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.owner = owner
        self.repo = repo
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.headers_graphql = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method, url, **kwargs):
        kwargs.setdefault("headers", self.headers)
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}
    
    def _graphql(self, query, variables=None):
        """GraphQL 请求"""
        url = GITHUB_GRAPHQL
        data = {"query": query}
        if variables:
            data["variables"] = variables
        
        response = requests.post(url, headers=self.headers_graphql, json=data)
        response.raise_for_status()
        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")
        return result.get("data", {})
    
    def get_release_by_tag(self, tag):
        """获取指定 tag 的 Release"""
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/releases/tags/{tag}"
        return self._request("GET", url)
    
    def create_release(self, tag, name=None, body=""):
        """创建 Release"""
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/releases"
        data = {
            "tag_name": tag,
            "name": name or tag,
            "body": body
        }
        return self._request("POST", url, json=data)
    
    def upload_asset(self, release_id, filename, content_type, data):
        """上传 Asset 到 Release"""
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/releases/{release_id}/assets"
        
        # GitHub API 上传 Asset 需要不同的处理
        upload_url = f"https://uploads.github.com/repos/{self.owner}/{self.repo}/releases/{release_id}/assets?name={filename}"
        
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": content_type
        }
        
        response = requests.post(
            upload_url,
            headers=headers,
            data=data
        )
        response.raise_for_status()
        return response.json()
    
    def upload_image_to_release(self, tag, image_url, filename=None):
        """从 URL 下载图片并上传到 Release"""
        import uuid
        
        # 下载图片
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        content = response.content
        content_type = response.headers.get("Content-Type", "image/jpeg")
        
        # 生成文件名
        if not filename:
            ext = content_type.split("/")[-1]
            if ext == "jpeg":
                ext = "jpg"
            filename = f"{uuid.uuid4().hex[:8]}.{ext}"
        
        # 获取或创建 Release
        try:
            release = self.get_release_by_tag(tag)
        except Exception:
            release = self.create_release(tag)
        
        # 上传 Asset
        asset = self.upload_asset(release["id"], filename, content_type, content)
        
        # 返回直链
        return asset.get("browser_download_url")
    
    def add_discussion_comment(self, discussion_id, body):
        """在 Discussion 添加评论（使用 GraphQL）"""
        # 先获取 discussion 的 node_id
        query = """
        query($owner: String!, $repo: String!, $discussionNumber: Int!) {
          repository(owner: $owner, name: $repo) {
            discussion(number: $discussionNumber) {
              id
            }
          }
        }
        """
        variables = {
            "owner": self.owner,
            "repo": self.repo,
            "discussionNumber": int(discussion_id)
        }
        
        result = self._graphql(query, variables)
        discussion_node_id = result.get("repository", {}).get("discussion", {}).get("id")
        
        if not discussion_node_id:
            raise Exception(f"Discussion #{discussion_number} not found")
        
        # 添加评论
        mutation = """
        mutation($discussionId: ID!, $body: String!) {
          addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {
            comment { id }
          }
        }
        """
        variables = {
            "discussionId": discussion_node_id,
            "body": body
        }
        
        result = self._graphql(mutation, variables)
        return result.get("addDiscussionComment", {}).get("comment", {})
    
    def create_discussion(self, category_id, title, body):
        """创建 Discussion"""
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/discussions"
        data = {
            "category_id": category_id,
            "title": title,
            "body": body
        }
        return self._request("POST", url, json=data)


def get_asset_url(owner, repo, tag, filename):
    """获取 Release Asset 的直链"""
    return f"https://github.com/{owner}/{repo}/releases/download/{tag}/{filename}"
