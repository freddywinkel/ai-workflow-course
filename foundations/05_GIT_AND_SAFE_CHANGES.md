# Foundation 5 — Git, a Tool for Recording File Changes Safely

**Git** is a version-control tool: it records deliberate file checkpoints and
shows how they changed. Git is its name, not an acronym.

## Outcome

You will create a local Git repository, inspect changes, make small commits, and
return to a working state with no uncommitted changes, without deleting or
publishing anything.

## Study plan — six blocks of no more than 60 minutes

**Time label: AUTHOR ESTIMATE — NOT BEGINNER MEASURED.** The published
5–6-hour range is a planning estimate, not measured novice completion time.
Use each row as a separate study segment. Stop when the row is complete or
when 60 focused minutes have elapsed, whichever happens first. Record the last
completed part using synthetic wording, close the tools, and take a break.
Run **Start or resume safely** in every new PowerShell session; never combine
blocks.

| Block | Maximum | Work and safe stopping point |
|---:|---:|---|
| 1 | 60 minutes | Learn the Git words and safety boundary. Stop before **Follow along**. |
| 2 | 60 minutes | Run the start/resume block, decide the exact attempt state, and complete Part A. |
| 3 | 60 minutes | Complete Part B using only the fictional local identity. |
| 4 | 60 minutes | Complete Part C and stop after inspecting the first local commit. |
| 5 | 60 minutes | Complete Part D, compare the exact result, and troubleshoot only observed mismatches. |
| 6 | 60 minutes | Recreate the local history with different synthetic content, ask Codex for the bounded check, and apply every pass criterion. |

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
$lessonFolderName = "foundation-05"
if ($lessonFolderName -notmatch '^foundation-05(?:-retry-\d{2,})?$') {
    throw "STOP: use foundation-05 or a retry name created by this lesson."
}
$lessonPath = Join-Path $practiceRoot $lessonFolderName

function New-FoundationRetryAttempt {
    param([string]$BaseName, [string]$PracticeRoot)
    $retryNumber = 1
    do {
        $retryName = "$BaseName-retry-{0:D2}" -f $retryNumber
        $retryPath = Join-Path $PracticeRoot $retryName
        $retryNumber += 1
    } while (Test-Path -LiteralPath $retryPath)
    New-Item -ItemType Directory -Path $retryPath -ErrorAction Stop | Out-Null
    $retryPath
}

if (-not (Test-Path -LiteralPath $practiceRoot -PathType Container)) {
    throw "STOP: the controlled-ai-course-practice folder is missing. Return to Foundation 1."
}
if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
    throw "STOP: the selected Foundation 5 attempt is a file, not a folder. Do not change it."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new Foundation 5 attempt: $lessonFolderName"
}
else {
    "Existing Foundation 5 attempt found; nothing was overwritten: $lessonFolderName"
}

Set-Location -LiteralPath $lessonPath
Get-Location
Get-ChildItem -Force
git --version
```

Expected result: the location ends in `foundation-05` or the selected numbered
retry name, and the final line begins with `git version`. If items are listed,
do not initialise, edit, stage, configure, or commit yet.

`New-FoundationRetryAttempt` is a helper: it checks retry numbers from `01`
upward, creates only the first absent folder, and returns that new path. It does
not alter an older attempt.

### Decide the exact Git attempt state before continuing

Foundation 5 deliberately accepts only complete, clean checkpoints. This avoids
guessing which Git action was interrupted.

1. If the attempt is empty and has no `.git` folder, continue to Part A.
2. If files exist but `.git` does not, or if an unexpected item exists, do not
   initialise or inspect its content. Use a fresh retry.
3. If `.git` exists, first run:

   ```powershell
   git status --short
   git remote -v
   if (git rev-parse --verify HEAD 2>$null) {
       git log --reverse --format="%s"
   }
   else {
       "NO COMMITS"
   }
   ```

4. If a remote is printed, the status is not empty, or a commit message differs
   from the checkpoints below, do not change the repository. Use a fresh retry.
5. Only when the item names are `.git`, `README.md`, or `DECISIONS.md`, you
   recognise them as this synthetic lesson, and step 4 passed, inspect an
   existing expected file with:

   ```powershell
   if (Test-Path -LiteralPath ".\README.md" -PathType Leaf) {
       Get-Content -LiteralPath ".\README.md"
   }
   if (Test-Path -LiteralPath ".\DECISIONS.md" -PathType Leaf) {
       Get-Content -LiteralPath ".\DECISIONS.md"
   }
   ```

6. Resume only at one exact checkpoint:

   | Clean checkpoint | Required exact state | Continue at |
   |---|---|---|
   | 0 | `NO COMMITS`; no `README.md` or `DECISIONS.md` | Part B |
   | 1 | one commit `Add synthetic queue note`; `README.md` says `Status: new`; no `DECISIONS.md` | Part D |
   | 2 | the first two expected commits; `README.md` says `Status: waiting`; no `DECISIONS.md` | Recreation |
   | 3 | all three expected commits; both files contain the completed lesson values | Codex check |

   Any other content or state—including an existing uncommitted `README.md`,
   a partial file, a staged change, unfamiliar content, or apparent real or
   sensitive data—must remain unchanged and routes to a fresh retry.
7. Create the next unused retry with:

   ```powershell
   $lessonPath = New-FoundationRetryAttempt -BaseName "foundation-05" -PracticeRoot $practiceRoot
   $lessonFolderName = Split-Path -Leaf $lessonPath
   Set-Location -LiteralPath $lessonPath
   "Selected fresh attempt: $lessonFolderName"
   ```

8. Record the retry name. In a new PowerShell session, replace only
   `"foundation-05"` in `$lessonFolderName` with that exact name. A retry starts
   with Part A in a new empty folder; it never alters the old repository.

Never rerun an earlier Git part on an accepted checkpoint. Resume at the table's
named next part. If you want to repeat the exercise from the beginning, create
a fresh retry repository first.

### Part A — create a local repository

Run this non-overwriting repository check:

```powershell
if (Test-Path -LiteralPath ".git" -PathType Container) {
    throw "STOP: an existing Git repository must be handled by the checkpoint decision above. Do not run git init again."
}
elseif (@(Get-ChildItem -Force).Count -eq 0) {
    git init
}
else {
    throw "STOP: this folder has files but no .git folder. Do not initialise or change it; use the next unused retry."
}
```

What this does: for a new empty attempt, it creates hidden Git tracking
information inside this one folder. It does not upload or overwrite a file.

Expected result: output includes `Initialized empty Git repository`. Existing
repositories are never reinitialised by this step.

### Part B — set a fictional identity for this practice repository

Run this guarded identity block:

```powershell
$currentName = git config --local user.name
$currentEmail = git config --local user.email
if ($currentName -and $currentName -ne "Course Learner") {
    throw "STOP: a different local Git name exists. Leave this repository unchanged and use a fresh retry."
}
if ($currentEmail -and $currentEmail -ne "course-learner@example.invalid") {
    throw "STOP: a different local Git email exists. Leave this repository unchanged and use a fresh retry."
}
if (-not $currentName) {
    git config --local user.name "Course Learner"
}
if (-not $currentEmail) {
    git config --local user.email "course-learner@example.invalid"
}
```

What this does: it records a deliberately fictional commit identity only in
this repository. The reserved `.invalid` address cannot receive email.

Run:

```powershell
git config --local --list
```

Expected result: the output includes the two fictional values.

### Part C — create, inspect, stage, and commit one file

1. Run this create-once guard:

   ```powershell
   if (Test-Path -LiteralPath ".\README.md") {
       throw "STOP: README.md already exists. Do not edit or overwrite it; use the checkpoint decision and, if needed, a fresh retry."
   }
   New-Item -ItemType File -Path ".\README.md" -ErrorAction Stop | Out-Null
   "CREATED ONCE — enter the guided README.md content."
   notepad ".\README.md"
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
   git commit --only -m "Add synthetic queue note" -- "README.md"
   if ($LASTEXITCODE -ne 0) {
       throw "STOP: the expected commit was not created. Do not add random changes; leave this attempt unchanged and use a fresh retry."
   }
   ```

   What this does: it creates one local snapshot containing only `README.md`.
   `--only` prevents an unrelated file staged by mistake from entering this
   commit.

### Part D — inspect and commit a modification

1. Run this exact checkpoint guard:

   ```powershell
   $readmeLines = @(Get-Content -LiteralPath ".\README.md")
   $workingChanges = @(git status --short)
   $latestMessage = git log -1 --format="%s"
   if (
       $workingChanges.Count -ne 0 -or
       $latestMessage -ne "Add synthetic queue note" -or
       $readmeLines.Count -ne 4 -or
       $readmeLines[0] -ne "# Synthetic queue" -or
       $readmeLines[1] -ne "" -or
       $readmeLines[2] -ne "Status: new" -or
       $readmeLines[3] -ne "Contains real data: no"
   ) {
       throw "STOP: this is not clean checkpoint 1. Do not edit README.md; use a fresh retry."
   }
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
   git commit --only -m "Update synthetic queue status" -- "README.md"
   if ($LASTEXITCODE -ne 0) {
       throw "STOP: the expected commit was not created. Do not add random changes; leave this attempt unchanged and use a fresh retry."
   }
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
- If a selected attempt exists, do not delete it. Apply the exact checkpoint
  decision before any changing command.
- If a commit says there is nothing to commit, do not add a random change and
  do not rerun earlier edits. Leave that attempt unchanged, create the next
  unused Foundation 5 retry, and repeat the exercise there.
- Git may print a hint about the default branch name after `git init`. That is
  information, not a failure.

## Now recreate it yourself

Continue only from clean checkpoint 2. Run this create-once and checkpoint
guard:

```powershell
$workingChanges = @(git status --short)
$messages = @(git log --reverse --format="%s")
if (
    $workingChanges.Count -ne 0 -or
    $messages.Count -ne 2 -or
    $messages[0] -ne "Add synthetic queue note" -or
    $messages[1] -ne "Update synthetic queue status" -or
    (Test-Path -LiteralPath ".\DECISIONS.md")
) {
    throw "STOP: this is not clean checkpoint 2. Do not create or overwrite DECISIONS.md; use a fresh retry."
}
New-Item -ItemType File -Path ".\DECISIONS.md" -ErrorAction Stop | Out-Null
"CREATED ONCE — complete DECISIONS.md, then continue the steps below."
notepad ".\DECISIONS.md"
```

In the newly created `DECISIONS.md`:

1. type the heading `Synthetic decision`;
2. add `Decision ID: DEC-204`;
3. add `Outcome: test again`;
4. save and close Notepad;
5. inspect status:

   ```powershell
   git status --short
   ```

   Expected output: `?? DECISIONS.md`.
6. stage only that file:

   ```powershell
   git add -- "DECISIONS.md"
   ```

7. inspect exactly what is staged:

   ```powershell
   git diff --staged -- "DECISIONS.md"
   ```

8. commit it and stop visibly if the expected commit was not created:

   ```powershell
   git commit --only -m "Add synthetic decision record" -- "DECISIONS.md"
   if ($LASTEXITCODE -ne 0) {
       throw "STOP: the recreation commit was not created. Leave this attempt unchanged and use a fresh retry."
   }
   ```

9. confirm the working tree is clean:

   ```powershell
   git status --short
   ```

   Expected output: nothing.
10. confirm the three commits:

    ```powershell
    git log --oneline -3
    ```

This uses a different file, record type, and commit message from the guided
example.

11. prove that this exercise has no configured remote:

    ```powershell
    $remoteNames = @(git remote)
    if ($LASTEXITCODE -ne 0) {
        throw "STOP: Git could not inspect configured remotes."
    }
    if ($remoteNames.Count -ne 0) {
        throw "STOP: this local-only practice repository has a configured remote. Do not push, fetch, or delete it; preserve the attempt and ask for read-only diagnosis."
    }
    "PASS: no Git remote is configured"
    ```

    Expected output: `PASS: no Git remote is configured`. “I did not push” is
    not enough evidence; the empty `git remote` result proves the stated local
    practice condition.

If the recreation commit reports nothing to commit or otherwise fails, leave
the attempt unchanged and use a fresh retry. Do not create another file or
invent a different commit merely to make the count reach three.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and its local Git metadata,
and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, stage, commit, restore, reset, clean, delete,
push, or change Git configuration. Run only read-only inspection commands such
as git status, git diff, git log, and git remote.

Report PASS or NOT YET for each criterion:
1. The folder is a local Git repository.
2. README.md contains Status: waiting and Contains real data: no.
3. DECISIONS.md contains DEC-204 and Outcome: test again.
4. The three expected commit messages exist in the correct order.
5. git status --short is empty.
6. git remote prints no name and git remote -v prints no entry; the repository
   has no configured remote.

Explain NOT YET in beginner language and make no changes.
I attest that I created this attempt with synthetic course data only and did
not intentionally add secrets, personal data, client data, employer data, or
other real work data. If you notice content that appears sensitive, stop the
inspection,
do not quote or repeat it, report only the file name and general category, and
report NOT YET. If you notice none, say: "No apparent sensitive content noticed
in this bounded inspection; this is not proof that none exists." Do not claim
that an inspection proves the folder is free of secrets or real data.
```

## Pass criteria

- [ ] I can explain Git as a version-control tool and know its name is not an
      acronym.
- [ ] I can distinguish untracked, staged, committed, and modified.
- [ ] I inspected status and the staged diff before every commit.
- [ ] The repository contains exactly the three intended local commits.
- [ ] `git status --short` prints nothing at the end.
- [ ] `git remote` prints nothing, so this practice repository is demonstrably
      local-only.
- [ ] I did not use a destructive Git command. I attest that all
      information I entered was synthetic and that I did not intentionally use
      a credential or real business data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
