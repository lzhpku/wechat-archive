# WeChat Archive Skill for Claude Code

A Claude Code skill that archives WeChat public account articles from mp.weixin.qq.com URLs. This skill extracts article content and saves it as markdown files in Obsidian-compatible format for easy knowledge management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.ai/claude-code)

## Features

- 📄 **Article Extraction**: Automatically scrapes WeChat articles from provided URLs
- 📝 **Content Organization**: Creates timestamped folders with article content
- 🏷️ **Obsidian Integration**: Generates Obsidian-formatted notes with frontmatter
- 📚 **Knowledge Management**: Saves both processed notes and original content
- 🛡️ **Rate Limiting**: Includes automatic delays to prevent being blocked

## Installation

1. Download the latest `wechat-archive.skill` file from [Releases](https://github.com/YOUR_USERNAME/wechat-archive-skill/releases)
2. Install in Claude Code:
   ```bash
   gemini skills install wechat-archive.skill --scope user
   ```
3. Reload skills:
   ```
   /skills reload
   ```

## Usage

Once installed, you can use this skill by asking Claude Code to archive WeChat articles:

```
Please archive this WeChat article: https://mp.weixin.qq.com/s/YOUR_ARTICLE_ID
```

Or use the script directly:

```bash
python scripts/archive_article.py "https://mp.weixin.qq.com/s/YOUR_ARTICLE_ID"
```

## Output Structure

The skill creates a structured archive with:
- **Obsidian Note**: Pre-formatted note with article metadata and summary template
- **Original Article**: Clean markdown version of the original content
- **Metadata**: JSON file with article details and archive information

## skill Structure

```
wechat-archive/
├── SKILL.md             # Main skill definition and instructions
├── scripts/
│   ├── wechat_archive.py    # Core archive functionality
│   └── archive_article.py   # CLI interface
├── references/          # Additional documentation
└── assets/             # Templates and resources
```

## Requirements

This skill requires the following Python packages:
- `requests` - For HTTP requests
- `beautifulsoup4` - For HTML parsing

Install dependencies:
```bash
pip install requests beautifulsoup4
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)
