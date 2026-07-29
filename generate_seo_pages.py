import json
import os

os.makedirs("blog/en", exist_ok=True)
os.makedirs("blog/ar", exist_ok=True)
os.makedirs("blog/fr", exist_ok=True)

with open("batteries.json", "r", encoding="utf-8") as f: batteries = json.load(f)
with open("compatibilities.json", "r", encoding="utf-8") as f: compatibilities = json.load(f)
with open("lcds.json", "r", encoding="utf-8") as f: lcds = json.load(f)

# Read components using "{base}" placeholder
with open("components/head.html", "r", encoding="utf-8") as f: head_raw = f.read()
with open("components/header.html", "r", encoding="utf-8") as f: header_raw = f.read()
with open("components/footer.html", "r", encoding="utf-8") as f: footer_raw = f.read()

all_items = []
for b in batteries: all_items.append({"ref": b.get("battery_ref"), "type": "Battery", "models": [m["brand"] + " " + m["model"] for m in b.get("compatible_models", [])]})
for s in compatibilities: all_items.append({"ref": s.get("screen_ref"), "type": "Screen", "models": [m["brand"] + " " + m["model"] for m in s.get("compatible_models", [])]})
for l in lcds: all_items.append({"ref": l.get("lcd_ref"), "type": "Screen", "models": [m["brand"] + " " + m["model"] for m in l.get("compatible_models", [])]})

translations = {
    "en": {
        "dir": "ltr",
        "Screen": "Screen", "Battery": "Battery",
        "title": "{ref} {part} Compatibility List & Cross Reference",
        "desc": "Discover all mobile phones compatible with the {ref} {part}. Complete cross-reference list for repair technicians to save on inventory.",
        "p1": "If you are a mobile repair technician or a DIY enthusiast looking for information about the <strong>{ref} {part}</strong>, you have come to the right place.",
        "p2": "The <strong>{ref}</strong> is a highly sought-after component in the mobile repair industry. Instead of buying specific parts for every single smartphone model, you can use the {ref} {part} across multiple devices seamlessly.",
        "h2_1": "List of Compatible Phones for {ref}",
        "p3": "Below is the complete, verified list of mobile phone models that are 100% compatible with the {ref} {part}.",
        "h2_2": "Why Use Our Cross-Reference Engine?",
        "p4": "The <em>Mobile Parts Matrix</em> is the largest independent database for mobile technicians. It is built specifically for wholesale buyers and repair shops.",
        "cta_title": "Want to search for more parts or phone models?",
        "cta_btn": "🔍 Launch Interactive Parts Search",
        "index_title": "All Compatibility Articles",
        "q_match": "Does the {ref} {part} fit the {model}?",
        "a_match": "Yes, the {ref} {part} is fully compatible with the {model}."
    },
    "ar": {
        "dir": "rtl",
        "Screen": "شاشة", "Battery": "بطارية",
        "title": "دليل توافق {part} {ref} للأجهزة",
        "desc": "اكتشف جميع الهواتف المتوافقة مع {part} {ref}. الدليل الشامل لفنيي الصيانة لتقليل تكلفة المخزون.",
        "p1": "إذا كنت فني صيانة هواتف ذكية وتبحث عن توافقات <strong>{part} {ref}</strong>، فأنت في المكان الصحيح.",
        "p2": "تعتبر قطعة <strong>{ref}</strong> من القطع المطلوبة بكثرة. بدلاً من شراء قطعة خاصة لكل هاتف، يمكنك استخدام نفس القطعة لعدة هواتف بكل كفاءة.",
        "h2_1": "قائمة الهواتف المتوافقة مع {ref}",
        "p3": "فيما يلي القائمة الكاملة والمؤكدة للهواتف التي تتوافق بنسبة 100% مع {part} {ref}.",
        "h2_2": "لماذا تستخدم موسوعتنا؟",
        "p4": "تعد (موسوعة توافق القطع) أكبر قاعدة بيانات مستقلة للفنيين، مصممة لتجار الجملة ومحلات الصيانة.",
        "cta_title": "هل تريد البحث عن قطع أو هواتف أخرى؟",
        "cta_btn": "🔍 افتح محرك البحث الذكي",
        "index_title": "جميع مقالات التوافق",
        "q_match": "هل {part} {ref} يركب على هاتف {model}؟",
        "a_match": "نعم، {part} {ref} متوافق تماماً مع {model}."
    },
    "fr": {
        "dir": "ltr",
        "Screen": "Écran", "Battery": "Batterie",
        "title": "Liste de compatibilité {part} {ref}",
        "desc": "Découvrez tous les téléphones compatibles avec {part} {ref}. Guide complet pour les techniciens de réparation.",
        "p1": "Si vous êtes technicien de réparation et que vous cherchez des informations sur <strong>{part} {ref}</strong>, vous êtes au bon endroit.",
        "p2": "La pièce <strong>{ref}</strong> est très demandée. Au lieu d'acheter des pièces spécifiques, utilisez cette même pièce sur plusieurs téléphones.",
        "h2_1": "Liste des téléphones compatibles avec {ref}",
        "p3": "Voici la liste complète et vérifiée des téléphones 100% compatibles avec {part} {ref}.",
        "h2_2": "Pourquoi utiliser notre base de données ?",
        "p4": "Mobile Parts Matrix est la plus grande base de données indépendante conçue pour les grossistes et techniciens.",
        "cta_title": "Vous voulez chercher d'autres pièces ?",
        "cta_btn": "🔍 Lancer le moteur de recherche",
        "index_title": "Tous les articles de compatibilité",
        "q_match": "Est-ce que {part} {ref} est compatible avec {model} ?",
        "a_match": "Oui, {part} {ref} est 100% compatible avec {model}."
    }
}

template = """<!DOCTYPE html>
<html lang="{lang}" dir="{dir}">
<head>
    {head_content}
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <style>
        .article-content {{ max-width: 800px; margin: 2rem auto; line-height: 1.8; font-size: 1.1rem; padding: 2.5rem; background: var(--card-bg); border-radius: 16px; border: 1px solid var(--card-border); text-align: {align}; }}
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
            <p>{p1}</p>
            <p>{p2}</p>
            <h2 style="color: var(--accent-screen); margin: 2rem 0 1rem; font-size: 1.5rem;">{h2_1}</h2>
            <p>{p3}</p>
            <ul style="list-style: none; display: flex; flex-wrap: wrap; gap: 10px; margin-top: 1.5rem; margin-bottom: 2rem;">
                {models_html}
            </ul>
            <h2 style="color: var(--accent-battery); margin: 2rem 0 1rem; font-size: 1.5rem;">{h2_2}</h2>
            <p>{p4}</p>
            <div style="text-align: center; margin-top: 3rem; border-top: 1px solid var(--card-border); padding-top: 2rem;">
                <p style="font-size: 1.2rem; font-weight: bold;">{cta_title}</p>
                <a href="../../index.html" class="cta-button">{cta_btn}</a>
            </div>
        </article>
        {footer_content}
    </main>
</body>
</html>
"""

print("Generating MULTILINGUAL SEO articles...")
count = 0
blog_index_html = {"en": "", "ar": "", "fr": ""}

# Inject components for blog (base url is '../..')
head_blog = head_raw.replace("{base}", "../..")
header_blog = header_raw.replace("{base}", "../..")
footer_blog = footer_raw.replace("{base}", "../..")

for item in all_items:
    ref = item["ref"]
    part_type = item["type"]
    models = item["models"]
    safe_ref = str(ref).replace(" ", "_").replace("/", "_").replace("\\", "_")
    
    models_html = ""
    for model in models:
        models_html += f'<li class="model-tag" style="font-size: 1rem; padding: 0.5rem 1rem;">{model}</li>\n                '
    
    for lang, t in translations.items():
        part_translated = t[part_type]
        title = t["title"].format(ref=ref, part=part_translated)
        desc = t["desc"].format(ref=ref, part=part_translated)
        
        faq_items = []
        for model in models:
            faq_items.append({
                "@type": "Question",
                "name": t["q_match"].format(ref=ref, part=part_translated, model=model),
                "acceptedAnswer": { "@type": "Answer", "text": t["a_match"].format(ref=ref, part=part_translated, model=model) }
            })
            
        schema = { "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items[:10] }
        schema_json = json.dumps(schema, indent=8, ensure_ascii=False)
            
        filename = f"compatibility_{part_type.lower()}_{safe_ref}.html"
        
        # Add link to blog index
        blog_index_html[lang] += f'<a href="{filename}" class="result-card glass-card" style="text-decoration:none; margin-bottom: 1rem; display: block;"><h3 style="color: var(--text-main);">{title}</h3><p style="color: var(--text-muted); font-size:0.9rem;">{desc}</p></a>\n'
        
        align = "right" if t["dir"] == "rtl" else "left"
        
        with open(f"blog/{lang}/{filename}", "w", encoding="utf-8") as f:
            f.write(template.format(
                lang=lang, dir=t["dir"], align=align,
                title=title, desc=desc, p1=t["p1"].format(ref=ref, part=part_translated),
                p2=t["p2"].format(ref=ref, part=part_translated),
                h2_1=t["h2_1"].format(ref=ref), p3=t["p3"].format(ref=ref, part=part_translated),
                models_html=models_html, h2_2=t["h2_2"], p4=t["p4"],
                cta_title=t["cta_title"], cta_btn=t["cta_btn"],
                schema_json=schema_json, head_content=head_blog,
                header_content=header_blog, footer_content=footer_blog
            ))
        count += 1

# Generate blog/index.html for each lang
index_template_str = """<!DOCTYPE html>
<html lang="{lang}" dir="{dir}">
<head>
    {head_content}
    <title>{title}</title>
</head>
<body>
    <div class="background-effects"><div class="glow glow-1"></div><div class="glow glow-2"></div></div>
    <main class="container">
        {header_content}
        <div style="max-width: 1000px; margin: 0 auto;">
            <h2 style="margin-bottom: 2rem; text-align: center;">{title}</h2>
            
            <!-- Language selector for blog -->
            <div style="display:flex; justify-content:center; gap:1rem; margin-bottom: 2rem;">
                <a href="../ar/index.html" class="filter-btn">العربية</a>
                <a href="../en/index.html" class="filter-btn">English</a>
                <a href="../fr/index.html" class="filter-btn">Français</a>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem;">
                {blog_html}
            </div>
        </div>
        {footer_content}
    </main>
</body>
</html>"""

for lang, t in translations.items():
    with open(f"blog/{lang}/index.html", "w", encoding="utf-8") as f:
        f.write(index_template_str.format(
            lang=lang, dir=t["dir"], title=t["index_title"],
            blog_html=blog_index_html[lang], head_content=head_blog,
            header_content=header_blog, footer_content=footer_blog
        ))
        
# Generate root blog index (redirect to ar)
with open("blog/index.html", "w", encoding="utf-8") as f:
    f.write('<meta http-equiv="refresh" content="0; url=ar/index.html" />')

# Build Root Pages
for page in ["index.html", "about.html", "contact.html", "privacy.html"]:
    with open(f"templates/{page}", "r", encoding="utf-8") as f:
        page_content = f.read()
    
    # Inject components for root pages (base url is '.')
    head_injected = head_raw.replace('href="{base}/', 'href="').replace('"{base}"', '"."')
    header_injected = header_raw.replace('href="{base}/', 'href="').replace('"{base}"', '"."')
    footer_injected = footer_raw.replace('href="{base}/', 'href="').replace('"{base}"', '"."')
    
    page_content = page_content.replace("{head_content}", head_injected)
    page_content = page_content.replace("{header_content}", header_injected)
    page_content = page_content.replace("{footer_content}", footer_injected)
    
    with open(page, "w", encoding="utf-8") as f:
        f.write(page_content)

print(f"Successfully generated {count} MULTILINGUAL SEO articles, indices, and built root pages!")
