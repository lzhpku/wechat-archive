---
name: wechat-archive
description: Archives WeChat articles from mp.weixin.qq.com URLs, extracting content and saving as Obsidian-compatible markdown files. Use when users need to save WeChat articles for offline reading or knowledge management.
---

# WeChat Archive

## Overview

Archives WeChat public account articles from mp.weixin.qq.com URLs by extracting the article content and saving it as markdown files in Obsidian-compatible format. The skill creates organized folders with article content, metadata, and note templates for easy knowledge management.

## Core Capabilities

### 1. Article Extraction
- Scrapes WeChat articles from provided URLs
- Extracts title, author, publish date, and article content
- Handles WeChat's specific HTML structure
- Includes automatic delays to avoid rate limiting

### 2. Content Organization
- Creates timestamped folders for each article
- Generates an Obsidian-formatted note with frontmatter
- Saves a clean version of the original article
- Stores metadata in JSON format

### 3. Archival Features
- Automatic WeChat URL validation
- Content formatting for readability
- Word count tracking
- Archive timestamp recording

## Usage

To archive a WeChat article, use the bundled script:

```bash
python scripts/archive_article.py "<wechat_article_url>"
```

The skill will:
1. Validate the WeChat URL
2. Extract article content and metadata
3. Create an organized archive folder
4. Generate Obsidian-compatible notes

## Example

```bash
python scripts/archive_article.py "https://mp.weixin.qq.com/s/abcdef123456"
```

This creates:
- A timestamped folder in `outputs/20-阅读笔记/`
- An Obsidian note with article summary template
- The original article content in markdown
- Metadata file with article details

## Scripts

### scripts/wechat_archive.py
Core archive functionality with WeChatArticle class for content extraction and WeChatArchiveManager for organizing archives.

### scripts/archive_article.py
Command-line interface that uses the core functionality to archive articles with appropriate output formatting for Claude Code.
