# CSS Organization Best Practices

This guide covers proven patterns for organizing CSS in web projects.

## Core Principles

1. **Separation of Concerns**: Group styles by purpose, not by page
2. **Modularity**: Each file should have a single, clear responsibility
3. **Scalability**: Structure should grow gracefully with project size
4. **Maintainability**: Easy to find and modify styles

## File Organization Patterns

### Pattern 1: Layer-Based (ITCSS-inspired)

Organize CSS by specificity and reach:

```
styles/
├── 01-settings/      # Variables, config
│   └── variables.css
├── 02-base/          # Resets, element defaults
│   ├── reset.css
│   └── typography.css
├── 03-layout/        # Page structure
│   ├── grid.css
│   └── containers.css
├── 04-components/    # Reusable UI pieces
│   ├── button.css
│   ├── card.css
│   └── modal.css
└── 05-utilities/     # Helper classes
    └── utilities.css
```

**When to use**: Medium to large projects, teams, design systems

### Pattern 2: Component-Based

Organize by UI component:

```
styles/
├── base.css          # Variables, resets, typography
├── layout.css        # Grid, containers
├── components/
│   ├── header.css
│   ├── navigation.css
│   ├── card.css
│   ├── button.css
│   └── footer.css
└── utilities.css     # Helpers
```

**When to use**: Component-driven projects, React/Vue apps

### Pattern 3: Feature-Based

Organize by application feature:

```
styles/
├── base/
│   ├── variables.css
│   └── reset.css
├── features/
│   ├── auth/
│   │   ├── login.css
│   │   └── register.css
│   ├── dashboard/
│   │   └── dashboard.css
│   └── profile/
│       └── profile.css
└── shared/
    └── components.css
```

**When to use**: Large applications with distinct features

## File Content Guidelines

### variables.css (Settings)
```css
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-secondary: #8b5cf6;
  --color-text: #1f2937;
  --color-bg: #ffffff;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  
  /* Typography */
  --font-base: system-ui, sans-serif;
  --font-mono: 'Courier New', monospace;
  
  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
}
```

### reset.css (Base)
```css
/* Modern CSS reset */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}
```

### button.css (Component)
```css
/* Single component per file */
.btn {
  display: inline-block;
  padding: var(--space-sm) var(--space-md);
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn--primary {
  background: var(--color-primary);
  color: white;
}

.btn--secondary {
  background: var(--color-secondary);
  color: white;
}

.btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}
```

## Naming Conventions

### BEM (Block Element Modifier)
```css
/* Block */
.card { }

/* Element */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier */
.card--featured { }
.card--large { }
```

**Benefits**: Clear relationships, avoids conflicts, self-documenting

### Utility Classes
```css
/* Spacing */
.mt-1 { margin-top: var(--space-xs); }
.p-2 { padding: var(--space-sm); }

/* Display */
.flex { display: flex; }
.grid { display: grid; }

/* Text */
.text-center { text-align: center; }
.font-bold { font-weight: bold; }
```

**Use sparingly**: For common patterns, not one-off styles

## Import Order

In your main CSS file:

```css
/* 1. Settings */
@import 'settings/variables.css';

/* 2. Base */
@import 'base/reset.css';
@import 'base/typography.css';

/* 3. Layout */
@import 'layout/grid.css';
@import 'layout/containers.css';

/* 4. Components (alphabetical) */
@import 'components/button.css';
@import 'components/card.css';
@import 'components/modal.css';

/* 5. Utilities (last - highest specificity) */
@import 'utilities/utilities.css';
```

## Common Anti-Patterns

❌ **Single monolithic file**
```
styles.css (2000+ lines)
```

❌ **Page-specific files**
```
home.css
about.css
contact.css
```
*Problem*: Duplicated styles, hard to maintain

❌ **Deep nesting**
```css
.header .nav .menu .item .link { }
```
*Problem*: High specificity, hard to override

❌ **Inline styles everywhere**
```html
<div style="color: red; margin: 10px;">
```
*Problem*: Not reusable, hard to maintain

## Best Practices

✅ **One component per file** (for component styles)
✅ **Use CSS variables** for theming and consistency
✅ **Keep specificity low** (avoid deep nesting)
✅ **Group related styles** together
✅ **Use meaningful names** (descriptive, not presentational)
✅ **Comment complex sections** (but code should be self-documenting)
✅ **Mobile-first** responsive design

## Quick Decision Guide

**Small project (<5 pages, <500 lines CSS)**:
```
styles/
├── base.css
├── components.css
└── utilities.css
```

**Medium project (5-20 pages, 500-2000 lines)**:
```
styles/
├── base.css
├── layout.css
├── components/
│   └── [multiple files]
└── utilities.css
```

**Large project (20+ pages, 2000+ lines)**:
Use layer-based or feature-based organization with proper architecture (ITCSS, SMACSS)
