# Payload CMS Lexical Rich Text Format

When publishing content to Payload CMS via the MCP (e.g., `createPosts`, `updatePosts`), the `content` field uses Lexical rich text format. This is a nested JSON structure that must follow specific rules.

## Structure

```json
{
  "root": {
    "type": "root",
    "children": [...],
    "direction": "ltr",
    "format": "",
    "indent": 0,
    "version": 1
  }
}
```

## Node Types

### Paragraph

```json
{
  "type": "paragraph",
  "version": 1,
  "children": [
    {"text": "普通文本", "type": "text", "version": 1},
    {"text": "粗体", "type": "text", "format": 1, "version": 1},
    {"text": "斜体", "type": "text", "format": 2, "version": 1},
    {"text": "行内代码", "type": "text", "format": 16, "version": 1}
  ]
}
```

Text formats: `format: 1` = bold, `format: 2` = italic, `format: 16` = inline code.

### Heading

```json
{
  "type": "heading",
  "tag": "h2",
  "version": 1,
  "children": [{"text": "章节标题", "type": "text", "version": 1}]
}
```

Tags: `h1` through `h6`.

### Code Block

```json
{
  "type": "code",
  "language": "text",
  "version": 1,
  "children": [{"text": "code content here", "type": "text", "version": 1}]
}
```

The entire code block content goes in a single text node. Newlines are literal `\n`.

### Upload / Image

```json
{
  "type": "upload",
  "value": 35,
  "relationTo": "media",
  "version": 3,
  "fields": null,
  "format": ""
}
```

`value` is the media document ID. `version: 3` is required for upload nodes.

## Critical Rules

1. **Every node MUST have `version`** — including text leaves, paragraphs, headings. Missing this field causes `-32602 Input validation error`.
2. **Text nodes inside paragraphs** need `"type": "text"` explicitly.
3. **Code blocks** put all content in a single text child under `children`.
4. **No sibling text outside children** — all text must be inside `children` arrays.

## Shell Escaping for mcporter

When passing content JSON via mcporter CLI, the content string contains quotes and braces that need shell escaping:

```bash
mcporter call aicodewith-cms.createPosts \
  title="标题" \
  slug="slug" \
  excerpt="摘要" \
  content='{"root":{"type":"root","children":[...]}}' \
  coverImage=1 \
  _status=published
```

**Better approach**: write content JSON to a temp file, then reference it in a shell script to avoid escaping hell:

```bash
#!/bin/bash
CONTENT=$(cat /tmp/content.json)
mcporter call aicodewith-cms.createPosts \
  title="..." slug="..." excerpt="..." \
  content="$CONTENT" coverImage=1 _status=published
```
