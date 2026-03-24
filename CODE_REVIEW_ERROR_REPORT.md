# Code Review Error Report (Post-Fix)

**Generated:** March 19, 2026  
**Scope:** All project files (excluding venv, migrations)  
**Status:** Re-run after implementing fixes from previous report

---

## Summary of Fixes Applied

1. **addCsrfMeta** — Removed (dead code).
2. **API.todayCount** — Now called in `loadTasks()` and used to update the reminder header.
3. **Null checks** — Added optional chaining and guards in login/register scripts; DOM null checks and try/catch in app.js.
4. **Duplicated code** — Extracted shared auth CSS to `static/css/auth.css`.
5. **Unused import** — Removed `BaseUserAdmin` from `tasks/admin.py`.
6. **SECRET_KEY** — Now reads from `DJANGO_SECRET_KEY` env var with dev fallback.
7. **Static paths** — Replaced hardcoded paths with `{% load static %}` and `{% static %}`.
8. **STATIC_URL** — Set to `/static/` for correct static file URLs.

---

## Checklist Results

### Issues Found: **None**

All checklist items were re-checked. No new issues were identified.

| Category | Status |
|----------|--------|
| Calling functions that don't exist | ✓ None |
| Hard coding for Gradescope | ✓ N/A |
| Missing imports | ✓ None |
| Copy-paste indentation errors | ✓ None |
| Syntax errors (semicolons) | ✓ None |
| Spelling errors (wrong file names) | ✓ Fixed |
| Wrong library version | ✓ None |
| Forgetting to upload to AFS | ✓ N/A |
| Pushing broken code into main | ✓ N/A |
| Forgetting to actually call the function | ✓ Fixed |
| Deleting a bunch of files | ✓ N/A |
| Wrong variable names | ✓ None |
| Duplicated code | ✓ Fixed |
| Accessing variable without null check | ✓ Fixed |
| Assuming array is always non-empty | ✓ None |
| Spelling variables wrongly | ✓ None |
| Mixing up variable names | ✓ None |
| Forgetting to close scope | ✓ None |
| Type mismatching (string vs int) | ✓ None |
| Making updates but forgetting elsewhere | ✓ N/A |
| Using = instead of == | ✓ None |
| Signed/unsigned int casting | ✓ N/A |
| Not accounting for floating points | ✓ N/A |
| Changing unused code | ✓ Fixed |
| Committing API keys | ✓ Fixed |
| Forgetting to free memory (C) | ✓ N/A |
| Inconsistent file naming | ✓ None |
| Out of scope functions | ✓ None |
| Using == instead of === (JS) | ✓ None |
| Falsy check vs "is not None" (Python) | ✓ None |
| Failing the linter | ✓ None |
| Committing generated build file | ✓ N/A |
| Type/pointer errors (low-level) | ✓ N/A |
| Copy-paste without adjusting variables | ✓ None |
| Duplicate files | ✓ None |
| Lack of modularity | ✓ Improved |
| Missing null checks | ✓ Fixed |
| Off-by-one errors | ✓ None |
| Missing semicolon | ✓ None |
| Poor modularization | ✓ Fixed |
| Wrong variable type | ✓ None |
| Recursion without base case | ✓ N/A |
| Wrong test case | ✓ N/A |
| Accidentally reusing variable | ✓ None |
| Forgetting to import required module | ✓ None |
| Using uninitialized variable | ✓ None |

---

## Verification

- `python manage.py check` — Passed
- Linter — No errors
- All previously reported issues addressed
