# Beginner Software Check — Read-only and Safe

## What this page is for

Software download pages and supported versions change. This check asks Codex
to compare the course instructions with current official sources and report
what is already present on your Windows computer. It does **not** update the
course, edit a file, download software, or install anything.

Use this page only after Foundations 1 and 2. Then complete
[Windows Setup](SETUP_WINDOWS.md) yourself, one explained step at a time.

Terms used below:

- **Git** is a version-control tool that records file changes. Git is a name,
  not an abbreviation.
- **Python** is the programming language used for the small rule-based
  workflow.
- **Visual Studio Code** is a text and code editor.
- **Node.js** runs JavaScript outside a web browser. It is optional in Course 1.
- **n8n** (pronounced “n-eight-n”) is a visual workflow-automation product. Its
  optional crosswalk lab is not required to pass Course 1.
- An **official source** is documentation published by the organisation that
  maintains the software.
- A **Uniform Resource Locator (URL)** is a web address.
- **Read-only** means Codex may inspect and report but may not change anything.

## Step 1 — locate the course folder

In File Explorer, open the folder that contains this course. Select the address
bar and copy the full path. It should end in:

```text
AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE
```

If you cannot find it, ask Codex to locate that folder in read-only mode. Do
not ask it to move the folder.

## Step 2 — ask Codex for a current, read-only report

Replace the placeholder with the copied full path, then send this entire
prompt:

```text
Please perform a READ-ONLY beginner software check for Course 1.

Course folder:
[PASTE THE FULL AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE PATH HERE]

You may:
1. inspect SOFTWARE_MATRIX.md, stack-manifest.yaml, requirements-course.txt,
   and SETUP_WINDOWS.md inside that course folder;
2. run non-mutating version or presence checks on this Windows computer;
3. browse the official documentation linked by those course files;
4. report what you found.

You must not create, edit, rename, move, or delete any file. Do not install,
update, download, or uninstall software. Do not change settings, environment
variables, PowerShell policy, Git configuration, or the course. Do not open or
print secrets. Do not use employer, client, patient, or other real work data.

Check the current official Windows guidance for Visual Studio Code, Git, and
Python. Treat Node.js and n8n as optional Course 1 tools. Report:
- the check date and each official source URL;
- what appears installed and the observed version, or NOT FOUND;
- whether each required item is compatible with the current Course 1 files;
- any contradiction between the course and the official source;
- the next manual setup step, without performing it.

Use a table with columns: Tool, Required or optional, Observed, Official
guidance checked, Result, Learner's next manual step.

If live browsing is unavailable, write UNVERIFIED instead of guessing. If the
course needs a maintainer update, report that separately; do not edit it.
```

## Step 3 — read the report before acting

The report should separate:

- **required now:** Visual Studio Code, Git, and Python;
- **optional later:** Node.js and n8n;
- **not installed:** a normal result before setup;
- **UNVERIFIED:** Codex could not confirm a current official source.

Do not copy an installation command from a search-result snippet or an
unofficial download site. Continue only with the official links in
[Windows Setup](SETUP_WINDOWS.md).

## Step 4 — keep a simple record

During Windows Setup you will create `setup-version-check.txt`. Type the check
date, the official links, and the observed version lines into that file
yourself. Do not paste passwords, access keys, account names, or employer
information.

## Pass check

- [ ] Codex used read-only inspection and made no changes.
- [ ] Required and optional tools are clearly separated.
- [ ] Every current-version statement has an official source URL and check
      date, or is marked `UNVERIFIED`.
- [ ] The report tells you what to do manually without installing anything.
- [ ] No secret or real work data appears in the report.

If any item is missing, ask Codex to correct the **report only**. Do not let the
software check turn into an installation or course-editing task.
