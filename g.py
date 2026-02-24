#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 HTML 目录自动生成工具 - 美化版
运行此脚本会自动扫描 ./html 文件夹并生成美观的 index.html
"""

import os
import re
from datetime import datetime
from pathlib import Path

# ==================== 配置区域 ====================
TARGET_FOLDER = './html'          # 要扫描的文件夹
OUTPUT_FILE = 'index.html'        # 输出的索引文件
EXCLUDE_FILES = ['index.html']    # 要排除的文件名
SITE_TITLE = '📚 ALCH与小D的聊天记录'         # 网站标题
SITE_DESCRIPTION = 'ALCH的一些思考'  # 网站描述
# =================================================

def get_html_title(file_path):
    """从文件名提取标题（去掉 .html 后缀并美化）"""
    filename = os.path.basename(file_path)
    title = re.sub(r'\.html$', '', filename, flags=re.IGNORECASE)
    title = title.replace('_', ' ').replace('-', ' ').title()
    return title

def get_file_size(file_path):
    """获取文件大小（人类可读格式）"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def get_modification_time(file_path):
    """获取文件修改时间"""
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')

def scan_html_files(folder):
    """扫描文件夹中的所有 HTML 文件"""
    files = []
    if not os.path.exists(folder):
        print(f"❌ 文件夹不存在：{folder}")
        return files
    
    for filename in os.listdir(folder):
        if filename.lower().endswith('.html') and filename not in EXCLUDE_FILES:
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                files.append({
                    'path': f"./{folder}/{filename}",
                    'filename': filename,
                    'title': get_html_title(file_path),
                    'size': get_file_size(file_path),
                    'modified': get_modification_time(file_path),
                    'modified_ts': os.path.getmtime(file_path),
                    'size_bytes': os.path.getsize(file_path)
                })
    
    # 按修改时间倒序排序（最新的在前）
    files.sort(key=lambda x: x['modified_ts'], reverse=True)
    return files

def generate_html(files):
    """生成完整的 HTML 索引页面"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    files_json = str(files).replace("'", '"')
    
    # 计算总大小
    total_size_bytes = sum(f['size_bytes'] for f in files)
    total_size = get_file_size_from_bytes(total_size_bytes)
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SITE_TITLE}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #6366f1;
            --primary-light: #818cf8;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --accent: #06b6d4;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-hover: rgba(255, 255, 255, 1);
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --text-muted: #9ca3af;
            --border: rgba(0, 0, 0, 0.08);
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --radius: 16px;
            --radius-sm: 8px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-gradient);
            background-attachment: fixed;
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
            padding: 0;
            overflow-x: hidden;
        }}

        .bg-decoration {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
            z-index: 0;
        }}

        .bg-decoration::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 20s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            50% {{ transform: translate(2%, 2%) rotate(5deg); }}
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
            position: relative;
            z-index: 1;
        }}

        .header {{
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: var(--radius);
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-xl);
            border: 1px solid rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
        }}

        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 25px;
        }}

        .header h1 {{
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 0;
        }}

        .header-description {{
            color: var(--text-secondary);
            font-size: 1.1em;
            margin-top: 10px;
        }}

        .header-actions {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 10px 20px;
            border-radius: var(--radius-sm);
            border: none;
            font-size: 0.9em;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }}

        .btn-secondary {{
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
        }}

        .btn-secondary:hover {{
            background: var(--primary);
            color: white;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            padding-top: 25px;
            border-top: 1px solid var(--border);
        }}

        .stat-card {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1));
            padding: 15px 20px;
            border-radius: var(--radius-sm);
            text-align: center;
            transition: var(--transition);
        }}

        .stat-card:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow);
        }}

        .stat-value {{
            font-size: 1.8em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-label {{
            font-size: 0.85em;
            color: var(--text-secondary);
            margin-top: 5px;
        }}

        .controls {{
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: var(--radius);
            padding: 25px 30px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-lg);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}

        .search-row {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .search-box {{
            flex: 1;
            min-width: 300px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            padding: 15px 20px 15px 50px;
            font-size: 1em;
            border: 2px solid var(--border);
            border-radius: var(--radius-sm);
            outline: none;
            transition: var(--transition);
            background: white;
        }}

        .search-box input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }}

        .search-box::before {{
            content: '🔍';
            position: absolute;
            left: 18px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2em;
        }}

        .filter-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid var(--border);
        }}

        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid var(--border);
            border-radius: 20px;
            background: white;
            color: var(--text-secondary);
            font-size: 0.85em;
            cursor: pointer;
            transition: var(--transition);
            font-weight: 500;
        }}

        .filter-btn:hover {{
            border-color: var(--primary);
            color: var(--primary);
        }}

        .filter-btn.active {{
            background: var(--primary);
            border-color: var(--primary);
            color: white;
        }}

        .file-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 25px;
        }}

        .file-card {{
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: var(--radius);
            padding: 25px;
            box-shadow: var(--shadow);
            transition: var(--transition);
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            border: 1px solid rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }}

        .file-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            transform: scaleX(0);
            transition: var(--transition);
        }}

        .file-card:hover {{
            transform: translateY(-8px);
            box-shadow: var(--shadow-xl);
            border-color: rgba(99, 102, 241, 0.3);
        }}

        .file-card:hover::before {{
            transform: scaleX(1);
        }}

        .file-card .icon-wrapper {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--primary-light), var(--primary));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            margin-bottom: 15px;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
        }}

        .file-card .title {{
            font-weight: 600;
            font-size: 1.15em;
            color: var(--text-primary);
            margin-bottom: 8px;
            word-break: break-word;
            line-height: 1.4;
        }}

        .file-card .filename {{
            font-size: 0.8em;
            color: var(--text-muted);
            background: rgba(0, 0, 0, 0.04);
            padding: 6px 10px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-family: 'Consolas', 'Monaco', monospace;
            word-break: break-all;
        }}

        .file-card .meta {{
            margin-top: auto;
            padding-top: 15px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8em;
            color: var(--text-secondary);
        }}

        .file-card .meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .file-card .badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, var(--secondary), #f43f5e);
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.7em;
            font-weight: 600;
        }}

        .no-result {{
            text-align: center;
            padding: 80px 20px;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: var(--radius);
            box-shadow: var(--shadow-lg);
            display: none;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}

        .no-result .emoji {{
            font-size: 5em;
            margin-bottom: 20px;
            display: block;
            animation: bounce 2s ease-in-out infinite;
        }}

        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}

        .no-result h3 {{
            font-size: 1.5em;
            color: var(--text-primary);
            margin-bottom: 10px;
        }}

        .no-result p {{
            color: var(--text-secondary);
        }}

        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 30px;
            color: rgba(255, 255, 255, 0.9);
            background: rgba(0, 0, 0, 0.2);
            border-radius: var(--radius);
            backdrop-filter: blur(10px);
        }}

        .footer p {{
            margin: 5px 0;
            font-size: 0.9em;
        }}

        .footer .highlight {{
            color: var(--primary-light);
            font-weight: 600;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 20px 15px;
            }}

            .header {{
                padding: 25px;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .file-list {{
                grid-template-columns: 1fr;
            }}

            .search-row {{
                flex-direction: column;
            }}

            .search-box {{
                min-width: 100%;
            }}

            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
        }}

        ::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.3);
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.5);
        }}
    </style>
</head>
<body>
    <div class="bg-decoration"></div>
    
    <div class="container">
        <div class="header">
            <div class="header-top">
                <div>
                    <h1>ALCH与小D的聊天记录</h1>
                    <p class="header-description">{SITE_DESCRIPTION}</p>
                </div>
                <div class="header-actions">
                    <a href="./html/" class="btn btn-secondary" target="_blank">📂 打开文件夹</a>
                    <button class="btn btn-primary" onclick="window.location.reload()">🔄 刷新</button>
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="totalCount">{len(files)}</div>
                    <div class="stat-label">📄 文件总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_size}</div>
                    <div class="stat-label">💾 总大小</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="todayCount">0</div>
                    <div class="stat-label">🆕 今日更新</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{timestamp.split(' ')[0]}</div>
                    <div class="stat-label">🕐 生成时间</div>
                </div>
            </div>
        </div>

        <div class="controls">
            <div class="search-row">
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="搜索文件名、标题或路径..." onkeyup="filterFiles()">
                </div>
            </div>
            <div class="filter-group">
                <button class="filter-btn active" data-filter="all">全部</button>
                <button class="filter-btn" data-filter="today">今日</button>
                <button class="filter-btn" data-filter="week">本周</button>
                <button class="filter-btn" data-filter="month">本月</button>
                <button class="filter-btn" data-filter="large">大文件</button>
            </div>
        </div>

        <div class="file-list" id="fileListContainer"></div>
        
        <div class="no-result" id="noResult">
            <span class="emoji">🔍</span>
            <h3>没有找到相关文件</h3>
            <p>尝试使用其他关键词搜索，或调整筛选条件</p>
        </div>

        <div class="footer">
            <p>✨ 自动生成于 <span class="highlight">{timestamp}</span></p>
            <p>💡 提示：添加新 HTML 文件后，运行 <code class="highlight">python g.py</code> 更新目录</p>
            <p style="margin-top: 15px; opacity: 0.7;">共 {len(files)} 个文件 | 总大小 {total_size}</p>
        </div>
    </div>

    <script>
        const files = {files_json};
        
        const container = document.getElementById('fileListContainer');
        const searchInput = document.getElementById('searchInput');
        const noResult = document.getElementById('noResult');
        const totalCount = document.getElementById('totalCount');
        const todayCount = document.getElementById('todayCount');
        const filterBtns = document.querySelectorAll('.filter-btn');
        
        let currentFilter = 'all';
        let searchKeyword = '';

        function countTodayFiles() {{
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const count = files.filter(f => {{
                const fileDate = new Date(f.modified_ts * 1000);
                fileDate.setHours(0, 0, 0, 0);
                return fileDate >= today;
            }}).length;
            todayCount.textContent = count;
        }}

        function matchesTimeFilter(file, filter) {{
            const now = new Date();
            const fileDate = new Date(file.modified_ts * 1000);
            const diffDays = (now - fileDate) / (1000 * 60 * 60 * 24);
            
            switch(filter) {{
                case 'today': return diffDays < 1;
                case 'week': return diffDays < 7;
                case 'month': return diffDays < 30;
                case 'large': 
                    const sizeNum = parseFloat(file.size);
                    return file.size.includes('MB') || (file.size.includes('KB') && sizeNum > 500);
                default: return true;
            }}
        }}

        function renderFiles(fileList) {{
            container.innerHTML = '';
            
            if (fileList.length === 0) {{
                noResult.style.display = 'block';
                totalCount.textContent = '0';
                return;
            }} else {{
                noResult.style.display = 'none';
                totalCount.textContent = fileList.length;
            }}

            fileList.forEach((file, index) => {{
                const card = document.createElement('a');
                card.className = 'file-card';
                card.href = file.path;
                card.target = '_blank';
                card.style.animation = `fadeInUp 0.5s ease forwards ${{index * 0.05}}s`;
                card.style.opacity = '0';
                
                const isToday = matchesTimeFilter(file, 'today');
                const badge = isToday ? '<span class="badge">NEW</span>' : '';
                
                card.innerHTML = `
                    ${{badge}}
                    <div class="icon-wrapper">📄</div>
                    <div class="title">${{file.title}}</div>
                    <div class="filename">${{file.filename}}</div>
                    <div class="meta">
                        <span class="meta-item">💾 ${{file.size}}</span>
                        <span class="meta-item">📅 ${{file.modified}}</span>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function filterFiles() {{
            searchKeyword = searchInput.value.toLowerCase().trim();
            
            const filtered = files.filter(file => {{
                const matchesSearch = file.title.toLowerCase().includes(searchKeyword) || 
                                     file.filename.toLowerCase().includes(searchKeyword) ||
                                     file.path.toLowerCase().includes(searchKeyword);
                const matchesFilter = matchesTimeFilter(file, currentFilter);
                return matchesSearch && matchesFilter;
            }});
            
            renderFiles(filtered);
        }}

        filterBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                filterFiles();
            }});
        }});

        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        `;
        document.head.appendChild(style);

        countTodayFiles();
        renderFiles(files);
        
        console.log('📚 目录加载完成，共', files.length, '个文件');
    </script>
</body>
</html>'''
    
    return html_content

def get_file_size_from_bytes(size_bytes):
    """从字节数获取人类可读的文件大小"""
    size = size_bytes
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def main():
    print("\n" + "=" * 70)
    print("🎨 " + " " * 20 + "HTML 目录自动生成工具 - 美化版" + " " * 20)
    print("=" * 70)
    
    print(f"\n📂 扫描目录：{TARGET_FOLDER}")
    files = scan_html_files(TARGET_FOLDER)
    
    if not files:
        print("\n❌ 未找到任何 HTML 文件！")
        print(f"   请确保 {TARGET_FOLDER} 文件夹存在且包含 .html 文件")
        print("\n💡 提示：")
        print("   1️⃣  检查文件夹路径是否正确")
        print("   2️⃣  确保文件夹中有 .html 文件")
        print("   3️⃣  检查文件权限")
        return
    
    print(f"✅ 找到 {len(files)} 个 HTML 文件")
    
    # 计算总大小
    total_size_bytes = sum(f['size_bytes'] for f in files)
    total_size_str = get_file_size_from_bytes(total_size_bytes)
    print(f"📊 总文件大小：{total_size_str}")
    
    html_content = generate_html(files)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    output_size = get_file_size(OUTPUT_FILE)
    
    print(f"\n✅ 成功生成：{OUTPUT_FILE}")
    print(f"📄 生成文件大小：{output_size}")
    print(f"📈 扫描文件总数：{len(files)}")
    
    print("\n" + "=" * 70)
    print("🎉 生成完成！")
    print("=" * 70)
    print("\n💡 使用方法：")
    print("   1️⃣  双击打开 index.html 查看美观的目录页面")
    print("   2️⃣  添加新 HTML 文件后，重新运行此脚本更新")
    print("   3️⃣  支持搜索、筛选、排序等交互功能")
    print("\n🎨 页面特性：")
    print("   ✨ 渐变背景 + 毛玻璃效果")
    print("   ✨ 卡片悬停动画")
    print("   ✨ 实时搜索过滤")
    print("   ✨ 时间筛选（今日/本周/本月）")
    print("   ✨ 响应式设计（支持手机）")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()