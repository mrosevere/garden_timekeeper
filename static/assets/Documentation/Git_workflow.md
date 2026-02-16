# Cloning the Repository & Git Branching & merging Workflow

This guide explains how to clone the project, create branches, stay up to date with `main`, and contribute using pull requests.
Follow these steps to ensure a smooth, conflict‑free workflow for the whole team.

---

## Table of Contents

- [1. Cloning the Repository](#1-cloning-the-repository)
- [2. Keeping Your Local Main Branch Up to Date](#2-keeping-your-local-main-branch-up-to-date)
- [3. Creating a Feature Branch](#3-creating-a-feature-branch)
- [4. Making Changes, Committing, and Pushing](#4-making-changes-committing-and-pushing)
- [5. Opening a Pull Request (PR)](#5-opening-a-pull-request-pr)
- [6. Linking Your PR to an Issue](#6-linking-your-pr-to-an-issue)
- [7. Getting Your PR Reviewed and Merged](#7-getting-your-pr-reviewed-and-merged)
- [8. Starting New Work After a Merge](#8-starting-new-work-after-a-merge)
- [How to Resolve Merge Conflicts in VS Code](#how-to-resolve-merge-conflicts-in-vs-code)
- [Git Workflow Diagram (Text Version)](#️-git-workflow-diagram-text-version)
- [How to Write a Good Pull Request](#-how-to-write-a-good-pull-request)
- [Branch Naming Conventions](#-branch-naming-conventions)

---
## 1. Cloning the Repository

> [!IMPORTANT]
> You only need to clone the repo ONCE.
> This will create the repository on your local machine.

### HTTPS
1. Chose where you want the git project to live (e.g. C:\Users\markr\Documents\vscode-projects)
2. In a Visual Studio Code terminal, navigate to the location you have chosen;
---
    cd C:\Users\markr\Documents\vscode-projects

3. In the Visual Studio Code terminal, clone the repository onto your local machine;
---
    git clone https://github.com/mrosevere/garden_timekeeper

4. After cloning, browse to the project folder and open it in Visual Studio Code (it may automatically open for you)

---

## 2. Always start from MAIN

Before starting any new work:

    git checkout main
    git pull origin main

This ensures your base is clean and up to date.

If you get messages about untracked files such as:
 - accounts/__pycache__/...
 - core/__pycache__/...
- garden_timekeeper/__pycache__/...

Run:

    git clean -fd

And update your .gitignore folder with the files that should be ignored.
---

## 3. Create a Feature/bug Branch

To create a feature branch:

    git checkout -b feature/<feature-name>

To create a bug fix branch:

    git checkout -b bug/<issue-number>

The key is: one issue = one branch

---

## 4. Make small, atomic commits

After each logical change:

### Stage your changes

    git add .

### Commit with a meaningful message

    git commit -m "Add fire element logic"

### Update your branch from "Main" before submitting your pull request

It is possible that other developers have checked code into the "Main" branch since you started working on your branch.
Pull the latest "Main" branch down into your feature branch again so you can resolve any conflicts locally.

    git checkout your-branch-name
    git pull origin main

### Resolve any merge conflicts
If there are conflicts:
- VS Code will highlight them
- Resolve the conflicts in your branch
- Test that the site still works as expected


### Stage your merged changes again

    git add .

### Commit with a meaningful message

    git commit -m "Merged main into my branch and resolved conflicts"

### Push your branch to GitHub
Before pushing, ALWAYS check your branch:

    git branch

You should see:

    * bug/issue-118
    main

If you're not on the correct branch:

    git checkout bug/issue-118

Push to the correct branch

    git push -u origin <branchname>

After the first push, future pushes are simply:

    git push

---

## 5. Open a Pull Request (PR)

1. Go to the GitHub repository
2. Click "Compare & pull request" (or Compare: <branch -> main)
3. Review the diff
4. Fill in the PR template
5. Ensure the PR title and description match the Issue
6. Submit the PR for review

---

## 6. Linking Your PR to an Issue

In the PR description, add:

    Closes #<issue-number>

Example:

    Closes #12

This automatically links the PR to the Issue and closes it when merged.

---

## 7. Getting Your PR Reviewed and Merged

- A teammate reviews your PR
- Once approved, it can be merged into `main`
- After merging, delete your branch (GitHub will offer a button)

---

## 8. Starting New Work After a Merge

Always:

    git checkout main
    git pull origin main
    git checkout -b feature/<your-name>/<new-task>

This keeps your workflow clean and conflict‑free.

---

## How to Resolve Merge Conflicts in VS Code

When updating your branch with the latest version of `main`, you may see:

**“1 conflict remaining”**

This means Git needs you to choose which version of the code to keep.

### Step 1 — Look for the conflict markers

```
<<<<<<< HEAD
(your version)
=======
(incoming version from main)
>>>>>>> main
```

Everything between these markers is the conflict.

### Step 2 — Use the Merge Editor

VS Code shows buttons above each conflict block:

- Accept Current Change
- Accept Incoming Change
- Accept Both Changes
- Compare Changes

Choose the option that makes sense for your feature.

### Step 3 — Switch to Inline View (recommended)

1. Click the “⋯” menu at the top of the merge editor
2. Select **Switch to Inline View**

This shows the conflict in one column with clear markers.

### Step 4 — Jump directly to the conflict

Click the **“1 conflict remaining”** indicator at the top of the file.

### Step 5 — Resolve the conflict

Choose the correct version, then remove any leftover markers if needed.

### Step 6 — Save, stage, commit, and push

```bash
git add .
git commit -m "Resolve merge conflicts with main"
git push
```

Your branch is now clean and ready for review.

---

## Git Workflow Diagram (Text Version)

```
main branch
   │
   ├── Developer creates feature branch
   │       │
   │       ├── Work on feature
   │       │
   │       ├── Pull latest main into feature branch
   │       │       ├── Resolve conflicts if needed
   │       │       └── Commit + push
   │       │
   │       └── Open Pull Request
   │               ├── Code review
   │               ├── Requested changes (if any)
   │               └── Approval
   │
   └── Maintainer merges PR into main
           │
           └── GitHub Pages redeploys automatically
```

---

## How to Write a Good Pull Request

A high‑quality PR makes review faster and reduces mistakes.

### A good PR includes:

- **A clear title** describing the change
- **A short summary** of what was done
- **Why the change was needed**
- **Screenshots** if UI changes were made
- **A list of files changed** (auto‑generated by GitHub)
- **Confirmation that the branch is up to date with `main`**
- **Confirmation that the project still runs without errors**

## Branch Naming Conventions

Consistent branch names make the repo easier to navigate.

### Recommended format:

```
type/short-description
```

### Types:

- `feature/` — new features
- `fix/` — bug fixes
- `style/` — CSS or UI changes
- `docs/` — documentation updates
- `refactor/` — code improvements without new features
- `test/` — testing‑related changes

### Examples:

```
feature/add-achievements
fix/score-not-updating
style/update-button-layout
docs/add-ux-strategy
refactor/game-logic-cleanup
```

---