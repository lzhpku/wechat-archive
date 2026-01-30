#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Article Archive CLI - Skill Interface

This script provides a simple interface for the Claude Code skill system
to archive WeChat articles with default settings.

Usage:
    python archive_article.py <url>
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_archive import fetch_wechat_article, WeChatArchiveManager


def main():
    if len(sys.argv) != 2:
        print("❌ 用法: python archive_article.py <微信公众号文章URL>")
        print("示例: python archive_article.py https://mp.weixin.qq.com/s/xxxxxx")
        sys.exit(1)

    url = sys.argv[1]

    # Validate WeChat URL
    if "mp.weixin.qq.com" not in url:
        print("❌ 错误: URL 必须来自微信公众号")
        print("   请提供类似 'https://mp.weixin.qq.com/s/xxx' 的格式")
        sys.exit(1)

    # Use default output directory from skill context
    output_dir = os.environ.get('WECHAT_ARCHIVE_OUTPUT_DIR', 'outputs/20-阅读笔记')

    try:
        # Create archiver and archive the article
        archiver = WeChatArchiveManager(output_dir)
        result = archiver.archive_article(url)

        # Output in a format easy for Claude Code to parse
        if result.get("status") == "success":
            print(f"SUCCESS: {result['title']}")
            print(f"AUTHOR: {result.get('author', 'Unknown')}")
            print(f"DATE: {result.get('publish_time', 'Unknown')}")
            print(f"FOLDER: {result['folder']}")
            print(f"WORD_COUNT: {result['word_count']}")
        else:
            print(f"ERROR: {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        print(f"ERROR: 归档过程中发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()