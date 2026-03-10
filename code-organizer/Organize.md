---
name: code-organizer
description: Comprehensive guidance for organizing code structure in web development projects. Use when users need help with: (1) Splitting monolithic CSS/JS files into smaller modules, (2) Organizing project file structure, (3) Refactoring poorly organized code, (4) Learning best practices for code organization, (5) Setting up new projects with proper structure, (6) Improving code maintainability and scalability. Provides analysis tools, organizational patterns, naming conventions, and practical examples for CSS, JavaScript, and HTML projects.
---

# Code Organizer

This skill helps organize code structure and enforce best practices for file organization in web development projects.

## Quick Start

### 1. Assess Current Structure

Run the analysis script to identify organizational issues:

```bash
python scripts/analyze_structure.py <project_path>
```

This will:
- Count files by type
- Identify monolithic files (too large)
- Detect single-file projects
- Provide specific recommendations

### 2. Analyze Large Files

For specific CSS or JS files that need splitting:

```bash
python scripts/split_files.py <file_path>
```

This will:
- Identify logical split points
- Suggest file organization
- Recommend grouping strategies

### 3. Choose Organization Pattern

Based on project size:

- **Small (<1000 lines)**: Basic organized structure
- **Medium (1000-5000 lines)**: Type-based or component-based
- **Large (5000+ lines)**: Feature-based or layer-based

See [references/project_structures.md](references/project_structures.md) for detailed patterns.

## Common Scenarios

### Scenario 1: Single Monolithic CSS File

**Problem**: All styles in one `styles.css` (1000+ lines)

**Solution**:
1. Run `python scripts/split_files.py styles.css`
2. Create directory structure:
   ```
   css/
   ├── base.css          (variables, resets, typography)
   ├── layout.css        (grid, containers, spacing)
   ├── components/       (one file per component)
   │   ├── button.css
   │   ├── card.css
   │   └── modal.css
   └── utilities.css     (helper classes)
   ```
3. Split content by purpose
4. Update HTML to import all files

**Reference**: [references/css_organization.md](references/css_organization.md)

### Scenario 2: Single Monolithic JS File

**Problem**: All JavaScript in one `script.js` (800+ lines)

**Solution**:
1. Run `python scripts/split_files.py script.js`
2. Create directory structure:
   ```
   js/
   ├── utils/            (helper functions)
   ├── components/       (UI components)
   ├── services/         (API calls, data)
   └── main.js           (initialization)
   ```
3. Extract functions into modules
4. Use ES6 imports/exports
5. Update HTML to use `type="module"`

**Reference**: [references/js_organization.md](references/js_organization.md)

### Scenario 3: Poorly Organized Project

**Problem**: Files scattered, inconsistent naming, unclear structure

**Solution**:
1. Run `python scripts/analyze_structure.py .`
2. Review recommendations
3. Choose appropriate structure from [references/project_structures.md](references/project_structures.md)
4. Create new directory structure
5. Move files systematically
6. Update all references
7. Test thoroughly

### Scenario 4: Starting New Project

**Problem**: Need to set up proper structure from the start

**Solution**:
1. Use template from `assets/templates/organized-example/`
2. Adapt to project needs
3. Follow naming conventions from [references/file_naming.md](references/file_naming.md)
4. Start with simple structure, grow as needed

## Decision Tree

```
Is the project new?
├─ Yes → Use template structure
└─ No → Run analyze_structure.py
    ├─ Issues found?
    │   ├─ Large files → Run split_files.py
    │   └─ Poor structure → Choose pattern from project_structures.md
    └─ No issues → Continue with current structure
```

## Key Principles

1. **Separation of Concerns**: Group by purpose, not by page
2. **Modularity**: One responsibility per file
3. **Scalability**: Structure grows with project
4. **Consistency**: Follow conventions throughout
5. **Discoverability**: Easy to find and understand code

## Common Anti-Patterns to Avoid

❌ **Single monolithic file** (all CSS/JS in one file)
❌ **Page-specific files** (home.css, about.css) - leads to duplication
❌ **Inconsistent naming** (Button.js, user-profile.js, contactForm.js)
❌ **Deep nesting** (>4 levels deep)
❌ **Generic names** (utils.js, helpers.js, misc.js without specificity)
❌ **Mixing concerns** (UI + logic + data in one file)

## Best Practices

✅ **Start simple, grow as needed** - Don't over-engineer small projects
✅ **Group related files together** - Colocation improves maintainability
✅ **Use consistent naming** - Follow conventions from file_naming.md
✅ **Separate concerns** - UI, logic, and data in different files
✅ **One component per file** - Makes code easier to find and test
✅ **Use meaningful names** - Descriptive, not abbreviated
✅ **Document structure** - Add README explaining organization

## Reference Files

For detailed guidance, see:

- **[references/css_organization.md](references/css_organization.md)**: CSS architecture patterns (BEM, ITCSS, SMACSS), file splitting strategies, naming conventions, import order
- **[references/js_organization.md](references/js_organization.md)**: JavaScript module patterns, file organization, dependency management, best practices
- **[references/file_naming.md](references/file_naming.md)**: Naming conventions for files and directories, case styles, framework-specific patterns
- **[references/project_structures.md](references/project_structures.md)**: Complete project layouts for different sizes and frameworks, migration paths

## Example Template

A complete example of a well-organized project is available in:
`assets/templates/organized-example/`

This includes:
- Proper HTML structure with organized imports
- CSS split into base, layout, and components
- JavaScript organized into utils, components, and main
- Demonstrates ES6 modules and proper separation

## Workflow

1. **Analyze**: Run analysis scripts to understand current state
2. **Plan**: Choose appropriate organization pattern
3. **Implement**: Create structure and move/split files
4. **Verify**: Test that everything still works
5. **Document**: Update README with structure explanation
6. **Maintain**: Keep organization consistent as project grows

## Tips for Success

- **Incremental refactoring**: Don't try to reorganize everything at once
- **Test frequently**: Ensure nothing breaks during reorganization
- **Use version control**: Commit before major restructuring
- **Update imports**: Don't forget to update all file references
- **Team alignment**: Ensure team agrees on organization pattern
- **Documentation**: Explain structure in README for future developers
