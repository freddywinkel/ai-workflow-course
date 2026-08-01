# Beginner Software Check — Read-only and Safe

## What this page is for

Software download pages and supported versions change. This check asks Codex
to compare the course instructions with current official sources and report
what is already present on your Windows computer. It does **not** update the
course, edit a file, download software, or install anything.

Use this page only after Foundations 1 and 2. Then complete
[Windows Setup](SETUP_WINDOWS.md) yourself, one explained step at a time.

This is a **diagnostic practice**, not a software-building task. “Diagnostic”
means checking and interpreting the current situation before changing it.
Codex remains read-only throughout. Your practical work is to distinguish
required from optional software, recognise a Windows Store alias, state the
correct next manual action, and explain what must not happen.

In the Progressive Web App (PWA), **Read** means you finished reading this
page. Mark **Practical** complete only after you finish all four parts below:

1. follow the worked classification;
2. recreate the classification from a current report;
3. have Codex check your interpretation without changing anything; and
4. meet every pass criterion.

## Study plan — two blocks of no more than 60 minutes

**Time label: AUTHOR ESTIMATE — NOT BEGINNER MEASURED.** The published
1–2-hour range is a planning estimate, not measured novice completion time.
Use each row as a separate study segment. Stop when the row is complete or
when 60 focused minutes have elapsed, whichever happens first. Record the last
completed heading using synthetic wording, close the page, and take a break.
Resume from that heading; never combine blocks to catch up.

| Block | Maximum | Work and safe stopping point |
|---:|---:|---|
| 1 | 45 minutes | Learn the terms, read the dated baseline, and follow the worked classification. Stop after **Worked classification**. |
| 2 | 60 minutes | Recreate the current read-only classification, explain the next manual action, ask Codex to check it, and apply the pass criteria. Stop after saving the result for Windows Setup. |

Terms used below:

- **Git** is a version-control tool that records file changes. Git is a name,
  not an abbreviation.
- **Python** is the programming language used for the small rule-based
  workflow.
- **Python Install Manager** is the current official Windows tool for
  installing and selecting Python versions.
- **Visual Studio Code** is a text and code editor.
- **Node.js** runs JavaScript outside a web browser. It is optional in Course 1.
- **n8n** (pronounced “n-eight-n”) is a visual workflow-automation product. Its
  optional crosswalk lab is not required to pass Course 1.
- An **official source** is documentation published by the organisation that
  maintains the software.
- A **Uniform Resource Locator (URL)** is a web address.
- **Read-only** means Codex may inspect and report but may not change anything.
- An **application execution alias** is a Windows shortcut that may offer to
  open the Microsoft Store even when a real Python runtime is not installed.

## Follow along — I show you exactly how

This is Part 1.

First watch how the distinction is made. Do not install anything while doing
this part.

### Dated baseline for this computer

The full Course 1 product audit observed the following on **2026-07-28**. This
is a dated starting point, not a promise that the computer will never change:

| Check | Observed result | Meaning for you |
|---|---|---|
| Windows | Windows 11 Home, 64-bit | Suitable for the Windows course path |
| Memory | 31.4 gigabytes (GB) | More than the course needs |
| Free space on the Documents drive | 777.5 GB | More than the 2 GB setup minimum |
| Visual Studio Code | 1.130.0 | Already present |
| Git | 2.54.0.windows.1 | Already present and usable |
| Browsers | Microsoft Edge 150 and Google Chrome 150 | A current course browser is present |
| `python` | Windows Store alias only | This is **not** an installed Python runtime |
| `py` and `pymanager` | Not found | Install Python Install Manager manually in Windows Setup |
| Effective PowerShell execution policy | Restricted | Expected; Course 1 does not require activation or a policy change |
| Required Course 1 source files | Found | The current course folder is complete enough to begin preflight |

Do not reinstall Visual Studio Code or Git merely because a newer version
exists. First check whether the installed version still works for Course 1.
The required manual action on this baseline is installing the official Python
Install Manager and stable Python 3.14. Windows Setup explains that action.

If you are reading this later, use the read-only report below again. Do not
treat this table as a live scan.

### Worked classification

Using the dated table above:

- **Git** is required and ready because a working version was observed.
- **Visual Studio Code** is required and ready because a working version was
  observed.
- **Python** is required but not ready. The `python` command points only to a
  Windows Store alias, while `pymanager` is not found.
- **Node.js and n8n** are optional, so their absence would not block Course 1.
- The next manual action is to follow the official Python Install Manager
  steps in Windows Setup.
- The unsafe action would be to treat the Store alias as a runtime, let Codex
  install software, or copy an unofficial installation command.

The evidence determines the classification. A tool is not “ready” merely
because its command name appears.

## Now recreate it yourself

This is Part 2.

### Step 1 — locate the course folder

In File Explorer, open the folder that contains this course. Select the address
bar and copy the full path. It should end in:

```text
AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE
```

If you cannot find it, ask Codex to locate that folder in read-only mode. Do
not ask it to move the folder.

### Step 2 — ask Codex for a current, read-only report

Replace the placeholder with the copied full path, then send this entire
prompt:

```text
Please perform a READ-ONLY beginner software check for Course 1.

Course folder:
[PASTE THE FULL AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE PATH HERE]

You may:
1. inspect SOFTWARE_MATRIX.md, stack-manifest.yaml, requirements-course.txt,
   and SETUP_WINDOWS.md inside that course folder;
2. run non-mutating version or presence checks on this Windows computer,
   including the effective PowerShell execution policy, available space on the
   Documents drive, browser presence, and whether a `python` result is only a
   Windows Store alias;
3. browse the official documentation linked by those course files;
4. report what you found.

You must not create, edit, rename, move, or delete any file. Do not install,
update, download, or uninstall software. Do not change settings, environment
variables, PowerShell policy, Git configuration, or the course. Do not open or
print secrets. Do not use employer, client, patient, or other real work data.

Check the current official Windows guidance for Visual Studio Code, Git, and
the Python Install Manager. For Python, use
https://docs.python.org/3/using/windows.html as the primary source and confirm
the latest stable Python Install Manager version and whether stable Python
3.14 remains supported. Reject alpha, beta, and release-candidate preview
versions. Treat Node.js and n8n as optional Course 1 tools. Report:
- the check date and each official source URL;
- what appears installed and the observed version, or NOT FOUND;
- whether each required item is compatible with the current Course 1 files;
- the resolved Documents path, free space, effective PowerShell policy,
  browser presence, and Course 1 source-file presence;
- whether `python`, `py`, or `pymanager` is a real runtime, an install manager,
  a legacy launcher, a Windows Store alias, or NOT FOUND;
- any contradiction between the course and the official source;
- the next manual setup step, without performing it.

Use a table with columns: Tool, Required or optional, Observed, Official
guidance checked, Result, Learner's next manual step.

If live browsing is unavailable, write UNVERIFIED instead of guessing. If the
course needs a maintainer update, report that separately; do not edit it.
```

### Step 3 — interpret the report before acting

The report should separate:

- **required now:** Visual Studio Code, Git, and Python;
- **required Python route:** Python Install Manager plus a stable Python 3.14
  runtime;
- **optional later:** Node.js and n8n;
- **not installed:** a normal result before setup;
- **UNVERIFIED:** Codex could not confirm a current official source.

Do not copy an installation command from a search-result snippet or an
unofficial download site. Continue only with the official links in
[Windows Setup](SETUP_WINDOWS.md).

### Step 4 — write your own classification in the chat

Without copying the worked classification, complete this template from the
new report. Paste the completed template into the same Codex chat. Do not
include a username, account name, password, access key, or employer path.

```text
Check date:
Required and ready:
Required but not ready:
The observed python command is a real runtime, a Store alias, or not found:
Evidence for that classification:
Optional only:
My next manual action:
One action I must not take:
```

If every required tool is already ready on a later check, write `NONE` after
**Required but not ready** and name the next Windows Setup verification step.
Do not invent a missing installation task.

### Record the result later during Windows Setup

During Windows Setup you will create `setup-version-check.txt`. Type the check
date, the official links, and the observed version lines into that file
yourself. Do not paste passwords, access keys, account names, or employer
information.

## Ask Codex to check your work

This is Part 3.

After your completed template, send this prompt in the same chat:

```text
Check my classification against the read-only software report you just gave
me. Do not inspect anything new and do not create, edit, move, rename, delete,
download, install, update, or configure anything.

Report PASS or NOT YET for each point:
1. I separated every required Course 1 tool from optional Node.js and n8n.
2. I identified each required tool as ready or not ready from observed
   evidence, not from its name alone.
3. I correctly classified the observed python command as a real runtime, a
   Windows Store alias, or not found.
4. My next manual action follows Windows Setup and does not invent an
   unnecessary installation.
5. My prohibited action preserves the read-only, no-secrets, and no-real-data
   boundary.

Explain each NOT YET result in literal beginner language. Check my answer
only. Do not perform the next action for me.
```

Correct a NOT YET answer yourself, then ask Codex to check the revised answer.
Codex checking or rewriting the answer for you is not the recreation.

## Pass criteria

This is Part 4.

- [ ] Codex used read-only inspection and made no changes.
- [ ] Required and optional tools are clearly separated.
- [ ] A Windows Store `python` alias is not mistaken for a working runtime.
- [ ] Documents storage, PowerShell policy, browser presence, and required
      course files are reported.
- [ ] Every current-version statement has an official source URL and check
      date, or is marked `UNVERIFIED`.
- [ ] The report tells you what to do manually without installing anything.
- [ ] I completed the classification template in my own words.
- [ ] Codex reported PASS for all five interpretation criteria, or I corrected
      each NOT YET answer myself and requested another read-only check.
- [ ] No secret or real work data appears in the report.

If the report is missing evidence, ask Codex to correct the **report only**. If
your interpretation is NOT YET, correct your own template and ask for another
read-only check. Do not let the software check turn into an installation or
course-editing task.
