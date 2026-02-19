# Secret Rotation & Git History Purge Workflow
A reusable guide for safely rotating secrets and removing sensitive files from Git history.

This document outlines a repeatable, safe workflow for handling leaked secrets, rotating credentials, and purging `.env` or other sensitive files from a Git repository.

---

## 1. Preparation

### Create a full backup of the repository
\`\`\`bash
cp -r project project_backup
\`\`\`

### Ensure `.env` is ignored
Add the following to `.gitignore`:
\`\`\`
.env
\`\`\`

---

## 2. Rotate All Secrets

Rotate each service one by one, updating both:

- your local `.env`
- your hosting provider’s config vars (e.g. Heroku)

Typical secrets to rotate:

- Django `SECRET_KEY`
- Email provider credentials (SendGrid, Gmail SMTP, etc.)
- Cloudinary API key and secret
- Database credentials (Heroku Postgres, Neon, ElephantSQL, etc.)
- Any third‑party API keys

Restart and test the application after each rotation.

---

## 3. Verify Database Exposure Status

Before purging history, confirm whether the database URL was ever public.

### Check GitHub Audit Log
1. Go to GitHub → Profile → Settings  
2. Security → Audit Log  
3. Search for:
   \`\`\`
   repo:<your-repo-name> visibility
   \`\`\`

If the database URL was public at any time, rotate the DB password.  
If it was never public, rotation is optional.

---

## 4. Remove `.env` From Git History

### Install `git-filter-repo`
\`\`\`bash
pip install git-filter-repo
\`\`\`

### Run the purge
From the root of the repository:
\`\`\`bash
git filter-repo --force --path .env --invert-paths
\`\`\`

This rewrites the entire commit history, removing `.env` from every commit.

### Re‑add the remote
\`\`\`bash
git remote add origin <your-repo-url>
\`\`\`

### Force‑push the cleaned history
\`\`\`bash
git push --force origin main
\`\`\`

---

## 5. Verification

On GitHub:

1. Open the earliest commit  
2. Confirm `.env` is not present  
3. Confirm no secrets appear in any commit diff  

Once verified, the repository is safe to make public.

---

## 6. Final Notes

- Never store secrets in version control  
- Always rotate secrets before a history purge  
- Always verify the purge succeeded  
- Keep this guide for future projects
