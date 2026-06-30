# Workflow: GitHub Account Switching

Use this workflow when you need to push your Product OS (or any project) to a different GitHub account (e.g., from Work to Personal).

## 1. Add the New Repository
First, create a new repository on your target GitHub account. Then, add it as a new remote in your terminal:

```bash
# Add the new remote (replace with your actual URL)
git remote add personal git@github.com:[YOUR-NEW-ACCOUNT]/[REPO-NAME].git
```

## 2. Push Your Code
Push your `main` branch to the new remote:

```bash
git push -u personal main
```

## 3. Manage Multiple Accounts (SSH Config)
If you use SSH and have different keys for work and personal accounts, edit your `~/.ssh/config`:

```text
# Work Account ([Your Company])
Host github.com-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_work

# Personal Account
Host github.com-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_personal
```

Then, you can add your remote using the alias:
```bash
git remote add personal git@github.com-personal:[YOUR-ACCOUNT]/[REPO-NAME].git
```

## 4. Verify
Check your remotes to ensure everything is mapped correctly:
```bash
git remote -v
```
