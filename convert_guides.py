#!/usr/bin/env python3
"""Convert markdown guides to HTML pages with dark theme styling."""

import re
import os

CSS = """
    <style>
        :root {
            --bg: #0a0a0a;
            --card: #161616;
            --border: #2a2a2a;
            --text: #e0e0e0;
            --muted: #888;
            --accent: #4ade80;
            --accent2: #38bdf8;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.8;
            min-height: 100vh;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem; }
        .back-link { display: inline-block; color: var(--accent); text-decoration: none; font-size: 0.95rem; margin-bottom: 2rem; }
        .back-link:hover { text-decoration: underline; }
        h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; line-height: 1.3; }
        h2 { font-size: 1.5rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
        h3 { font-size: 1.2rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; color: var(--accent); }
        h4 { font-size: 1.05rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        p { margin-bottom: 1rem; font-size: 0.95rem; }
        a { color: var(--accent); text-decoration: none; }
        a:hover { text-decoration: underline; }
        strong { color: #fff; }
        code { background: #1a1a1a; padding: 2px 6px; border-radius: 4px; font-size: 0.85rem; font-family: 'Consolas', 'Monaco', monospace; }
        pre { background: #1a1a1a; border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem; overflow-x: auto; }
        pre code { background: none; padding: 0; font-size: 0.85rem; line-height: 1.6; }
        ul, ol { margin-bottom: 1rem; padding-left: 1.5rem; }
        li { margin-bottom: 0.4rem; font-size: 0.95rem; }
        li ul, li ol { margin-top: 0.4rem; margin-bottom: 0.4rem; }
        blockquote {
            border-left: 3px solid var(--accent);
            background: #111;
            padding: 1rem 1.25rem;
            margin-bottom: 1.5rem;
            border-radius: 0 8px 8px 0;
        }
        blockquote p { margin-bottom: 0.5rem; }
        blockquote p:last-child { margin-bottom: 0; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; font-size: 0.9rem; }
        th { background: #1a1a1a; color: var(--accent); text-align: left; padding: 0.75rem; border: 1px solid var(--border); font-weight: 600; }
        td { padding: 0.75rem; border: 1px solid var(--border); }
        tr:hover { background: #1a1a1a; }
        hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
        .badge { display: inline-block; background: var(--accent); color: #000; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 4px; margin-bottom: 1rem; }
        .info-box { background: linear-gradient(135deg, #1a2e1a 0%, #162535 100%); border: 1px solid var(--accent); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem; }
        .info-box p { margin-bottom: 0.5rem; }
        .cta-box {
            background: linear-gradient(135deg, #1a2e1a 0%, #162535 100%);
            border: 1px solid var(--accent);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin-top: 3rem;
        }
        .cta-box h2 { border-bottom: none; margin-top: 0; padding-bottom: 0; font-size: 1.3rem; color: #fff; }
        .cta-box p { color: var(--muted); font-size: 0.95rem; margin-bottom: 1.25rem; }
        .cta-buttons { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
        .btn { display: inline-block; background: var(--accent); color: #000; font-weight: 600; text-decoration: none; padding: 0.5rem 1.25rem; border-radius: 8px; font-size: 0.9rem; transition: opacity 0.2s; }
        .btn:hover { opacity: 0.85; text-decoration: none; }
        .btn-yt { background: #ff0000; color: #fff; }
        .btn-kakao { background: #fee500; color: #000; }
        .btn-site { background: var(--accent2); color: #000; }
        footer { text-align: center; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.85rem; }
        footer a { color: var(--accent); text-decoration: none; }
        .callout { border-left: 3px solid var(--accent); background: #111; padding: 1rem 1.25rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0; }
        .callout.warning { border-left-color: #f59e0b; }
        .callout.danger { border-left-color: #ef4444; }
        .callout.success { border-left-color: var(--accent); }
        .callout.info { border-left-color: var(--accent2); }
        .callout-title { font-weight: 700; margin-bottom: 0.5rem; }
        @media (max-width: 600px) {
            .container { padding: 1.25rem 1rem; }
            h1 { font-size: 1.5rem; }
            table { font-size: 0.8rem; }
            th, td { padding: 0.5rem; }
        }
    </style>
"""

def md_to_html(md_content, title):
    """Convert markdown to HTML body content."""
    # Remove frontmatter
    md_content = re.sub(r'^---\n.*?\n---\n', '', md_content, flags=re.DOTALL)
    md_content = md_content.strip()
    
    lines = md_content.split('\n')
    html_parts = []
    i = 0
    in_list = False
    in_ordered_list = False
    list_indent_stack = []  # track nested lists
    in_table = False
    in_code_block = False
    code_block_content = []
    
    def close_lists():
        nonlocal in_list, in_ordered_list, list_indent_stack
        result = []
        while list_indent_stack:
            lt = list_indent_stack.pop()
            result.append(f'</{lt}>')
        in_list = False
        in_ordered_list = False
        return ''.join(result)
    
    def process_inline(text):
        """Process inline markdown formatting."""
        # Remove obsidian links [[#...]] and [[...]]
        text = re.sub(r'\[\[#([^\]]+)\]\]', r'\1', text)
        text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
        
        # Images (before links)
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%;border-radius:8px;margin:1rem 0;">', text)
        
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
        
        # Bold+italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # Inline code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Hashtags at end (remove them)
        text = re.sub(r'\s*#\w+(\s+#\w+)*\s*$', '', text)
        
        return text
    
    while i < len(lines):
        line = lines[i]
        
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html_parts.append(f'<pre><code>{"".join(code_block_content)}</code></pre>')
                code_block_content = []
                in_code_block = False
            else:
                if in_list or in_ordered_list:
                    html_parts.append(close_lists())
                if in_table:
                    html_parts.append('</table>')
                    in_table = False
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            from html import escape
            code_block_content.append(escape(line) + '\n')
            i += 1
            continue
        
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            if in_list or in_ordered_list:
                # Check if next non-empty line is also a list item
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and (re.match(r'^(\s*)[-*]\s', lines[j]) or re.match(r'^(\s*)\d+\.\s', lines[j])):
                    i += 1
                    continue
                html_parts.append(close_lists())
            if in_table:
                html_parts.append('</table>')
                in_table = False
            i += 1
            continue
        
        # Blockquotes (including obsidian callouts)
        if stripped.startswith('>'):
            if in_list or in_ordered_list:
                html_parts.append(close_lists())
            if in_table:
                html_parts.append('</table>')
                in_table = False
            
            # Check for obsidian callout
            callout_match = re.match(r'^>\s*\[!(tip|info|warning|danger|note|success|example|abstract|question)\]\s*(.*)', stripped)
            
            quote_lines = []
            callout_type = None
            callout_title = None
            
            if callout_match:
                callout_type = callout_match.group(1)
                callout_title = callout_match.group(2)
                css_class = 'info'
                if callout_type in ('warning',):
                    css_class = 'warning'
                elif callout_type in ('danger',):
                    css_class = 'danger'
                elif callout_type in ('success',):
                    css_class = 'success'
            else:
                first_content = re.sub(r'^>\s?', '', stripped)
                if first_content:
                    quote_lines.append(first_content)
            
            i += 1
            while i < len(lines):
                if lines[i].strip().startswith('>'):
                    content = re.sub(r'^>\s?', '', lines[i].strip())
                    quote_lines.append(content)
                    i += 1
                elif not lines[i].strip():
                    # check if next line continues the quote
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith('>'):
                        quote_lines.append('')
                        i += 1
                    else:
                        break
                else:
                    break
            
            inner = process_inline('\n'.join(quote_lines))
            # Split into paragraphs
            paragraphs = [p.strip() for p in inner.split('\n\n') if p.strip()]
            inner_html = ''.join(f'<p>{p}</p>' for p in paragraphs) if paragraphs else f'<p>{inner}</p>'
            # Handle single-line within paragraphs: replace single newlines with <br>
            inner_html = re.sub(r'(?<!</p>)\n(?!<p>)', '<br>', inner_html)
            
            if callout_type:
                html_parts.append(f'<div class="callout {css_class}">')
                if callout_title:
                    html_parts.append(f'<div class="callout-title">{process_inline(callout_title)}</div>')
                html_parts.append(inner_html)
                html_parts.append('</div>')
            else:
                html_parts.append(f'<blockquote>{inner_html}</blockquote>')
            continue
        
        # Headers
        h_match = re.match(r'^(#{1,4})\s+(.+)', stripped)
        if h_match:
            if in_list or in_ordered_list:
                html_parts.append(close_lists())
            if in_table:
                html_parts.append('</table>')
                in_table = False
            level = len(h_match.group(1))
            text = process_inline(h_match.group(2))
            html_parts.append(f'<h{level}>{text}</h{level}>')
            i += 1
            continue
        
        # Horizontal rule
        if re.match(r'^---+$', stripped):
            if in_list or in_ordered_list:
                html_parts.append(close_lists())
            if in_table:
                html_parts.append('</table>')
                in_table = False
            html_parts.append('<hr>')
            i += 1
            continue
        
        # Tables
        if '|' in stripped and not stripped.startswith('-'):
            if in_list or in_ordered_list:
                html_parts.append(close_lists())
            
            cells = [c.strip() for c in stripped.split('|')]
            cells = [c for c in cells if c or cells.index(c) not in (0, len(cells)-1)]
            # Remove empty first/last from pipe-delimited
            if stripped.startswith('|'):
                cells = [c.strip() for c in stripped[1:].split('|')]
                if cells and not cells[-1]:
                    cells = cells[:-1]
            
            # Check if next line is separator
            if not in_table:
                if i + 1 < len(lines) and re.match(r'^\|?[\s\-:|]+\|', lines[i + 1].strip()):
                    in_table = True
                    html_parts.append('<table>')
                    html_parts.append('<tr>')
                    for cell in cells:
                        html_parts.append(f'<th>{process_inline(cell)}</th>')
                    html_parts.append('</tr>')
                    i += 2  # skip separator line
                    continue
                else:
                    # Not a real table
                    html_parts.append(f'<p>{process_inline(stripped)}</p>')
                    i += 1
                    continue
            else:
                html_parts.append('<tr>')
                for cell in cells:
                    html_parts.append(f'<td>{process_inline(cell)}</td>')
                html_parts.append('</tr>')
                i += 1
                continue
        elif in_table:
            html_parts.append('</table>')
            in_table = False
            continue  # re-process this line
        
        # Checkbox list items
        checkbox_match = re.match(r'^(\s*)[-*]\s+\[([ x])\]\s+(.*)', line)
        if checkbox_match:
            indent = len(checkbox_match.group(1))
            checked = checkbox_match.group(2) == 'x'
            text = process_inline(checkbox_match.group(3))
            check_icon = '☑' if checked else '☐'
            if not in_list:
                html_parts.append('<ul style="list-style:none;padding-left:0.5rem;">')
                list_indent_stack.append('ul')
                in_list = True
            html_parts.append(f'<li>{check_icon} {text}</li>')
            i += 1
            continue
        
        # Unordered list
        list_match = re.match(r'^(\s*)[-*]\s+(.*)', line)
        if list_match:
            indent = len(list_match.group(1))
            text = process_inline(list_match.group(2))
            
            if not in_list and not in_ordered_list:
                html_parts.append('<ul>')
                list_indent_stack.append('ul')
                in_list = True
            
            html_parts.append(f'<li>{text}</li>')
            i += 1
            continue
        
        # Ordered list
        ol_match = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if ol_match:
            indent = len(ol_match.group(1))
            text = process_inline(ol_match.group(2))
            
            if not in_ordered_list and not in_list:
                html_parts.append('<ol>')
                list_indent_stack.append('ol')
                in_ordered_list = True
            
            html_parts.append(f'<li>{text}</li>')
            i += 1
            continue
        
        # Close lists if we hit non-list content
        if in_list or in_ordered_list:
            html_parts.append(close_lists())
        
        # Regular paragraph
        if stripped and not stripped.startswith('#'):
            # Check if it's a hashtag-only line
            if re.match(r'^(#\w+\s*)+$', stripped):
                i += 1
                continue
            html_parts.append(f'<p>{process_inline(stripped)}</p>')
        
        i += 1
    
    # Close any remaining open elements
    if in_list or in_ordered_list:
        html_parts.append(close_lists())
    if in_table:
        html_parts.append('</table>')
    
    return '\n'.join(html_parts)


def create_page(md_content, title, output_file):
    """Create a full HTML page from markdown content."""
    body_html = md_to_html(md_content, title)
    
    page = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AI 커머스 브레인</title>
    <meta name="description" content="{title} - 이커머스 셀러를 위한 실전 가이드">
{CSS}
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← 가이드 목록으로 돌아가기</a>
        <span class="badge">AI 커머스 브레인</span>
        
        {body_html}

        <div class="cta-box">
            <h2>🚀 더 많은 AI 활용법이 궁금하다면?</h2>
            <p>AI로 이커머스 자동화하고, 생산성 10배 올리는 실전 노하우를 공유합니다.</p>
            <div class="cta-buttons">
                <a href="https://www.youtube.com/@aiebrain" target="_blank" class="btn btn-yt">▶ 유튜브 구독하기</a>
                <a href="https://pf.kakao.com/_DIiBn" target="_blank" class="btn btn-kakao">💬 카카오 채널</a>
                <a href="https://aiebrain.lovable.app/" target="_blank" class="btn btn-site">🌐 포트폴리오 보기</a>
            </div>
        </div>

        <footer>
            <p>© 2026 <a href="https://www.youtube.com/@aiebrain" target="_blank">AI 커머스 브레인</a></p>
        </footer>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"Created: {output_file}")


if __name__ == '__main__':
    base_dir = r'C:\Users\aibra\projects\openclaw-claudecode-guide'
    guides_dir = r'C:\Users\aibra\obsidian\Guides'
    
    # Guide 1: AI 업무별 배치표
    with open(os.path.join(guides_dir, 'AI 업무별 배치표 - 셀러를 위한 완전 가이드.md'), 'r', encoding='utf-8') as f:
        md1 = f.read()
    create_page(md1, 'AI 업무별 배치표 — 이커머스 셀러 완전 가이드', os.path.join(base_dir, 'ai-task-guide.html'))
    
    # Guide 2: Cafe24 자사몰 셋팅
    with open(os.path.join(guides_dir, 'Cafe24 자사몰 셋팅 완전 가이드.md'), 'r', encoding='utf-8') as f:
        md2 = f.read()
    create_page(md2, 'Cafe24 자사몰 셋팅 완전 가이드', os.path.join(base_dir, 'cafe24-guide.html'))
    
    # Guide 3: AI 자사몰 구축
    with open(os.path.join(guides_dir, 'AI 자사몰 구축 완전 가이드 (초보자용).md'), 'r', encoding='utf-8') as f:
        md3 = f.read()
    create_page(md3, 'AI 자사몰 구축 완전 가이드 (초보자용)', os.path.join(base_dir, 'ai-store-guide.html'))
    
    print("All 3 guides converted!")
