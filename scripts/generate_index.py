import os
import glob
import sys
import re
import shutil
import json

# Constants
REPO = os.environ.get('GITHUB_REPOSITORY', 'owner/repo')
BRANCH = os.environ.get('GITHUB_REF_NAME', 'main')

INDEX_PLACEHOLDER_LINKS = '{{ LINKS_PLACEHOLDER }}'

FOOTER_PLACEHOLDER_REPO_URL = '{{ REPO_URL }}'
FOOTER_PLACEHOLDER_SOURCE_URL = '{{ SOURCE_URL }}'
FOOTER_PLACEHOLDER_VIEW_TEXT = '{{ VIEW_TEXT }}'

LINK_PLACEHOLDER_FILENAME = '{{ FILENAME }}'
LINK_PLACEHOLDER_TITLE = '{{ TITLE }}'
LINK_PLACEHOLDER_DESCRIPTION = '{{ DESCRIPTION }}'
LINK_PLACEHOLDER_META = '{{ META_HTML }}'
LINK_PLACEHOLDER_LAST_UPDATED = '{{ LAST_UPDATED }}'

# Determine the absolute path to the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'index_template.html')
FOOTER_TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'footer_template.html')
LINK_TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'link_template.html')
OUTPUT_FILE = 'index.html'
DIST_DIR = 'dist'

def get_footer_html(filename, is_index=False):
    """Generates the footer HTML using the template."""

    # Determine the "View Source" link
    if is_index:
        # For index.html, we link to the repository root
        source_url = f"https://github.com/{REPO}"
        view_text = "Repository Root"
    else:
        # For other files, link to the specific file blob
        source_url = f"https://github.com/{REPO}/blob/{BRANCH}/{filename}"
        view_text = "View Source"

    repo_url = f"https://github.com/{REPO}"

    try:
        with open(FOOTER_TEMPLATE_PATH, "r", encoding="utf-8") as t:
            footer_html = t.read()
    except FileNotFoundError:
        print(f"Error: {FOOTER_TEMPLATE_PATH} not found.")
        sys.exit(1)

    return footer_html.replace(FOOTER_PLACEHOLDER_REPO_URL, repo_url)\
                      .replace(FOOTER_PLACEHOLDER_SOURCE_URL, source_url)\
                      .replace(FOOTER_PLACEHOLDER_VIEW_TEXT, view_text)

def remove_existing_footer(content):
    """Removes the auto-generated footer from the content if it exists."""
    # Regex to match the footer block:
    # Starts with the specific comment, matches anything (dotall), ends with </footer>
    pattern = r'\s*<!-- Auto-generated Footer -->.*</footer>'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def extract_tool_overview(content):
    """Extracts the JSON object from the TOOL_OVERVIEW block."""
    pattern = r'TOOL_OVERVIEW_START(.*?)TOOL_OVERVIEW_END'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse TOOL_OVERVIEW JSON: {e}")
            return None
    return None

def generate_meta_html(overview):
    """Generates the HTML for the meta section (functionality, dependencies)."""
    if not overview:
        return ""
    
    html = '<div class="space-y-3 mb-2">'
    
    # Functionality (displayed as tags/pills)
    if 'functionality' in overview and isinstance(overview['functionality'], dict):
        html += '<div class="flex flex-wrap gap-1">'
        for key in overview['functionality']:
            # Create a readable label from the key
            label = key.replace('_', ' ').title()
            html += f'<span class="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded-full border border-blue-100" title="{overview["functionality"][key]}">{label}</span>'
        html += '</div>'
        
    # Dependencies
    if 'dependencies' in overview and isinstance(overview['dependencies'], list):
         html += '<div class="text-xs text-gray-400">Uses: ' + ', '.join(overview['dependencies']) + '</div>'
         
    html += '</div>'
    return html

def main():
    # 0. Create dist directory
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    # 1. List HTML files in the tools directory
    html_files = glob.glob(os.path.join("tools", "*.html"))
    html_files.sort()

    # 2. Read Link Template
    try:
        with open(LINK_TEMPLATE_PATH, "r", encoding="utf-8") as t:
            link_template = t.read()
    except FileNotFoundError:
        print(f"Error: {LINK_TEMPLATE_PATH} not found.")
        sys.exit(1)

    # 3. Generate Link List
    links_html = ""
    
    for f_name in html_files:
        # Read content to extract metadata
        with open(f_name, "r", encoding="utf-8") as f:
            content = f.read()
        
        overview = extract_tool_overview(content)
        
        # Determine Title
        if overview and 'name' in overview:
            title = overview['name']
        else:
            # Use basename for title derivation if name is missing
            base_name = os.path.basename(f_name)
            title = base_name.replace("-", " ").replace("_", " ").replace(".html", "").title()
            
        # Determine Description
        description = overview['description'] if overview and 'description' in overview else "No description available."
        
        # Determine Meta HTML
        meta_html = generate_meta_html(overview)
        
        # Determine Last Updated
        last_updated = ""
        if overview and 'last_updated' in overview:
            last_updated = f'<span class="text-gray-400">Updated: {overview["last_updated"]}</span>'

        # Link directly to the file in the root of dist
        link_filename = os.path.basename(f_name)
        links_html += link_template.replace(LINK_PLACEHOLDER_FILENAME, link_filename)\
                                   .replace(LINK_PLACEHOLDER_TITLE, title)\
                                   .replace(LINK_PLACEHOLDER_DESCRIPTION, description)\
                                   .replace(LINK_PLACEHOLDER_META, meta_html)\
                                   .replace(LINK_PLACEHOLDER_LAST_UPDATED, last_updated)

    # 4. Read Index Template
    try:
        with open(INDEX_TEMPLATE_PATH, "r", encoding="utf-8") as t:
            template_content = t.read()
    except FileNotFoundError:
        print(f"Error: {INDEX_TEMPLATE_PATH} not found.")
        sys.exit(1)

    # 5. Prepare index.html content
    index_content = template_content.replace(INDEX_PLACEHOLDER_LINKS, links_html)
    
    # 6. Process all files (including generated index) and write to dist
    print(f"Processing {len(html_files) + 1} files into {DIST_DIR}...")
    
    # Process regular HTML files
    for f_name in html_files:
        with open(f_name, "r", encoding="utf-8") as f:
            content = f.read()
        
        content = remove_existing_footer(content)
        footer = get_footer_html(f_name, is_index=False)
        
        if "</body>" in content:
            parts = content.rsplit("</body>", 1)
            new_content = parts[0] + footer + "\n</body>" + parts[1]
        else:
            new_content = content + footer
        
        # Output directly to dist root
        output_filename = os.path.basename(f_name)
        output_path = os.path.join(DIST_DIR, output_filename)
        # os.makedirs(os.path.dirname(output_path), exist_ok=True) # Not needed for root
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    # Process index.html
    index_content = remove_existing_footer(index_content)
    footer = get_footer_html(OUTPUT_FILE, is_index=True)
    if "</body>" in index_content:
        parts = index_content.rsplit("</body>", 1)
        new_content = parts[0] + footer + "\n</body>" + parts[1]
    else:
        new_content = index_content + footer
        
    with open(os.path.join(DIST_DIR, OUTPUT_FILE), "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Done.")

if __name__ == "__main__":
    main()