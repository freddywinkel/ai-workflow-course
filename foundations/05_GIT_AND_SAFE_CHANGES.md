# Foundation 5 — Git and Safe Change Tracking

## Outcome

You can inspect a repository, see what changed, make a small local commit, and
avoid commands that discard work or publish secrets.

## Git is not GitHub

**Git** is a local version-control tool. It records deliberate snapshots of
files and helps compare changes.

**GitHub** is an online hosting and collaboration service for Git repositories.
A local repository can exist without GitHub. A commit is local until you push
it.

Key terms:

- repository: the tracked project folder;
- working tree: the files as they currently exist;
- untracked: a new file Git is not yet tracking;
- modified: a tracked file changed since the last commit;
- staged: selected for the next commit;
- commit: a named local snapshot;
- branch: a line of development;
- diff: line-by-line change view;
- remote: an online or other linked repository;
- push: send commits to a remote.

## The safe inspection loop

From the project folder:

```powershell
git status --short
```

This reads status. Typical prefixes:

- `??`: untracked file;
- ` M`: modified but not staged;
- `M `: staged modification;
- `A `: staged new file.

Inspect changes:

```powershell
git diff
git diff --staged
```

The first shows unstaged changes; the second shows what the next commit would
contain. Lines beginning with `-` were removed and lines beginning with `+`
were added. These display markers are not literal file content.

## Your first practice repository

In the safe practice folder:

```powershell
git init
git status --short
```

Create `README.md` in your editor, then:

```powershell
git status --short
git diff
git add README.md
git diff --staged
git commit -m "Add practice README"
git status --short
```

Before `git add`, inspect the file for secrets or personal paths. Before
`git commit`, inspect the staged diff. A commit message should say what the
change does.

If Git asks for a user name/email, configure the identity you deliberately
choose for commits. Do not copy a stranger's identity from an example.

## `.gitignore`

`.gitignore` lists paths Git should normally leave untracked:

```gitignore
.env
.venv/
__pycache__/
artifacts/local/
```

Add ignore rules before creating secrets. Ignoring a file does not remove it
from old commits. If a real API key ever enters Git history:

1. stop;
2. revoke/rotate the key;
3. preserve evidence without redisplaying the value;
4. get explicit help cleaning the history.

Deleting the visible file is not enough.

## Commands that require special care

Do not run these merely because an AI assistant suggests them:

- `git reset --hard`;
- `git clean -fd`;
- `git checkout -- <file>`;
- `git restore <file>`;
- `git push --force`.

They can discard or overwrite work. Ask for a read-only diagnosis, exact
affected files, recovery route, and safer option. In this course, preserve
unexpected changes until you understand who created them.

## Git does not prove quality

A clean `git status` means no uncommitted tracked changes. It does not mean:

- tests passed;
- no secrets exist in history;
- the workflow is correct;
- the deployed version matches the commit;
- the code is understandable.

Save test evidence separately and bind releases to an exact commit ID.

## Chapter check

You pass when you can:

- explain Git versus GitHub;
- use status and both diff views;
- describe untracked, modified, staged, and committed;
- explain why `.env` must be ignored before use;
- name at least three destructive Git commands you will not run blindly.

