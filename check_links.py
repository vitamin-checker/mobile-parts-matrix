import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    # Exclude components folder because they use {base} placeholders
    if 'components' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

broken_links = []
href_regex = re.compile(r'href=[\'\"]([^\'\">]+)')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        links = href_regex.findall(content)
        for link in links:
            if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
                continue
            
            # Resolve relative path
            base_dir = os.path.dirname(filepath)
            target = os.path.normpath(os.path.join(base_dir, link))
            
            # Remove url parameters or fragments for file checking
            if '?' in target: target = target.split('?')[0]
            if '#' in target: target = target.split('#')[0]
            
            if not os.path.exists(target):
                broken_links.append(f'{filepath} -> {link} (Resolved to {target})')

if len(broken_links) > 0:
    print('Found broken links:')
    # Only print first 20 unique to avoid spam
    for b in list(set(broken_links))[:20]:
        print(b)
else:
    print('No broken internal links found in any of the HTML files!')
