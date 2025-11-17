# Security Guidelines

## API Key Management

### ✅ What We Do (Secure)

1. **Environment Variables**: API keys are stored in `.env` files
2. **Gitignored**: All `.env` files are in `.gitignore` and won't be committed
3. **Example Files**: We provide `.env.example` as a template (without real keys)
4. **No Defaults**: Code raises an error if API key is missing (no hardcoded fallbacks)

### ❌ What to NEVER Do

1. **Never** commit `.env` files to GitHub
2. **Never** hardcode API keys in source code
3. **Never** share API keys in chat, email, or screenshots
4. **Never** commit files with real API keys

## Setup Your API Key

1. **Copy the example file:**
   ```bash
   cd apps/backend
   cp .env.example .env
   ```

2. **Get your Gemini API key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy it

3. **Add to .env file:**
   ```bash
   # Edit apps/backend/.env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Verify it's gitignored:**
   ```bash
   git status apps/backend/.env
   # Should show: nothing (file is ignored)
   ```

## Files Protected

The following files are gitignored and safe:
- `apps/backend/.env`
- `apps/backend/.env.local`
- `.env` (root level)
- `apps/backend/venv/` (Python virtual environment)

## Before Pushing to GitHub

Always check:
```bash
git status
git diff --cached
```

Make sure no `.env` files or API keys are included!

## If You Accidentally Commit an API Key

1. **Immediately revoke** the API key at https://makersuite.google.com/app/apikey
2. Generate a new API key
3. Remove the key from git history (contact your team lead)
4. Update your local `.env` with the new key
