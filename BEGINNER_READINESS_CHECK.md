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

Read the practical, health, and data-safety boundaries on this page now. Before
opening Foundation 1, complete the required recreation exercise and Codex check
below. The separate **Module 1 entry gate** is checked later, after all nine
foundations. Continue to the [Beginner Foundations](foundations/README.md) only
after the readiness recreation meets every pass criterion. Do not skip the
foundations because an AI assistant can generate code. The professional skill
is being able to explain, test, stop, and repair what was generated.

## Study plan — two blocks of no more than 60 minutes

**Time label: AUTHOR ESTIMATE — NOT BEGINNER MEASURED.** The published
1–2-hour range is a planning estimate, not measured novice completion time.
Use each row as a separate study segment. Stop when the row is complete or
when 60 focused minutes have elapsed, whichever happens first. Record the last
completed heading using synthetic wording, close the page, and take a break.
Resume from that heading; never combine blocks to catch up.

| Block | Maximum | Work and safe stopping point |
|---:|---:|---|
| 1 | 45 minutes | Read the practical, assessment, learning, health, employment, and Foundation gates. Stop after **Foundation gate**. |
| 2 | 60 minutes | Complete the required readiness follow-along, different recreation, Codex check, and pass criteria. Stop after recording `READY` or `NOT READY` honestly. |

## Practical prerequisites

Before starting, confirm:

- [ ] I have a Windows computer on which I may install software.
- [ ] I have at least 2 gigabytes (GB) of free space on the drive that contains
      my Documents folder.
- [ ] I can use an internet connection for the official Python download and
      the one-time package installation. The required workflow runs offline
      after setup.
- [ ] I have a current web browser and can open the Course 1 progressive web
      app (PWA), an installable website.
- [ ] I can create a separate folder for this course.
- [ ] I can find the `AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE` source folder in
      Codex or File Explorer.
- [ ] I will use only **synthetic** course data, meaning information created for
      practice rather than copied from real people or work.
- [ ] I will not paste employer, client, patient, employee, or personal
      information into the course project or an AI tool.
- [ ] I will keep API keys—secret values that authorize access to a
      service—outside code and Git.
- [ ] I am willing to stop when I cannot explain an observed result.
- [ ] I understand that the progressive web app (PWA)—an installable
      website—is the course reader, not the workflow itself.

A cloud account, GitHub account, paid subscription, application programming
interface (API) key, employer login, Node.js, and n8n are **not** prerequisites.
A `Restricted` PowerShell execution policy is also acceptable: Course 1 calls
the virtual environment's Python file directly and does not require you to
activate it or weaken that policy.

## Plan for the final human assessment

You do not need an assessor to start or to complete the practice. The official
status `COURSE 1 COMPETENCE: PASS`, however, requires at least two other
eligible adults:

- both independently complete the assessor-calibration cases;
- one calibrated assessor reviews and scores the artifacts; and
- one independent assessor hears the live oral assessment.

Version 2.6.0 is also an `UNVERIFIED` personal-study product release. Prepare
the assessment evidence now, but do not record the final competence pass until
both a later course-product `PASS` and your independent human assessment exist.
Keep `ASSESSMENT PENDING` while either is missing.

The same two people may divide or share the artifact and oral roles. They must
consent, must not create, edit, or correct your evidence, must be able to read
the rubric and calibration cases, and must declare conflicts or help. The oral
assessor must hear your answers live. Use synthetic course material only.

Before any assessment or observed trial, state its purpose and expected time,
that participation is voluntary and may stop at any time, exactly what will be
observed, who can access the structured result, and the retention/deletion
date. State that this is not employment, medical, or professional evaluation.
Use participant/reviewer codes and collect no unnecessary names, employer
details, health information, credentials, or client information. Screen,
audio, video, or quotation recording is optional and requires separate
explicit consent. No recording is needed for Course 1 assessment.

Author planning estimate: reserve 30–45 minutes for the second calibrator and
2–4 hours for the primary calibration, artifact review, and oral assessment.
These estimates have not yet been measured with real beginner cohorts.

- [ ] I understand that I can start alone.
- [ ] I understand that Codex and self-reflection cannot award the competence
      pass.
- [ ] I expect to ask two eligible adults later, or I will honestly keep
      `ASSESSMENT PENDING` while continuing to use the practice evidence.

The exact storage, internet, write-access, browser, and source-folder checks are
in [Windows Setup](SETUP_WINDOWS.md). Complete that preflight before
installing Python.

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
- accept `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or `DO NOT CONTINUE` as
  valid evidence-based Course 1 conclusions.

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

## Required readiness exercise — complete before Foundation 1

This is a rehearsal for the practice method used throughout the course. Do not
automate the process. The skill is observing it clearly.

**Notepad** is the plain-text editor included with Windows. **File Explorer** is
the Windows application for viewing files and folders. **Codex** is the course
workspace assistant you are using now; when asked to work in **read-only** mode,
it may inspect and explain files but may not change them.

### Select or resume one attempt safely

Keep the demonstration and recreation together in one selected attempt folder.
Use this literal decision:

1. Open **Documents** in File Explorer.
2. If `controlled-ai-course-practice` is absent, create it. If it exists, open
   it; do not create a duplicate.
3. Look for `readiness-attempt`.
   - If it is absent, create it and select it for this attempt.
   - If it exists, open it and inspect the item names. The only expected
     subfolders are `follow-along` and `recreate`.
4. Open any existing expected text file in Notepad before deciding:
   - if its content is your own, fictional, and exactly complete for the step
     below, close it without saving and skip that file's creation;
   - if a required file or subfolder is absent, it may be created by its step;
   - if an existing file is incomplete, different, unfamiliar, or appears to
     contain real or sensitive information, close it without saving. Do not
     edit, rename, delete, or overwrite anything in that attempt.
5. When step 4 requires a fresh attempt, return to
   `controlled-ai-course-practice` and select the next unused name:
   `readiness-attempt-retry-01`, then `readiness-attempt-retry-02`, and so on.
   Create the first name that is absent and use it for both parts below.

Write down the selected attempt-folder name. A later restart means reopening
that exact folder and applying the same decision again; it does not mean
starting over inside an existing incomplete file.

### Follow along — I show you exactly how

Use the harmless example **preparing a three-item shopping list**.

1. In the selected attempt folder, look for `follow-along`.
   - If absent, create and open it.
   - If present, open it and inspect the item names.
2. Look for `shopping-process.txt`.
   - If it exists and contains the exact completed demonstration below, close
     it without saving and skip to the expected result.
   - If it exists but is incomplete, different, unfamiliar, or appears
     sensitive, close it without saving, choose the next unused readiness retry
     folder above, and restart this part there.
   - Only if it is absent should you continue to step 3.
3. Open **Notepad** from the Windows Start menu.
4. Type the heading `Shopping-list process`.
5. On the next lines, type exactly:

   ```text
   Start: I notice that household supplies are running low.
   Input: the items that are missing.
   Fixed steps: check the cupboard, write each missing item, take the list.
   Human judgment: decide whether an item is needed this week.
   Possible failure: I forget to check one cupboard.
   Manual fallback: look through each cupboard again with paper and a pen.
   ```

6. Select **File → Save As**.
7. In the Save As window, browse to the `follow-along` subfolder inside your
   selected readiness attempt.
8. In **File name**, enter `shopping-process.txt`.
9. Select **Save**.
10. Close Notepad, reopen the file from File Explorer, and confirm all six
    labelled lines remain.

Expected result: the folder contains one readable text file with a start,
input, fixed steps, judgment, possible failure, and manual fallback.

If the file appears as `shopping-process.txt.txt`, turn on
**File Explorer → View → Show → File name extensions**. Do not rename, delete,
or overwrite the incorrectly saved file. Preserve that attempt, choose the next
unused readiness retry folder, and repeat the exercise there using the correct
file name.

### Now recreate it yourself

In the same selected readiness attempt, look for the subfolder `recreate`.
Create it only if it is absent, then open it. Look for
`household-task-process.txt`:

- if it exists and already meets every recreation requirement below, close it
  without saving and skip its creation;
- if it is incomplete, different, unfamiliar, or appears sensitive, close it
  without saving, choose the next unused readiness retry folder, and repeat the
  complete demonstration and recreation there;
- only if it is absent should you use the same Notepad **Save As** method to
  create it.

Use a different harmless process: checking whether fictional household tasks
are overdue.

Write the same six labels, but create your own content. Include at least three
fictional tasks. Do not copy the shopping-list answers and do not use work,
client, patient, or other real personal information.

### Ask Codex to check your work

Open the `recreate` subfolder inside your selected attempt. Replace the
placeholder below with its full path shown in File Explorer's address bar,
then send the prompt to Codex:

```text
Please inspect this practice folder in READ-ONLY mode:
[PASTE THE FULL PATH TO THE recreate SUBFOLDER IN YOUR SELECTED ATTEMPT HERE]

Do not create, edit, rename, move, or delete anything. Check only this folder.
Confirm that household-task-process.txt exists and contains: a clear start,
input, fixed steps, a human judgment, one possible failure, a manual fallback,
and at least three fictional tasks. Report PASS or NOT YET. If it is NOT YET,
explain the exact smallest correction and let me make it.

I attest that I created this attempt with fictional course information only and
did not intentionally add secrets or real employer, client, patient, employee,
or personal data. If you notice content that appears sensitive, stop
the inspection, do not quote or repeat it, report only the file name and general
category, and report NOT YET. If you notice none, say:
"No apparent sensitive content noticed in this bounded inspection; this is not proof that none exists."
Do not claim that an inspection proves the folder is free of secrets or real
data.
```

### Pass criteria

- [ ] The recreation uses a different process from the demonstration.
- [ ] All six requested labels contain a specific answer.
- [ ] At least three tasks are fictional.
- [ ] A person still owns the judgment.
- [ ] The fallback can be performed without AI or automation.
- [ ] I attest that all information I entered was fictional course information
      and that I did not intentionally add secrets or real personal, employer,
      or client data.
- [ ] Codex reports `PASS` after read-only inspection.

Do not begin Foundation 1 while any box above remains unchecked. After all
boxes are checked, continue to the
[Beginner Foundations](foundations/README.md) and start Foundation 1.

## Not ready is useful information

If the readiness check feels overwhelming, complete one foundation per study
session. The course intentionally separates foundational literacy from the
project so you can see what you are learning and why.
