#!/usr/bin/env python3
"""
Analyzes project structure and identifies organizational issues.
Provides recommendations for improving code organization.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict


class ProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.stats = defaultdict(lambda: {'count': 0, 'total_size': 0, 'files': []})
        
        # Thresholds for "large" files (in lines)
        self.thresholds = {
            '.css': 300,
            '.js': 400,
            '.html': 500,
            '.py': 500,
        }
    
    def analyze(self):
        """Run the full analysis."""
        print(f"\n{'='*60}")
        print(f"PROJECT STRUCTURE ANALYSIS")
        print(f"{'='*60}")
        print(f"Path: {self.project_path.absolute()}\n")
        
        self._scan_directory()
        self._print_summary()
        self._identify_issues()
        self._provide_recommendations()
    
    def _scan_directory(self):
        """Scan directory and collect file statistics."""
        for root, dirs, files in os.walk(self.project_path):
            # Skip common directories to ignore
            dirs[:] = [d for d in dirs if d not in {
                'node_modules', '.git', '__pycache__', 'venv', 
                '.venv', 'dist', 'build', '.next'
            }]
            
            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                
                if ext in {'.css', '.js', '.html', '.py', '.jsx', '.tsx', '.ts', '.vue'}:
                    size = self._count_lines(file_path)
                    self.stats[ext]['count'] += 1
                    self.stats[ext]['total_size'] += size
                    self.stats[ext]['files'].append({
                        'path': file_path.relative_to(self.project_path),
                        'size': size
                    })
    
    def _count_lines(self, file_path):
        """Count non-empty lines in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0
    
    def _print_summary(self):
        """Print file statistics summary."""
        print("FILE STATISTICS")
        print("-" * 60)
        
        if not self.stats:
            print("No code files found.")
            return
        
        for ext in sorted(self.stats.keys()):
            data = self.stats[ext]
            avg_size = data['total_size'] / data['count'] if data['count'] > 0 else 0
            print(f"{ext:8} | Files: {data['count']:3} | "
                  f"Total lines: {data['total_size']:5} | "
                  f"Avg: {avg_size:6.1f} lines/file")
        print()
    
    def _identify_issues(self):
        """Identify organizational issues."""
        print("IDENTIFIED ISSUES")
        print("-" * 60)
        
        issues_found = False
        
        for ext, data in self.stats.items():
            threshold = self.thresholds.get(ext, 500)
            large_files = [f for f in data['files'] if f['size'] > threshold]
            
            if large_files:
                issues_found = True
                print(f"\n⚠️  Large {ext} files (>{threshold} lines):")
                for file in sorted(large_files, key=lambda x: x['size'], reverse=True):
                    print(f"   • {file['path']} ({file['size']} lines)")
        
        # Check for single-file projects
        for ext in ['.css', '.js']:
            if ext in self.stats and self.stats[ext]['count'] == 1:
                file_size = self.stats[ext]['files'][0]['size']
                if file_size > 100:
                    issues_found = True
                    print(f"\n⚠️  Single {ext} file detected:")
                    print(f"   • {self.stats[ext]['files'][0]['path']} ({file_size} lines)")
                    print(f"   • Consider splitting into multiple files")
        
        if not issues_found:
            print("✅ No major organizational issues detected!")
        
        print()
    
    def _provide_recommendations(self):
        """Provide recommendations based on analysis."""
        print("RECOMMENDATIONS")
        print("-" * 60)
        
        recommendations = []
        
        # CSS recommendations
        if '.css' in self.stats:
            css_data = self.stats['.css']
            if css_data['count'] == 1 and css_data['total_size'] > 200:
                recommendations.append({
                    'priority': 'HIGH',
                    'type': 'CSS Organization',
                    'suggestion': 'Split CSS into multiple files:',
                    'details': [
                        '- base.css (resets, variables, typography)',
                        '- layout.css (grid, containers, spacing)',
                        '- components/ (one file per component)',
                        '- utilities.css (helper classes)'
                    ]
                })
            
            large_css = [f for f in css_data['files'] if f['size'] > 300]
            if large_css:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'type': 'CSS Files',
                    'suggestion': f'Split large CSS files ({len(large_css)} found)',
                    'details': [
                        '- Group related styles together',
                        '- Extract component-specific styles',
                        '- Consider using a CSS architecture (BEM, SMACSS)'
                    ]
                })
        
        # JS recommendations
        if '.js' in self.stats:
            js_data = self.stats['.js']
            if js_data['count'] == 1 and js_data['total_size'] > 200:
                recommendations.append({
                    'priority': 'HIGH',
                    'type': 'JS Organization',
                    'suggestion': 'Split JavaScript into modules:',
                    'details': [
                        '- utils/ (helper functions)',
                        '- components/ (UI components)',
                        '- services/ (API calls, data fetching)',
                        '- main.js (initialization)'
                    ]
                })
            
            large_js = [f for f in js_data['files'] if f['size'] > 400]
            if large_js:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'type': 'JS Files',
                    'suggestion': f'Refactor large JS files ({len(large_js)} found)',
                    'details': [
                        '- Extract functions into separate modules',
                        '- Group by feature or responsibility',
                        '- Use ES6 modules for better organization'
                    ]
                })
        
        # General recommendations
        total_files = sum(data['count'] for data in self.stats.values())
        if total_files < 5 and sum(data['total_size'] for data in self.stats.values()) > 500:
            recommendations.append({
                'priority': 'MEDIUM',
                'type': 'Project Structure',
                'suggestion': 'Consider organizing files into directories:',
                'details': [
                    '- css/ or styles/',
                    '- js/ or scripts/',
                    '- assets/ (images, fonts)',
                    '- components/ (if using components)'
                ]
            })
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. [{rec['priority']}] {rec['type']}")
                print(f"   {rec['suggestion']}")
                for detail in rec['details']:
                    print(f"   {detail}")
        else:
            print("✅ Project structure looks good!")
        
        print(f"\n{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_structure.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"Error: Path '{project_path}' does not exist.")
        sys.exit(1)
    
    analyzer = ProjectAnalyzer(project_path)
    analyzer.analyze()


if __name__ == "__main__":
    main()
