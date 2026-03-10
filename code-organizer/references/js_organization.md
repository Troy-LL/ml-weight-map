# JavaScript Organization Best Practices

This guide covers proven patterns for organizing JavaScript in web projects.

## Core Principles

1. **Single Responsibility**: Each file/module does one thing well
2. **Modularity**: Code is split into reusable, independent pieces
3. **Clear Dependencies**: Easy to understand what depends on what
4. **Separation of Concerns**: UI, logic, and data are separated

## File Organization Patterns

### Pattern 1: Layer-Based

Organize by technical responsibility:

```
js/
├── utils/            # Pure functions, helpers
│   ├── dom.js
│   ├── validation.js
│   └── formatting.js
├── services/         # API calls, data fetching
│   ├── api.js
│   └── storage.js
├── components/       # UI components
│   ├── Modal.js
│   ├── Dropdown.js
│   └── Carousel.js
├── state/            # State management
│   └── store.js
└── main.js           # Entry point, initialization
```

**When to use**: Medium to large projects, clear separation needed

### Pattern 2: Feature-Based

Organize by application feature:

```
js/
├── shared/
│   ├── utils.js
│   └── api.js
├── features/
│   ├── auth/
│   │   ├── login.js
│   │   ├── register.js
│   │   └── authService.js
│   ├── dashboard/
│   │   ├── dashboard.js
│   │   └── widgets.js
│   └── profile/
│       ├── profile.js
│       └── settings.js
└── main.js
```

**When to use**: Large apps with distinct features, team collaboration

### Pattern 3: Component-Based

Organize by UI component (for component frameworks):

```
js/
├── components/
│   ├── Header/
│   │   ├── Header.js
│   │   ├── Navigation.js
│   │   └── UserMenu.js
│   ├── Dashboard/
│   │   ├── Dashboard.js
│   │   ├── Widget.js
│   │   └── Chart.js
│   └── shared/
│       ├── Button.js
│       └── Modal.js
├── hooks/            # Reusable logic (React)
│   └── useAuth.js
├── services/
│   └── api.js
└── main.js
```

**When to use**: React, Vue, or other component frameworks

## Module Patterns

### ES6 Modules (Recommended)

**Export:**
```javascript
// utils/validation.js
export function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function validatePassword(password) {
  return password.length >= 8;
}

// Default export
export default function validate(data) {
  return {
    email: validateEmail(data.email),
    password: validatePassword(data.password)
  };
}
```

**Import:**
```javascript
// main.js
import validate, { validateEmail } from './utils/validation.js';

// Use named import
if (validateEmail(email)) { }

// Use default import
const isValid = validate(formData);
```

### Revealing Module Pattern (No build step)

```javascript
// components/Modal.js
const Modal = (function() {
  // Private variables
  let isOpen = false;
  
  // Private functions
  function createOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    return overlay;
  }
  
  // Public API
  return {
    open(content) {
      if (isOpen) return;
      // Implementation
      isOpen = true;
    },
    
    close() {
      if (!isOpen) return;
      // Implementation
      isOpen = false;
    },
    
    isOpen() {
      return isOpen;
    }
  };
})();
```

## File Content Guidelines

### utils/helpers.js (Utilities)
```javascript
/**
 * Pure utility functions with no side effects
 */

export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}
```

### services/api.js (Data Layer)
```javascript
/**
 * API communication layer
 * Handles all HTTP requests
 */

const API_BASE = 'https://api.example.com';

export async function fetchUser(userId) {
  const response = await fetch(`${API_BASE}/users/${userId}`);
  if (!response.ok) throw new Error('Failed to fetch user');
  return response.json();
}

export async function updateUser(userId, data) {
  const response = await fetch(`${API_BASE}/users/${userId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) throw new Error('Failed to update user');
  return response.json();
}
```

### components/Button.js (UI Component)
```javascript
/**
 * Reusable Button component
 */

export class Button {
  constructor(text, options = {}) {
    this.text = text;
    this.variant = options.variant || 'primary';
    this.onClick = options.onClick || (() => {});
    this.element = this.create();
  }
  
  create() {
    const button = document.createElement('button');
    button.className = `btn btn--${this.variant}`;
    button.textContent = this.text;
    button.addEventListener('click', this.onClick);
    return button;
  }
  
  render(container) {
    container.appendChild(this.element);
  }
  
  destroy() {
    this.element.removeEventListener('click', this.onClick);
    this.element.remove();
  }
}
```

### main.js (Entry Point)
```javascript
/**
 * Application entry point
 * Handles initialization and setup
 */

import { initAuth } from './features/auth/auth.js';
import { initDashboard } from './features/dashboard/dashboard.js';
import { setupEventListeners } from './utils/events.js';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  initAuth();
  setupEventListeners();
  
  // Route to appropriate page
  const path = window.location.pathname;
  if (path === '/dashboard') {
    initDashboard();
  }
});
```

## Import Organization

Order imports logically:

```javascript
// 1. External dependencies (if using)
import React from 'react';
import axios from 'axios';

// 2. Internal utilities
import { debounce, formatDate } from './utils/helpers.js';

// 3. Services
import { fetchUser } from './services/api.js';

// 4. Components
import { Modal } from './components/Modal.js';
import { Button } from './components/Button.js';

// 5. Styles (if applicable)
import './styles.css';
```

## Naming Conventions

### Files
- **Components**: PascalCase (`Button.js`, `UserProfile.js`)
- **Utilities**: camelCase (`validation.js`, `formatters.js`)
- **Services**: camelCase (`api.js`, `authService.js`)
- **Constants**: UPPER_SNAKE_CASE (`CONSTANTS.js`, `CONFIG.js`)

### Code
```javascript
// Classes: PascalCase
class UserManager { }

// Functions: camelCase
function fetchUserData() { }

// Constants: UPPER_SNAKE_CASE
const API_KEY = 'abc123';
const MAX_RETRIES = 3;

// Private (convention): prefix with _
function _privateHelper() { }
```

## Common Anti-Patterns

❌ **Single monolithic file**
```
script.js (3000+ lines)
```

❌ **Global variables everywhere**
```javascript
var user;
var data;
var config;
```
*Problem*: Namespace pollution, conflicts

❌ **Mixing concerns**
```javascript
// DON'T: UI + API + validation in one function
function handleSubmit() {
  const email = document.querySelector('#email').value;
  if (!email.includes('@')) alert('Invalid');
  fetch('/api/users', { method: 'POST', body: email });
}
```

❌ **Circular dependencies**
```javascript
// a.js imports b.js
// b.js imports a.js
```
*Problem*: Loading issues, hard to reason about

❌ **Deep nesting**
```javascript
function a() {
  function b() {
    function c() {
      function d() {
        // Too deep!
      }
    }
  }
}
```

## Best Practices

✅ **One module per file** (generally)
✅ **Export only what's needed** (encapsulation)
✅ **Use meaningful names** (descriptive, not abbreviated)
✅ **Group related functions** together
✅ **Separate UI from logic** (easier to test)
✅ **Handle errors properly** (try/catch, error boundaries)
✅ **Document complex logic** (JSDoc comments)
✅ **Avoid side effects** in utilities (pure functions)

## Dependency Management

### Avoid Circular Dependencies
```javascript
// ❌ BAD
// userService.js imports authService.js
// authService.js imports userService.js

// ✅ GOOD: Extract shared logic
// userService.js imports shared.js
// authService.js imports shared.js
```

### Clear Dependency Flow
```
main.js
  ├─> components/
  ├─> services/
  │     └─> utils/
  └─> utils/
```

Dependencies should flow downward, not circular.

## Quick Decision Guide

**Small project (<500 lines)**:
```
js/
├── utils.js
├── components.js
└── main.js
```

**Medium project (500-2000 lines)**:
```
js/
├── utils/
│   └── [helpers]
├── components/
│   └── [components]
├── services/
│   └── api.js
└── main.js
```

**Large project (2000+ lines)**:
Use feature-based or layer-based with proper architecture

## Testing Considerations

Organized code is easier to test:

```javascript
// utils/math.js - Easy to test (pure function)
export function add(a, b) {
  return a + b;
}

// services/api.js - Can mock HTTP calls
export async function fetchData() {
  return fetch('/api/data');
}

// components/Button.js - Can test in isolation
export class Button {
  // Component logic
}
```

Separate concerns = testable code
