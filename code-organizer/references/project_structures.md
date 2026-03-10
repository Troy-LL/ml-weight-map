# Project Structure Patterns

This guide covers common project layouts for web applications.

## Choosing a Structure

Consider these factors:
- **Project size**: Lines of code, number of files
- **Team size**: Solo vs team collaboration
- **Complexity**: Simple site vs complex application
- **Framework**: Vanilla JS, React, Vue, etc.
- **Growth**: Expected future expansion

## Small Projects (<1000 lines)

### Flat Structure

Best for: Landing pages, simple sites, prototypes

```
project/
├── index.html
├── about.html
├── contact.html
├── styles.css
├── script.js
└── assets/
    ├── logo.png
    └── hero.jpg
```

**Pros**: Simple, easy to navigate
**Cons**: Doesn't scale, becomes messy quickly

### Basic Organized

Best for: Small multi-page sites

```
project/
├── index.html
├── about.html
├── contact.html
├── css/
│   ├── base.css
│   ├── layout.css
│   └── components.css
├── js/
│   ├── utils.js
│   └── main.js
└── assets/
    ├── images/
    └── fonts/
```

**Pros**: Clean separation, easy to find files
**Cons**: Still limited for complex projects

## Medium Projects (1000-5000 lines)

### Type-Based Structure

Best for: Multi-page applications, traditional websites

```
project/
├── index.html
├── pages/
│   ├── about.html
│   ├── services.html
│   └── contact.html
├── css/
│   ├── base/
│   │   ├── reset.css
│   │   └── typography.css
│   ├── layout/
│   │   ├── grid.css
│   │   └── containers.css
│   ├── components/
│   │   ├── button.css
│   │   ├── card.css
│   │   ├── modal.css
│   │   └── navigation.css
│   └── utilities/
│       └── helpers.css
├── js/
│   ├── components/
│   │   ├── Modal.js
│   │   ├── Dropdown.js
│   │   └── Carousel.js
│   ├── utils/
│   │   ├── dom.js
│   │   └── validation.js
│   ├── services/
│   │   └── api.js
│   └── main.js
└── assets/
    ├── images/
    ├── fonts/
    └── icons/
```

**Pros**: Clear organization, scales reasonably
**Cons**: Can lead to jumping between directories

### Component-Based Structure

Best for: Component-driven development, SPAs

```
project/
├── index.html
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.js
│   │   │   ├── Button.css
│   │   │   └── index.js
│   │   ├── Card/
│   │   │   ├── Card.js
│   │   │   ├── Card.css
│   │   │   └── index.js
│   │   └── Modal/
│   │       ├── Modal.js
│   │       ├── Modal.css
│   │       └── index.js
│   ├── styles/
│   │   ├── base.css
│   │   ├── layout.css
│   │   └── utilities.css
│   ├── utils/
│   │   └── helpers.js
│   └── main.js
└── assets/
    └── images/
```

**Pros**: Related files together, easy to find component code
**Cons**: More directories to navigate

## Large Projects (5000+ lines)

### Feature-Based Structure

Best for: Large applications with distinct features

```
project/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── features/
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   │   ├── LoginForm.js
│   │   │   │   └── RegisterForm.js
│   │   │   ├── services/
│   │   │   │   └── authService.js
│   │   │   ├── styles/
│   │   │   │   └── auth.css
│   │   │   └── index.js
│   │   ├── dashboard/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   ├── styles/
│   │   │   └── index.js
│   │   └── profile/
│   │       ├── components/
│   │       ├── services/
│   │       ├── styles/
│   │       └── index.js
│   ├── shared/
│   │   ├── components/
│   │   │   ├── Button/
│   │   │   └── Modal/
│   │   ├── utils/
│   │   ├── services/
│   │   └── styles/
│   ├── config/
│   │   └── constants.js
│   └── main.js
└── assets/
    └── images/
```

**Pros**: Scales well, clear feature boundaries, team-friendly
**Cons**: More complex, requires discipline

### Layer-Based Structure

Best for: Enterprise applications, clear separation of concerns

```
project/
├── public/
│   └── index.html
├── src/
│   ├── presentation/        # UI Layer
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   ├── application/         # Business Logic
│   │   ├── services/
│   │   ├── hooks/
│   │   └── state/
│   ├── domain/              # Core Logic
│   │   ├── models/
│   │   ├── entities/
│   │   └── validators/
│   ├── infrastructure/      # External Services
│   │   ├── api/
│   │   ├── storage/
│   │   └── analytics/
│   └── shared/              # Shared Utilities
│       ├── utils/
│       ├── constants/
│       └── types/
└── assets/
```

**Pros**: Clear separation, testable, professional
**Cons**: Complex, overkill for smaller projects

## Framework-Specific Structures

### React (Create React App)

```
project/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.jsx
│   │   │   ├── Button.module.css
│   │   │   └── index.js
│   │   └── Card/
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── About.jsx
│   │   └── Contact.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useLocalStorage.js
│   ├── services/
│   │   └── api.js
│   ├── utils/
│   │   └── helpers.js
│   ├── styles/
│   │   └── global.css
│   ├── App.jsx
│   └── index.js
└── package.json
```

### Vue

```
project/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── BaseButton.vue
│   │   └── TheHeader.vue
│   ├── views/
│   │   ├── Home.vue
│   │   └── About.vue
│   ├── router/
│   │   └── index.js
│   ├── store/
│   │   └── index.js
│   ├── composables/
│   │   └── useAuth.js
│   ├── assets/
│   │   └── styles/
│   ├── App.vue
│   └── main.js
└── package.json
```

### Next.js

```
project/
├── pages/
│   ├── index.js
│   ├── about.js
│   ├── api/
│   │   └── users.js
│   └── [id].js
├── components/
│   ├── Layout.jsx
│   └── Button.jsx
├── styles/
│   ├── globals.css
│   └── Home.module.css
├── public/
│   └── images/
├── lib/
│   └── api.js
└── package.json
```

## Hybrid Approach

Combine patterns for best results:

```
project/
├── public/
│   └── index.html
├── src/
│   ├── features/              # Feature-based
│   │   ├── auth/
│   │   └── dashboard/
│   ├── components/            # Shared components
│   │   ├── Button/
│   │   └── Modal/
│   ├── services/              # Layer-based
│   │   ├── api/
│   │   └── storage/
│   ├── utils/                 # Type-based
│   │   └── helpers.js
│   └── styles/
│       ├── base/
│       └── utilities/
└── assets/
```

## Common Directories Explained

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `src/` | Source code | All application code |
| `public/` | Static files | HTML, favicon, robots.txt |
| `dist/` or `build/` | Build output | Compiled/bundled files |
| `components/` | UI components | Reusable components |
| `pages/` or `views/` | Page components | Route-level components |
| `services/` | Business logic | API calls, data fetching |
| `utils/` or `helpers/` | Utilities | Pure helper functions |
| `styles/` or `css/` | Stylesheets | CSS files |
| `assets/` | Static assets | Images, fonts, icons |
| `config/` | Configuration | App configuration |
| `hooks/` | Custom hooks | React hooks |
| `store/` | State management | Redux, Vuex, etc. |
| `types/` | Type definitions | TypeScript types |
| `tests/` or `__tests__/` | Tests | Test files |

## Migration Path

### From Flat to Organized

**Before**:
```
project/
├── index.html
├── styles.css (1000 lines)
└── script.js (800 lines)
```

**After**:
```
project/
├── index.html
├── css/
│   ├── base.css
│   ├── layout.css
│   └── components.css
└── js/
    ├── utils.js
    ├── components.js
    └── main.js
```

### From Type-Based to Feature-Based

**Before**:
```
src/
├── components/
│   ├── LoginForm.js
│   ├── Dashboard.js
│   └── Profile.js
└── services/
    ├── authService.js
    └── userService.js
```

**After**:
```
src/
├── features/
│   ├── auth/
│   │   ├── LoginForm.js
│   │   └── authService.js
│   └── profile/
│       ├── Profile.js
│       └── userService.js
└── shared/
    └── components/
```

## Best Practices

✅ **Start simple, grow as needed**
✅ **Group related files together**
✅ **Use consistent naming**
✅ **Separate concerns** (UI, logic, data)
✅ **Keep shared code in shared/**
✅ **Document structure** (README.md)

## Anti-Patterns

❌ **Too many top-level directories**
❌ **Inconsistent organization**
❌ **Deep nesting** (>4 levels)
❌ **Mixing patterns** without reason
❌ **Generic names** (stuff/, misc/)

## Quick Decision Guide

**Project Size**:
- <1000 lines → Basic organized
- 1000-5000 lines → Type-based or component-based
- 5000+ lines → Feature-based or layer-based

**Team Size**:
- Solo → Simpler structure
- Team → Feature-based (clear boundaries)

**Complexity**:
- Simple site → Type-based
- Complex app → Feature-based or layer-based
