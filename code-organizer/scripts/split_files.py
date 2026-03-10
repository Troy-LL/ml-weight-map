#!/usr/bin/env python3
"""
Interactive helper for splitting large CSS/JS files into smaller, organized modules.
"""

import os
import sys
import re
from pathlib import Path


class FileSplitter:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.ext = self.file_path.suffix.lower()
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def analyze_css(self):
        """Analyze CSS file and suggest split points."""
        print(f"\nAnalyzing CSS file: {self.file_path.name}")
        print("=" * 60)
        
        # Find major sections (comments, selectors)
        sections = []
        
        # Look for comment-based sections
        comment_pattern = r'/\*\s*([^*]+?)\s*\*/'
        for match in re.finditer(comment_pattern, self.content):
            sections.append({
                'type': 'comment',
                'name': match.group(1).strip(),
                'position': match.start()
            })
        
        # Look for major selector patterns
        selector_patterns = [
            (r'\.([a-zA-Z0-9_-]+)\s*{', 'component'),
            (r'#([a-zA-Z0-9_-]+)\s*{', 'id'),
            (r':root\s*{', 'variables'),
            (r'@media', 'media-query'),
        ]
        
        for pattern, section_type in selector_patterns:
            for match in re.finditer(pattern, self.content):
                name = match.group(1) if match.lastindex else section_type
                sections.append({
                    'type': section_type,
                    'name': name,
                    'position': match.start()
                })
        
        sections.sort(key=lambda x: x['position'])
        
        print(f"\nFound {len(sections)} potential sections:\n")
        for i, section in enumerate(sections[:20], 1):  # Show first 20
            print(f"{i:2}. {section['type']:15} | {section['name']}")
        
        if len(sections) > 20:
            print(f"... and {len(sections) - 20} more")
        
        self._suggest_css_organization(sections)
    
    def analyze_js(self):
        """Analyze JavaScript file and suggest split points."""
        print(f"\nAnalyzing JavaScript file: {self.file_path.name}")
        print("=" * 60)
        
        # Find functions, classes, and major blocks
        sections = []
        
        # Function declarations
        func_pattern = r'function\s+([a-zA-Z0-9_]+)\s*\('
        for match in re.finditer(func_pattern, self.content):
            sections.append({
                'type': 'function',
                'name': match.group(1),
                'position': match.start()
            })
        
        # Arrow functions assigned to variables
        arrow_pattern = r'(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>'
        for match in re.finditer(arrow_pattern, self.content):
            sections.append({
                'type': 'arrow-function',
                'name': match.group(1),
                'position': match.start()
            })
        
        # Class declarations
        class_pattern = r'class\s+([a-zA-Z0-9_]+)'
        for match in re.finditer(class_pattern, self.content):
            sections.append({
                'type': 'class',
                'name': match.group(1),
                'position': match.start()
            })
        
        # Event listeners (common pattern)
        event_pattern = r'addEventListener\([\'"]([a-zA-Z0-9_-]+)'
        for match in re.finditer(event_pattern, self.content):
            sections.append({
                'type': 'event-listener',
                'name': match.group(1),
                'position': match.start()
            })
        
        sections.sort(key=lambda x: x['position'])
        
        print(f"\nFound {len(sections)} code sections:\n")
        for i, section in enumerate(sections[:20], 1):
            print(f"{i:2}. {section['type']:20} | {section['name']}")
        
        if len(sections) > 20:
            print(f"... and {len(sections) - 20} more")
        
        self._suggest_js_organization(sections)
    
    def _suggest_css_organization(self, sections):
        """Suggest CSS file organization."""
        print("\n" + "=" * 60)
        print("SUGGESTED ORGANIZATION")
        print("=" * 60)
        
        print("\nRecommended file structure:")
        print("  styles/")
        print("    ├── base.css          (resets, variables, typography)")
        print("    ├── layout.css        (grid, containers, spacing)")
        print("    ├── components/")
        print("    │   ├── button.css")
        print("    │   ├── card.css")
        print("    │   └── [component].css")
        print("    └── utilities.css     (helper classes)")
        
        print("\nSuggested groupings:")
        
        # Group by type
        by_type = {}
        for section in sections:
            section_type = section['type']
            if section_type not in by_type:
                by_type[section_type] = []
            by_type[section_type].append(section['name'])
        
        if 'variables' in by_type or any(':root' in s['name'] for s in sections):
            print("  • base.css: CSS variables, resets, typography")
        
        if 'component' in by_type:
            print(f"  • components/: {len(by_type['component'])} component styles")
        
        if 'media-query' in by_type:
            print("  • Consider: responsive.css for media queries")
    
    def _suggest_js_organization(self, sections):
        """Suggest JavaScript file organization."""
        print("\n" + "=" * 60)
        print("SUGGESTED ORGANIZATION")
        print("=" * 60)
        
        print("\nRecommended file structure:")
        print("  js/")
        print("    ├── utils/")
        print("    │   └── helpers.js    (utility functions)")
        print("    ├── components/")
        print("    │   └── [component].js")
        print("    ├── services/")
        print("    │   └── api.js        (data fetching)")
        print("    └── main.js           (initialization)")
        
        print("\nSuggested groupings:")
        
        # Categorize functions
        by_type = {}
        for section in sections:
            section_type = section['type']
            if section_type not in by_type:
                by_type[section_type] = []
            by_type[section_type].append(section['name'])
        
        if 'function' in by_type or 'arrow-function' in by_type:
            total_funcs = len(by_type.get('function', [])) + len(by_type.get('arrow-function', []))
            print(f"  • utils/: {total_funcs} functions (group by purpose)")
        
        if 'class' in by_type:
            print(f"  • components/: {len(by_type['class'])} classes")
        
        if 'event-listener' in by_type:
            print(f"  • Consider: events.js for {len(by_type['event-listener'])} event handlers")
    
    def run(self):
        """Run the analysis based on file type."""
        if self.ext == '.css':
            self.analyze_css()
        elif self.ext in {'.js', '.jsx'}:
            self.analyze_js()
        else:
            print(f"Unsupported file type: {self.ext}")
            print("Supported types: .css, .js, .jsx")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("Next steps:")
        print("  1. Create the suggested directory structure")
        print("  2. Move related code into separate files")
        print("  3. Update import/link statements")
        print("  4. Test to ensure everything still works")
        print("=" * 60 + "\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python split_files.py <file_path>")
        print("\nExample:")
        print("  python split_files.py styles.css")
        print("  python split_files.py script.js")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        splitter = FileSplitter(file_path)
        splitter.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
