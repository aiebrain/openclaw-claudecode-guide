import { marked } from 'marked';
import { readFileSync, writeFileSync } from 'fs';

const template = (title, content) => `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} | AI 커머스 브레인</title>
    <style>
        :root { --bg:#0a0a0a; --card:#161616; --border:#2a2a2a; --text:#e0e0e0; --muted:#888; --accent:#4ade80; --accent2:#38bdf8; --code-bg:#1a1a2e; }
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:var(--bg); color:var(--text); line-height:1.7; }
        .container { max-width:780px; margin:0 auto; padding:2rem 1.5rem; }
        .back { display:inline-block; color:var(--accent); text-decoration:none; font-size:0.9rem; margin-bottom:1.5rem; }
        .back:hover { text-decoration:underline; }
        h1 { font-size:1.8rem; margin-bottom:0.5rem; line-height:1.3; }
        h2 { font-size:1.35rem; margin-top:2.5rem; margin-bottom:0.75rem; padding-bottom:0.4rem; border-bottom:1px solid var(--border); color:var(--accent); }
        h3 { font-size:1.1rem; margin-top:1.5rem; margin-bottom:0.5rem; }
        h4 { font-size:1rem; margin-top:1.2rem; margin-bottom:0.4rem; color:var(--accent2); }
        p { margin-bottom:0.75rem; }
        a { color:var(--accent2); }
        ul, ol { margin-bottom:0.75rem; padding-left:1.5rem; }
        li { margin-bottom:0.3rem; }
        table { width:100%; border-collapse:collapse; margin-bottom:1rem; font-size:0.9rem; }
        th, td { padding:0.5rem 0.75rem; border:1px solid var(--border); text-align:left; }
        th { background:var(--card); font-weight:600; }
        td { background:#111; }
        code { background:var(--code-bg); padding:0.15rem 0.4rem; border-radius:4px; font-size:0.88em; font-family:'SF Mono',Consolas,monospace; }
        pre { background:var(--code-bg); border:1px solid var(--border); border-radius:8px; padding:1rem; overflow-x:auto; margin-bottom:1rem; }
        pre code { background:none; padding:0; font-size:0.85rem; }
        blockquote { border-left:3px solid var(--accent); padding:0.5rem 1rem; margin:0.75rem 0; background:rgba(74,222,128,0.05); border-radius:0 8px 8px 0; }
        blockquote p { margin-bottom:0.25rem; }
        hr { border:none; border-top:1px solid var(--border); margin:2rem 0; }
        .cta-box { background:linear-gradient(135deg,#1a2e1a 0%,#162535 100%); border:1px solid var(--accent); border-radius:12px; padding:2rem; text-align:center; margin-top:2.5rem; }
        .cta-box h2 { font-size:1.3rem; margin-bottom:0.5rem; color:#fff; border:none; }
        .cta-box p { color:var(--muted); font-size:0.95rem; margin-bottom:1.25rem; }
        .cta-buttons { display:flex; gap:1rem; justify-content:center; flex-wrap:wrap; }
        .btn-cta { display:inline-block; font-weight:600; text-decoration:none; padding:0.5rem 1.25rem; border-radius:8px; font-size:0.9rem; transition:opacity 0.2s; }
        .btn-yt { background:#ff0000; color:#fff; }
        .btn-site { background:var(--accent2); color:#000; }
        .btn-cta:hover { opacity:0.85; }
        .footer { text-align:center; margin-top:3rem; padding-top:1rem; border-top:1px solid var(--border); color:var(--muted); font-size:0.85rem; }
        .footer a { color:var(--accent); text-decoration:none; }
        input[type="checkbox"] { margin-right:0.4rem; }
        @media (max-width:600px) { .container{padding:1.25rem 1rem;} h1{font-size:1.4rem;} table{font-size:0.8rem;} }
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back">← 가이드 목록으로</a>
        ${content}
        <div class="cta-box">
            <h2>🚀 더 많은 AI 활용법이 궁금하다면?</h2>
            <p>AI로 이커머스 자동화하고, 생산성 10배 올리는 실전 노하우를 공유합니다.</p>
            <div class="cta-buttons">
                <a href="https://www.youtube.com/@aiebrain" target="_blank" class="btn-cta btn-yt">▶ 유튜브 구독하기</a>
                <a href="https://aiebrain.lovable.app/" target="_blank" class="btn-cta btn-site">🌐 포트폴리오 보기</a>
            </div>
        </div>
        <div class="footer">
            <p>Made by <a href="https://github.com/aiebrain">@aiebrain</a> · <a href="https://www.youtube.com/@aiebrain">AI 커머스 브레인</a></p>
        </div>
    </div>
</body>
</html>`;

const guides = [
    {
        src: String.raw`C:\Users\aibra\obsidian\Guides\Claude Code × Antigravity 설치 가이드.md`,
        out: 'antigravity-claude-code.html',
        title: 'Google Antigravity × Claude Code 설치 가이드',
    },
    {
        src: String.raw`C:\Users\aibra\obsidian\Guides\Claude Code × OpenClaw × Obsidian 설치 가이드.md`,
        out: 'openclaw-obsidian.html',
        title: 'Claude Code × OpenClaw × Obsidian 설치 가이드',
    },
];

for (const g of guides) {
    const md = readFileSync(g.src, 'utf-8');
    // Remove obsidian-specific links like [[note]] and tags like #tag
    const cleanMd = md.replace(/\[\[([^\]]+)\]\]/g, '$1').replace(/^#\w+.*$/gm, '');
    const html = marked.parse(cleanMd);
    writeFileSync(g.out, template(g.title, html));
    console.log(`✅ ${g.out}`);
}
