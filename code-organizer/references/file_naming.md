# File and Directory Naming Conventions

Consistent naming makes code easier to navigate and understand.

## General Principles

1. **Be Descriptive**: Names should clearly indicate purpose
2. **Be Consistent**: Use the same pattern throughout the project
3. **Be Conventional**: Follow language/framework standards
4. **Avoid Abbreviations**: Unless widely understood (API, HTTP, URL)

## File Naming Patterns

### Web Files (HTML, CSS, JS)

**HTML Files**: kebab-case
```
index.html
about-us.html
contact-form.html
privacy-policy.html
```

**CSS Files**: kebab-case
```
styles.css
base.css
button.css
user-profile.css
responsive-grid.css
```

**JavaScript Files**: Depends on content
- **Utilities/Services**: camelCase
  ```
  validation.js
  apiService.js
  localStorage.js
  ```
- **Components/Classes**: PascalCase
  ```
  Button.js
  UserProfile.js
  Modal.js
  ```
- **Entry points**: lowercase
  ```
  main.js
  index.js
  app.js
  ```

### Special File Types

**Configuration**: lowercase or kebab-case
```
config.js
.env
package.json
webpack.config.js
```

**Test Files**: Match source + suffix
```
validation.js → validation.test.js
Button.js → Button.spec.js
```

**Type Definitions**: Match source + suffix
```
api.js → api.d.ts
types.ts
```

## Directory Naming

### General Guidelines

**Plural for collections**:
```
components/
utils/
services/
assets/
```

**Singular for single-purpose**:
```
config/
public/
build/
```

**kebab-case for multi-word**:
```
user-management/
api-services/
shared-components/
```

### Common Directory Names

**Source Code**:
```
src/              # Source files
lib/              # Library code
app/              # Application code
public/           # Static assets
dist/             # Distribution/build output
build/            # Build artifacts
```

**Assets**:
```
assets/           # General assets
images/           # Image files
fonts/            # Font files
icons/            # Icon files
styles/           # CSS files
scripts/          # JavaScript files
```

**Organization**:
```
components/       # UI components
utils/            # Utility functions
helpers/          # Helper functions
services/         # Service layer
api/              # API-related code
hooks/            # Custom hooks (React)
store/            # State management
models/           # Data models
types/            # Type definitions
```

**Testing**:
```
tests/            # Test files
__tests__/        # Jest convention
spec/             # Spec files
fixtures/         # Test fixtures
mocks/            # Mock data
```

**Configuration**:
```
config/           # Configuration files
.github/          # GitHub-specific files
.vscode/          # VS Code settings
```

## Prefixes and Suffixes

### File Prefixes

**Underscore (_)**: Private/internal files
```
_helpers.js       # Internal helpers
_config.js        # Internal config
```

**Index**: Entry point for directory
```
index.js          # Main export
index.html        # Main page
```

### File Suffixes

**Purpose indicators**:
```
userService.js    # Service
apiClient.js      # Client
authHelper.js     # Helper
dateUtils.js      # Utilities
```

**Type indicators**:
```
Button.component.js
user.model.js
auth.service.js
api.controller.js
```

**Test files**:
```
validation.test.js
Button.spec.js
utils.test.ts
```

**Environment-specific**:
```
config.dev.js
config.prod.js
settings.local.js
```

## Framework-Specific Conventions

### React
```
components/
  Button/
    Button.jsx          # Component
    Button.module.css   # Scoped styles
    Button.test.jsx     # Tests
    index.js            # Re-export

hooks/
  useAuth.js
  useLocalStorage.js

pages/
  Home.jsx
  About.jsx
```

### Vue
```
components/
  BaseButton.vue        # Base components
  TheHeader.vue         # Single-instance
  UserProfile.vue       # Multi-instance

views/
  Home.vue
  Dashboard.vue

composables/
  useAuth.js
```

### Next.js
```
pages/
  index.js              # Routes
  about.js
  [id].js               # Dynamic routes

components/
  Button.jsx

public/
  favicon.ico
```

## Case Styles Reference

### kebab-case (Recommended for files)
```
user-profile.js
contact-form.html
primary-button.css
```
**Use for**: HTML, CSS, general files

### camelCase
```
userProfile.js
contactForm.js
apiService.js
```
**Use for**: JavaScript variables, functions, utility files

### PascalCase
```
UserProfile.js
ContactForm.jsx
Button.js
```
**Use for**: JavaScript classes, React components

### snake_case
```
user_profile.py
contact_form.rb
```
**Use for**: Python, Ruby files (language convention)

### UPPER_SNAKE_CASE
```
API_KEY
MAX_RETRIES
CONFIG_PATH
```
**Use for**: Constants (in code, not filenames)

## Common Patterns

### Component Files
```
Button.js             # Simple component
Button.jsx            # React component (JSX)
Button.vue            # Vue component
Button.component.js   # Explicit component marker
```

### Style Files
```
styles.css            # General styles
Button.css            # Component styles
Button.module.css     # CSS modules
_variables.scss       # Sass partial
```

### Configuration
```
config.js             # General config
.env                  # Environment variables
.eslintrc.js          # ESLint config
tsconfig.json         # TypeScript config
```

## Anti-Patterns

❌ **Inconsistent casing**:
```
UserProfile.js
user-settings.js      # Should match
contactForm.js
```

❌ **Unclear abbreviations**:
```
usrPrf.js            # What is this?
btn.js               # Spell it out: button.js
```

❌ **Generic names**:
```
utils.js             # Too broad
helpers.js           # What kind of helpers?
misc.js              # Avoid "miscellaneous"
```

❌ **Redundant naming**:
```
components/ButtonComponent.js  # "Component" is redundant
utils/utilityFunctions.js      # "Functions" is redundant
```

❌ **Special characters** (except - and _):
```
my@file.js           # Avoid
file#1.js            # Avoid
test(1).js           # Avoid
```

## Best Practices

✅ **Match framework conventions**
- React: PascalCase for components
- Vue: PascalCase for components
- Node: camelCase for modules

✅ **Be descriptive, not clever**
```
userAuthentication.js  ✅
auth.js               ✅
usrAuth.js            ❌
```

✅ **Group related files**
```
Button/
  Button.js
  Button.css
  Button.test.js
```

✅ **Use index.js for re-exports**
```javascript
// components/index.js
export { Button } from './Button/Button.js';
export { Modal } from './Modal/Modal.js';
```

✅ **Indicate file type when helpful**
```
user.model.js
api.service.js
auth.middleware.js
```

## Quick Reference

| File Type | Convention | Example |
|-----------|------------|---------|
| HTML | kebab-case | `contact-form.html` |
| CSS | kebab-case | `button-styles.css` |
| JS Utilities | camelCase | `validation.js` |
| JS Components | PascalCase | `Button.js` |
| Directories | kebab-case | `user-profile/` |
| Constants | UPPER_SNAKE | `API_KEY` |
| Test Files | source + .test | `Button.test.js` |

## Decision Tree

**Naming a file?**
1. Is it a component/class? → PascalCase
2. Is it HTML/CSS? → kebab-case
3. Is it a utility/service? → camelCase
4. Is it a config? → lowercase or kebab-case

**Naming a directory?**
1. Does it contain multiple items? → plural (components/)
2. Is it single-purpose? → singular (config/)
3. Multi-word? → kebab-case (api-services/)
