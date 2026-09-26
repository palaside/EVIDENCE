import re, pathlib, sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = pathlib.Path('index.html')
raw_content = html_path.read_text(encoding='utf-8')

# Extract CSS
style_match = re.search(r'<style>(.*?)</style>', raw_content, re.DOTALL)
if not style_match:
    print("[ERROR] Could not find <style> tag in index.html")
    sys.exit(1)
css_content = style_match.group(1).strip()

# Extract JS
script_match = re.search(r'<script>(.*?)</script>', raw_content, re.DOTALL)
if not script_match:
    print("[ERROR] Could not find <script> tag in index.html")
    sys.exit(1)
js_content = script_match.group(1).strip()

# Prepare directories
css_dir = pathlib.Path('static/css')
js_dir = pathlib.Path('static/js')
css_dir.mkdir(parents=True, exist_ok=True)
js_dir.mkdir(parents=True, exist_ok=True)

# Write CSS
css_file = css_dir / 'style.css'
css_file.write_text(css_content + '\n', encoding='utf-8')
print(f"[OK] Created {css_file} ({len(css_content.splitlines())} lines, {len(css_content)/1024:.1f} KB)")

# Write JS
js_file = js_dir / 'app.js'
js_file.write_text(js_content + '\n', encoding='utf-8')
print(f"[OK] Created {js_file} ({len(js_content.splitlines())} lines, {len(js_content)/1024:.1f} KB)")

# Replace in index.html
# Replace <style>...</style> with <link rel="stylesheet" href="static/css/style.css">
modular_html = raw_content[:style_match.start()] + '<link rel="stylesheet" href="static/css/style.css">' + raw_content[style_match.end():]

# In the modified html, find the script tag and replace
script_match2 = re.search(r'<script>(.*?)</script>', modular_html, re.DOTALL)
modular_html = modular_html[:script_match2.start()] + '<script src="static/js/app.js"></script>' + modular_html[script_match2.end():]

html_path.write_text(modular_html, encoding='utf-8')
print(f"[OK] Updated index.html ({len(modular_html.splitlines())} lines, {len(modular_html)/1024:.1f} KB)")
