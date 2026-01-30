#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章抓取归档工具
WeChat Article Archive Tool
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import re
import json
import hashlib
import sys
from datetime import datetime
from pathlib import Path


def fetch_wechat_article(url, delay_range=(1, 3), timeout=10):
    """
    抓取微信公众号文章内容

    Args:
        url: 微信公众号文章完整URL
        delay_range: 随机延迟范围（秒）
        timeout: 请求超时时间（秒）

    Returns:
        dict: 抓取结果，失败时包含 error 字段
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        # 随机延迟，降低被风控概率
        time.sleep(random.uniform(*delay_range))

        print("🚀 正在抓取文章...")
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        resp.encoding = 'utf-8'

        soup = BeautifulSoup(resp.text, 'html.parser')

        # 提取标题
        title_tag = soup.find('h1', class_='rich_media_title')
        title = title_tag.get_text(strip=True) if title_tag else "未知标题"

        # 提取正文
        content_div = soup.find('div', class_='rich_media_content')
        content = ""
        if content_div:
            for elem in content_div.select('p, section, h1, h2, h3, h4'):
                text = elem.get_text(strip=True)
                if text:
                    # 保持标题格式
                    if elem.name in ['h1', 'h2', 'h3', 'h4']:
                        content += f"\n## {text}\n\n"
                    else:
                        content += f"{text}\n\n"
            content = content.strip()

        # 提取作者
        author_tag = soup.find('span', class_='rich_media_meta rich_media_meta_text')
        author = author_tag.get_text(strip=True) if author_tag else ""

        # 提取发布时间
        publish_time = "未知时间"

        # 方法1: 从JS变量提取
        time_match = re.search(r'var ct\s*=\s*"(\d+)"', resp.text)
        if time_match:
            ts = int(time_match.group(1))
            publish_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        else:
            # 方法2: 从meta标签提取
            meta_time = soup.find('meta', {'property': 'og:article:published_time'}) or \
                       soup.find('meta', {'property': 'article:published_time'}) or \
                       soup.find('em', id='publish_time')
            if meta_time:
                content_time = meta_time.get('content') if meta_time.name == 'meta' else meta_time.get_text(strip=True)
                if content_time:
                    publish_time = content_time

        print(f"✅ 成功抓取: {title}")

        return {
            "title": title,
            "content": content,
            "author": author,
            "publish_time": publish_time,
            "url": url,
            "status": "success"
        }

    except Exception as e:
        return {
            "error": f"抓取失败: {str(e)}",
            "url": url,
            "status": "failed"
        }


class WeChatArchiveManager:
    """微信文章归档管理器"""

    def __init__(self, vault_dir="outputs/20-阅读笔记"):
        self.vault_dir = Path(vault_dir)
        self.vault_dir.mkdir(parents=True, exist_ok=True)

    def generate_slug(self, title, url_hash):
        """生成文件夹名称"""
        date_str = datetime.now().strftime("%Y%m%d")
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'[-\s]+', '-', clean_title.strip())[:30]
        return f"{date_str}-{clean_title}-{url_hash[:6]}"

    def create_obsidian_note(self, result, folder_path):
        """创建 Obsidian 格式的笔记"""
        slug = folder_path.name
        filename = f"{slug}.md"
        note_path = folder_path / filename

        # 创建 front matter
        front_matter = {
            "title": result['title'],
            "author": result.get('author', ''),
            "date": result.get('publish_time', datetime.now().strftime('%Y-%m-%d')),
            "url": result['url'],
            "tags": ["wechat", "article"],
            "archived": datetime.now().isoformat()
        }

        # 创建笔记内容
        note_content = f"""---
{json.dumps(front_matter, ensure_ascii=False, indent=2)}
---

# {result['title']}

## 📖 文章信息

- **作者**: {result.get('author', '未知')}
- **发布时间**: {result.get('publish_time', '未知')}
- **原文链接**: [🔗 点击阅读]({result['url']})

## 🔍 内容摘要

> 核心摘要内容...

## 💡 核心观点

1.
2.
3.

## 📚 关键概念

1. **概念1**:
2. **概念2**:
3. **概念3**:

## 🤔 个人思考

-
-

## 📋 行动项

- [ ] 整理笔记
- [ ] 延伸阅读
- [ ] 实践应用

---
*归档于: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}*
"""

        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(note_content)
        return note_path

    def save_original_article(self, result, folder_path):
        """保存原始文章"""
        content = result.get('content', '')

        # 如果内容没有标题，添加标题
        if not content.startswith('#'):
            content = f"# {result['title']}\n\n{content}"

        article_content = f"""{content}

---
*原文发布: {result.get('publish_time', '')}*
*原文链接: {result['url']}*
"""

        article_path = folder_path / "article.md"
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(article_content)
        return article_path

    def save_metadata(self, result):
        """保存元数据"""
        meta = {
            "title": result['title'],
            "author": result.get('author', ''),
            "publish_time": result.get('publish_time', ''),
            "url": result['url'],
            "archived_at": datetime.now().isoformat(),
            "word_count": len(result.get('content', '').split()),
            "content_hash": hashlib.sha256(result.get('content', '').encode()).hexdigest()
        }
        return meta

    def archive_article(self, url):
        """
        完整归档流程

        Args:
            url: 微信公众号文章URL

        Returns:
            dict: 归档结果
        """
        print(f"\n开始归档: {url}")

        # 1. 抓取文章
        result = fetch_wechat_article(url)

        if result['status'] == 'failed':
            return result

        # 2. 生成路径
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        slug = self.generate_slug(result['title'], url_hash)

        folder_path = self.vault_dir / slug
        folder_path.mkdir(exist_ok=True)

        print("📝 正在保存文件...")

        # 3. 保存文件
        note_path = self.create_obsidian_note(result, folder_path)
        article_path = self.save_original_article(result, folder_path)

        # 4. 保存元数据
        meta = self.save_metadata(result)
        meta_path = folder_path / "meta.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        print("✨ 归档完成!")
        print(f"📁 文件位置: {folder_path}")

        return {
            "status": "success",
            "title": result['title'],
            "author": result.get('author', ''),
            "publish_time": result.get('publish_time', ''),
            "folder": str(folder_path),
            "slug": slug,
            "word_count": len(result.get('content', '').split())
        }