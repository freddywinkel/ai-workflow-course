# Foundation 5 — Git, a Tool for Recording File Changes Safely

**Git** is a version-control tool: it records deliberate file checkpoints and
shows how they changed. Git is its name, not an acronym.

## Outcome

You will create a local Git repository, inspect changes, make small commits, and
return to a working state with no uncommitted changes, without deleting or
publishing anything.

## Words you need first

- A **repository** is a project folder tracked by Git.
- The **working tree** is the current set of files in that repository.
- An **untracked** file exists but is not yet recorded by Git.
- A **diff** is a line-by-line view of changes.
- **Staging** selects exact changes for the next snapshot.
- A **commit** is a local recorded snapshot with a message.
- A **branch** is a named line of development.
- A **remote** is another linked repository, often online.
- A **push** sends commits to a remote.
- An **identifier (ID)** is a stable value that identifies one record, such as
  `DEC-204`.
- **PowerShell** is the Windows command shell used for the Git commands.
- **Notepad** is the Windows plain-text editor used to create the practice
  files.
- **Markdown** is a plain-text documentation format that normally uses the
  `.md` extension.
- A **synthetic** record is deliberately fictional practice data.
- `README.md` is a conventional “read me” Markdown filename for a project's
  introductory information.
- **Git metadata** is the hidden tracking information Git stores for a
  repository.
- **Git configuration** is the set of Git settings that control behaviour or
  identity.
- A **credential** is a secret value, such as a password, key, or token, that
  can grant access.
- **GitHub** is an online service that can host Git repositories. Git and
  GitHub are different; this lesson uses no GitHub account and performs no push.
- **Codex** is the artificial intelligence (AI) assistant used for the final
  read-only check. The check prompt limits it to one practice folder.

Git status or a commit does not prove that code works, data is safe, or a
release is correct. It proves only what Git recorded.

## Safety boundary

Do not use `git reset --hard`, `git clean -fd`, forced checkout, forced restore,
or forced push. Those commands can discard work. This lesson creates a new
local repository containing only synthetic Markdown files.

## Follow along — I show you exactly how

### Prerequisites and start state

- Foundations 1–4 are complete.
- Git is installed using the course setup instructions.
- `Documents\controlled-ai-course-practice` exists.
- PowerShell is closed or showing a ready prompt.

### Start or resume safely — run this at every new PowerShell session

Run this whole block whenever you start or resume Foundation 5:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonPath = Join-Path $practiceRoot "foundation-05"

if (-not (Test-Path -LiteralPath $practiceRoot -PathType Container)) {
    throw "STOP: the controlled-ai-course-practice folder is missing. Return to Foundation 1."
}
if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
    throw "STOP: foundation-05 is a file, not a folder. Do not rename or delete it; ask Codex to inspect read-only."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new foundation-05 folder."
}
else {
    "Existing foundation-05 folder found; nothing was overwritten."
}

Set-Location -LiteralPath $lessonPath
Get-Location
Get-ChildItem -Force
git --version
```

Expected result: the location ends in `foundation-05` and the final line begins
with `git version`. If existing items are listed, do not initialise, edit,
stage, or commit yet. Inspect the names and continue only when they are your
synthetic work from this lesson. At a resumed repository, run
`git status --short`, `git log --oneline -3`, and `git remote -v` before the
next unfinished step. This inspection does not change the repository. A remote
should not exist in this local-only lesson.

### Part A — create a local repository

Run this non-overwriting repository check:

```powershell
if (Test-Path -LiteralPath ".git" -PathType Container) {
    "Existing local Git repository found; git init was skipped."
    git status --short
    if (git rev-parse --verify HEAD 2>$null) {
        git log --oneline -3
    }
    else {
        "No commits recorded yet."
    }
    git remote -v
}
elseif (@(Get-ChildItem -Force).Count -eq 0) {
    git init
}
else {
    throw "STOP: this folder has files but no .git folder. Do not initialise or change it; ask Codex to inspect read-only."
}
```

What this does: for a new empty attempt, it creates hidden Git tracking
information inside this one folder. For a resumed attempt, it inspects the
existing repository instead. It does not upload anything or overwrite a file.

Expected result for a new attempt: output includes
`Initialized empty Git repository`. For a resumed attempt, Git shows the
current local status and history. If `git remote -v` prints a remote, stop and
ask Codex for read-only help; do not push.

### Part B — set a fictional identity for this practice repository

Run:

```powershell
git config user.name "Course Learner"
```

```powershell
git config user.email "course-learner@example.invalid"
```

What this does: it records a deliberately fictional commit identity only in
this repository. The reserved `.invalid` address cannot receive email.

Run:

```powershell
git config --local --list
```

Expected result: the output includes the two fictional values.

### Part C — create, inspect, stage, and commit one file

1. Run:

   ```powershell
   notepad "README.md"
   ```

2. Enter:

   ```markdown
   # Synthetic queue

   Status: new
   Contains real data: no
   ```

3. Save and close Notepad.
4. Run:

   ```powershell
   git status --short
   ```

   Expected output:

   ```text
   ?? README.md
   ```

   `??` means the file is untracked.

5. Run:

   ```powershell
   git add -- "README.md"
   ```

   What this does: it stages this one file. It does not upload or commit it.
   The `--` separates options from the file name.

6. Run:

   ```powershell
   git status --short
   ```

   Expected output:

   ```text
   A  README.md
   ```

7. Run:

   ```powershell
   git diff --staged -- "README.md"
   ```

   What this does: it shows the exact content selected for the next commit.
   Lines beginning with `+` are display markers for additions.

8. Run:

   ```powershell
   git commit -m "Add synthetic queue note"
   ```

   What this does: it creates one local snapshot.

### Part D — inspect and commit a modification

1. Run:

   ```powershell
   notepad "README.md"
   ```

2. Change only:

   ```text
   Status: new
   ```

   to:

   ```text
   Status: waiting
   ```

3. Save and close Notepad.
4. Run:

   ```powershell
   git diff -- "README.md"
   ```

   Expected result: the diff shows one line removed with `Status: new` and one
   line added with `Status: waiting`.

5. Run:

   ```powershell
   git add -- "README.md"
   ```

6. Run:

   ```powershell
   git diff --staged -- "README.md"
   ```

7. Run:

   ```powershell
   git commit -m "Update synthetic queue status"
   ```

8. Run:

   ```powershell
   git status --short
   ```

9. Run:

   ```powershell
   git log --oneline -2
   ```

10. Run:

    ```powershell
    (Get-Location).Path
    ```

    What this does: it prints the exact full repository path for the read-only
    Codex check.

### Expected result — exact

- `git status --short` prints nothing after the second commit. No output here
  means the working tree is clean.
- `git log --oneline -2` shows two commits. The newest message is
  `Update synthetic queue status`; the older message is
  `Add synthetic queue note`.
- `README.md` contains `Status: waiting`.
- Nothing was pushed or published.

### Troubleshooting

- If `git` is not recognised, stop and return to the course setup. Do not
  download Git from an advertisement or unverified package site.
- If `foundation-05` already exists, do not delete it. Enter it and run
  `git status --short` before doing anything else.
- If a commit says there is nothing to commit, inspect `git status --short` and
  the file content rather than adding random changes.
- Git may print a hint about the default branch name after `git init`. That is
  information, not a failure.

## Now recreate it yourself

In the same repository:

1. create `DECISIONS.md`;
2. give it the heading `Synthetic decision`;
3. add `Decision ID: DEC-204`;
4. add `Outcome: test again`;
5. inspect status;
6. stage only `DECISIONS.md`;
7. inspect the staged diff;
8. commit it with message `Add synthetic decision record`;
9. confirm `git status --short` prints nothing;
10. confirm `git log --oneline -3` shows three commits.

This uses a different file, record type, and commit message from the guided
example.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and its local Git metadata,
and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, stage, commit, restore, reset, clean, delete,
push, or change Git configuration. Run only read-only inspection commands such
as git status, git diff, and git log.

Report PASS or NOT YET for each criterion:
1. The folder is a local Git repository.
2. README.md contains Status: waiting and Contains real data: no.
3. DECISIONS.md contains DEC-204 and Outcome: test again.
4. The three expected commit messages exist in the correct order.
5. git status --short is empty.
6. No remote push or credential is required for this exercise.

Explain NOT YET in beginner language and make no changes.
This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] I can explain Git as a version-control tool and know its name is not an
      acronym.
- [ ] I can distinguish untracked, staged, committed, and modified.
- [ ] I inspected status and the staged diff before every commit.
- [ ] The repository contains exactly the three intended local commits.
- [ ] `git status --short` prints nothing at the end.
- [ ] I did not use a destructive Git command, remote, credential, or real
      business data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
