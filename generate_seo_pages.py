import json
import os

os.makedirs("blog", exist_ok=True)

with open("batteries.json", "r", encoding="utf-8") as f: batteries = json.load(f)
with open("compatibilities.json", "r", encoding="utf-8") as f: compatibilities = json.load(f)
with open("lcds.json", "r", encoding="utf-8") as f: lcds = json.load(f)

with open("components/head.html", "r", encoding="utf-8") as f: head_content = f.read().replace("{base}", "..")
with open("components/header.html", "r", encoding="utf-8") as f: header_content = f.read().replace("{base}", "..")
with open("components/footer.html", "r", encoding="utf-8") as f: footer_content = f.read().replace("{base}", "..")

all_items = []
for b in batteries: all_items.append({"ref": b.get("battery_ref"), "type": "Battery", "models": [m["brand"] + " " + m["model"] for m in b.get("compatible_models", [])]})
for s in compatibilities: all_items.append({"ref": s.get("screen_ref"), "type": "Screen", "models": [m["brand"] + " " + m["model"] for m in s.get("compatible_models", [])]})
for l in lcds: all_items.append({"ref": l.get("lcd_ref"), "type": "Screen", "models": [m["brand"] + " " + m["model"] for m in l.get("compatible_models", [])]})

template = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    {head_content}
    <title>{title}</title>
    <meta name="description" content="{description}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <style>
        .article-content {{ max-width: 800px; margin: 2rem auto; line-height: 1.8; font-size: 1.1rem; padding: 2.5rem; background: var(--card-bg); border-radius: 16px; border: 1px solid var(--card-border); text-align: left; }}
        .article-content p {{ margin-bottom: 1.5rem; }}
        .cta-button {{ display: inline-block; background: var(--primary); color: white; padding: 1rem 2rem; border-radius: 12px; text-decoration: none; font-weight: bold; margin-top: 2rem; transition: all 0.3s ease; box-shadow: 0 0 15px var(--primary-glow); }}
        .cta-button:hover {{ transform: translateY(-3px); box-shadow: 0 0 25px var(--primary-glow); background: #2563eb; color: white; }}
    </style>
</head>
<body>
    <div class="background-effects"><div class="glow glow-1"></div><div class="glow glow-2"></div></div>
    <main class="container">
        {header_content}
        <article class="article-content glass-card">
            <h1 class="gradient-text" style="font-size: 2rem; margin-bottom: 1.5rem;">{title}</h1>
            <p>If you are a mobile repair technician or a DIY enthusiast looking for information about the <strong>{ref} {part_type}</strong>, you have come to the right place.</p>
            <p>The <strong>{ref}</strong> is a highly sought-after {part_type_lower} in the mobile repair industry. Instead of buying specific parts for every single smartphone model, you can use the {ref} {part_type_lower} across multiple devices seamlessly.</p>
            <h2 style="color: var(--accent-screen); margin: 2rem 0 1rem; font-size: 1.5rem;">List of Compatible Phones for {ref}</h2>
            <p>Below is the complete, verified list of mobile phone models that are 100% compatible with the {ref} {part_type_lower}.</p>
            <ul style="list-style: none; display: flex; flex-wrap: wrap; gap: 10px; margin-top: 1.5rem; margin-bottom: 2rem;">
                {models_html}
            </ul>
            <h2 style="color: var(--accent-battery); margin: 2rem 0 1rem; font-size: 1.5rem;">Why Use Our Cross-Reference Engine?</h2>
            <p>The <em>Mobile Parts Matrix</em> is the largest independent database for mobile technicians. It is built specifically for wholesale buyers and repair shops.</p>
            <div style="text-align: center; margin-top: 3rem; border-top: 1px solid var(--card-border); padding-top: 2rem;">
                <p style="font-size: 1.2rem; font-weight: bold;">Want to search for more parts or phone models?</p>
                <a href="../index.html" class="cta-button">🔍 Launch Interactive Parts Search</a>
            </div>
        </article>
        {footer_content}
    </main>
</body>
</html>
"""

print("Generating rich SEO articles...")
count = 0
blog_index_html = ""

for item in all_items:
    ref = item["ref"]
    part_type = item["type"]
    part_type_lower = part_type.lower()
    models = item["models"]
    
    safe_ref = str(ref).replace(" ", "_").replace("/", "_").replace("\\", "_")
    title = f"{ref} {part_type} Compatibility List & Cross Reference"
    desc = f"Discover all mobile phones compatible with the {ref} {part_type}. Complete cross-reference list for repair technicians to save on inventory."
    
    models_html = ""
    for model in models:
        models_html += f'<li class="model-tag" style="font-size: 1rem; padding: 0.5rem 1rem;">{model}</li>\n                '
    
    faq_items = []
    for model in models:
        faq_items.append({
            "@type": "Question",
            "name": f"Does the {ref} {part_type_lower} fit the {model}?",
            "acceptedAnswer": { "@type": "Answer", "text": f"Yes, the {ref} {part_type_lower} is fully compatible with the {model}." }
        })
        
    schema = { "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items[:10] }
    schema_json = json.dumps(schema, indent=8)
        
    filename = f"compatibility_{part_type_lower}_{safe_ref}.html"
    
    # Add link to blog index
    blog_index_html += f'<a href="{filename}" class="result-card glass-card" style="text-decoration:none; margin-bottom: 1rem; display: block;"><h3 style="color: var(--text-main);">{title}</h3><p style="color: var(--text-muted); font-size:0.9rem;">{desc}</p></a>\n'
    
    with open(f"blog/{filename}", "w", encoding="utf-8") as f:
        f.write(template.format(
            title=title, description=desc, ref=ref, part_type=part_type, 
            part_type_lower=part_type_lower, models_html=models_html,
            schema_json=schema_json, head_content=head_content,
            header_content=header_content, footer_content=footer_content
        ))
    count += 1

# Generate blog/index.html
index_template = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    {head_content}
    <title>دليل المقالات - موسوعة توافق القطع</title>
</head>
<body>
    <div class="background-effects"><div class="glow glow-1"></div><div class="glow glow-2"></div></div>
    <main class="container">
        {header_content}
        <div style="max-width: 1000px; margin: 0 auto;">
            <h2 style="margin-bottom: 2rem; text-align: center;">جميع مقالات توافق القطع (دليل الشاشات والبطاريات)</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem;">
                {blog_index_html}
            </div>
        </div>
        {footer_content}
    </main>
</body>
</html>"""

with open("blog/index.html", "w", encoding="utf-8") as f:
    f.write(index_template)

# Build Root Pages
for page in ["index.html", "about.html", "contact.html", "privacy.html"]:
    with open(f"templates/{page}", "r", encoding="utf-8") as f:
        page_content = f.read()
    
    # Inject components for root pages (base url is '.')
    head_injected = head_content.replace('href="../', 'href="').replace('href="..', 'href=".')
    header_injected = header_content.replace('href="../', 'href="').replace('href="..', 'href=".')
    footer_injected = footer_content.replace('href="../', 'href="').replace('href="..', 'href=".')
    
    page_content = page_content.replace("{head_content}", head_injected)
    page_content = page_content.replace("{header_content}", header_injected)
    page_content = page_content.replace("{footer_content}", footer_injected)
    
    with open(page, "w", encoding="utf-8") as f:
        f.write(page_content)

print(f"Successfully generated {count} HIGH-QUALITY SEO articles, blog/index.html, and built root pages!")
