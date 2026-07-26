# Beginner Readiness Check

## You may start with zero technical knowledge

You do not need prior experience with:

- programming;
- **PowerShell**, the Windows tool in which you type commands;
- **Git**, a version-control tool that records changes to files; Git is a
  product name, not an abbreviation;
- **Python**, a programming language used for the small code examples in this
  course;
- an **application programming interface (API)**, which lets software exchange
  requests and responses;
- **JavaScript Object Notation (JSON)**, a strict text format used to store or
  exchange structured data;
- spreadsheets beyond basic use;
- **databases**, organized collections of information that software can search
  and update;
- **n8n** (pronounced “n-eight-n”), a workflow-automation application, or other
  workflow tools;
- artificial intelligence (AI) services reached through an API.

Start with the [Beginner Foundations](foundations/README.md). Do not skip them
because an AI assistant can generate code. The professional skill is being able
to explain, test, stop, and repair what was generated.

## Practical prerequisites

Before starting, confirm:

- [ ] I have a Windows computer on which I may install software.
- [ ] I can create a separate folder for this course.
- [ ] I will use only **synthetic** course data, meaning information created for
      practice rather than copied from real people or work.
- [ ] I will not paste employer, client, patient, employee, or personal
      information into the course project or an AI tool.
- [ ] I will keep API keys—secret values that authorize access to a
      service—outside code and Git.
- [ ] I am willing to stop when I cannot explain an observed result.
- [ ] I understand that the progressive web app (PWA)—an installable
      website—is the course reader, not the workflow itself.

## Learning readiness

The course is **gate-based**: you continue after meeting a stated pass
checklist, not simply because a planned week has ended. A healthy study rhythm
matters more than speed.

You are ready when you can:

- reserve several short, focused sessions rather than relying on one long
  session;
- write down errors and observed outputs instead of repeatedly trying random
  changes;
- redo a small exercise without copying;
- explain uncertainty without hiding it;
- accept `NO AI`, `REWORK`, or `DO NOT PILOT` as valid conclusions.

## Health and employment boundary

If study or business preparation happens during sick leave, discuss sustained
workload, interviews, and especially paid activity with the relevant
**bedrijfsarts** (occupational physician), **casemanager** (person coordinating
the absence or return-to-work process), employer, or the Dutch Employee
Insurance Agency (*Uitvoeringsinstituut Werknemersverzekeringen*, UWV) as
applicable. Self-paced study is not automatically equivalent to normal job
capacity, but it should not conflict with **reintegration** obligations—the
agreed steps towards a safe return to work.

This course does not provide employment or benefits advice.

## Foundation gate

Do not begin Module 1 until you can demonstrate all of the following:

- [ ] I can identify the folder a command will affect.
- [ ] I can distinguish code (instructions for a computer), configuration
      (settings), data (information used as input), secrets (password-like
      access values), and generated output (files a program creates).
- [ ] I can read a small Python function line by line.
- [ ] I can explain a JSON object, a comma-separated values (CSV) row, a
      column, an **identifier (ID)** that uniquely labels one item, and a
      **missing value** where an expected field is blank.
- [ ] I can use `git status`, which lists changed files, and `git diff`, which
      shows the changed lines, to inspect a change.
- [ ] I know that valid JSON from an AI model—the AI system producing the
      answer—is not automatically true.
- [ ] I can explain the difference between a **deterministic rule**, which gives
      the same result for the same input, and an AI judgment.
- [ ] I can describe a **trigger** that starts the workflow, a **workflow step**
      that performs one action, a **state** that names the current stage, an
      **exception** that needs attention, and a **manual fallback** that a person
      can use when the workflow cannot continue.
- [ ] I can run a small check twice and compare the results.
- [ ] I know how to stop a running command.

If one item is unclear, return to the matching foundation. This is normal.

## Module 1 entry exercise

This is a rehearsal for the practice method used throughout the course. Do not
automate the process. The skill is observing it clearly.

**Notepad** is the plain-text editor included with Windows. **File Explorer** is
the Windows application for viewing files and folders. **Codex** is the course
workspace assistant you are using now; when asked to work in **read-only** mode,
it may inspect and explain files but may not change them.

### Follow along — I show you exactly how

Use the harmless example **preparing a three-item shopping list**.

1. Open **Notepad** from the Windows Start menu.
2. Type the heading `Shopping-list process`.
3. On the next lines, type exactly:

   ```text
   Start: I notice that household supplies are running low.
   Input: the items that are missing.
   Fixed steps: check the cupboard, write each missing item, take the list.
   Human judgment: decide whether an item is needed this week.
   Possible failure: I forget to check one cupboard.
   Manual fallback: look through each cupboard again with paper and a pen.
   ```

4. Select **File → Save As**.
5. In the Save As window, select **Documents** in the left side.
6. Select **New folder**, type `controlled-ai-course-practice`, and press
   `Enter`. If that folder already exists, open it instead of creating a
   duplicate.
7. Open `controlled-ai-course-practice`.
8. Select **New folder**, type `readiness-follow-along`, and press `Enter`.
9. Open `readiness-follow-along`.
10. In **File name**, enter `shopping-process.txt`.
11. Select **Save**.
12. Close Notepad, reopen the file from File Explorer, and confirm all six
    labelled lines remain.

Expected result: the folder contains one readable text file with a start,
input, fixed steps, judgment, possible failure, and manual fallback.

If the file appears as `shopping-process.txt.txt`, turn on
**File Explorer → View → Show → File name extensions**, then remove only the
extra final `.txt`.

### Now recreate it yourself

Repeat the same Save As method, but create the different folder
`Documents\controlled-ai-course-practice\readiness-recreate` and save
`household-task-process.txt` inside it. Use a different harmless process:
checking whether fictional household tasks are overdue.

Write the same six labels, but create your own content. Include at least three
fictional tasks. Do not copy the shopping-list answers and do not use work,
client, patient, or other real personal information.

### Ask Codex to check your work

Replace the placeholder below with the full path shown in File Explorer's
address bar, then send the prompt to Codex:

```text
Please inspect this practice folder in READ-ONLY mode:
[PASTE THE FULL PATH TO readiness-recreate HERE]

Do not create, edit, rename, move, or delete anything. Check only this folder.
Confirm that household-task-process.txt exists and contains: a clear start,
input, fixed steps, a human judgment, one possible failure, a manual fallback,
and at least three fictional tasks. Check that it contains no secrets or real
employer, client, patient, employee, or personal data. Report PASS or NOT YET.
If it is NOT YET, explain the exact smallest correction and let me make it.
```

### Pass criteria

- [ ] The recreation uses a different process from the demonstration.
- [ ] All six requested labels contain a specific answer.
- [ ] At least three tasks are fictional.
- [ ] A person still owns the judgment.
- [ ] The fallback can be performed without AI or automation.
- [ ] Codex reports `PASS` after read-only inspection.

## Not ready is useful information

If the readiness check feels overwhelming, complete one foundation per study
session. The course intentionally separates foundational literacy from the
project so you can see what you are learning and why.
