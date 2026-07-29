# Foundation 1 — Files, Folders, Paths, and Plain Text

## Outcome

You will create a safe practice folder in Windows, make two correctly named
plain-text files, reopen them, and verify their exact contents.

This lesson assumes no technical experience.

## Study plan — six blocks of no more than 60 minutes

**Time label: AUTHOR ESTIMATE — NOT BEGINNER MEASURED.** The published
5–6-hour range is a planning estimate, not measured novice completion time.
Use each row as a separate study segment. Stop when the row is complete or
when 60 focused minutes have elapsed, whichever happens first. Record the last
completed part using synthetic wording, close every file, and take a break.
Use **Start or resume safely** at the next block; never combine blocks.

| Block | Maximum | Work and safe stopping point |
|---:|---:|---|
| 1 | 60 minutes | Learn the required words and safety boundary. Stop before **Follow along**. |
| 2 | 60 minutes | Complete **Start or resume safely**, Part A, and Part B. Stop after file extensions are visible. |
| 3 | 60 minutes | Complete Part C and verify the Markdown filename and text. |
| 4 | 60 minutes | Complete Part D and verify the JavaScript Object Notation (JSON) filename and text. |
| 5 | 60 minutes | Complete Part E, compare the exact expected result, and use troubleshooting if needed. |
| 6 | 60 minutes | Recreate the task with different content, ask Codex for the bounded check, and apply every pass criterion. |

## Words you need first

- A **folder** is a container for files and other folders.
- A **file** is stored information with a name.
- A **path** is the address of a file or folder.
- A **file extension** is the ending after the final dot. `.txt` means a plain
  text file, `.md` usually means a Markdown file, and `.json` means a JSON data
  file.
- **Plain text** stores ordinary characters without hidden document formatting.
- **Markdown** is plain text that uses simple marks such as `#` for a heading.
  Its usual extension is `.md`.
- **JavaScript Object Notation (JSON)** is a strict plain-text data format. Its
  extension is `.json`. **JavaScript** is a programming language, but you do not
  need to know JavaScript to read JSON.
- An **identifier (ID)** is a stable value that identifies one fictional
  record, such as `REQ-001`.
- **Unicode Transformation Format 8-bit (UTF-8)** is a common way to store text
  characters. Select it when saving the files in this lesson.
- **Codex** is the artificial intelligence (AI) assistant used for the final
  read-only check. The check prompt limits it to one practice folder.

**Microsoft Word** is a word-processing program. Its `.docx` format stores a
formatted document rather than plain text. A **Portable Document Format (PDF)**
file uses the `.pdf` extension and preserves a document's page layout. Do not
rename either format to `.txt`, `.md`, or `.json` to convert it.

## Safety boundary

Use only the fictional values printed below. Do not enter a real name,
workplace, customer, patient, supplier, email address, password, or access key.

## Follow along — I show you exactly how

### Prerequisites and start state

- You are at the Windows desktop.
- **File Explorer**, the Windows program used to browse folders, and
  **Notepad**, the Windows plain-text editor, are available.
- No real business document is open.

### Start or resume safely

Before creating anything, look in `Documents`:

1. If `controlled-ai-course-practice` does not exist, create it in Part A.
2. If it already exists, open it. Do not create a duplicate and do not delete
   its contents.
3. If `foundation-01` does not exist, use that name for this attempt.
4. If `foundation-01` already exists, open it and inspect only the file names.
   If it contains your own synthetic work from this lesson, resume at the first
   unfinished part. Open an existing file and read it before deciding whether
   your own unfinished practice needs a correction. Never paste the sample over
   an existing file without inspecting it first.
5. If the folder contains unfamiliar material, real data, or different
   practice you want to keep unchanged, stop. Create a new folder beside it
   named `foundation-01-retry-01`. If that name also exists, try
   `foundation-01-retry-02`, then the next unused number. Use that one folder
   for the whole lesson.

Where the instructions below say `foundation-01`, that means the unused or
resumed attempt folder you selected above. The final Codex prompt uses the full
path you paste, so a safe retry folder works without changing the check.

### Part A — create the practice folder

1. Hold the Windows key and press `E`.

   What this does: it opens File Explorer.

2. In the left side of File Explorer, click **Documents**.

   What this does: it opens your Windows Documents folder. The full path may
   include **OneDrive**, Microsoft's cloud file-synchronisation service, on some
   computers; that is acceptable.

3. Look for a folder named `controlled-ai-course-practice`.
   - If it exists, do not click **New**. Continue to step 5.
   - If it does not exist, click **New**, then click **Folder**. If your
     version of Windows has no **New** button, right-click an empty area, click
     **New**, then click **Folder**.
4. Only when the folder was absent, type this exact folder name and press
   Enter:

   ```text
   controlled-ai-course-practice
   ```

5. Double-click `controlled-ai-course-practice`.
6. If your selected lesson-attempt folder does not exist, create it using the
   same method. For a first attempt, name it:

   ```text
   foundation-01
   ```

   If you selected an existing attempt or a numbered retry folder, do not
   create or rename it.

7. Double-click the lesson-attempt folder you selected.

   What this does: it gives this lesson one isolated folder. The folder should
   be empty for a new attempt. A resumed attempt may contain your earlier
   synthetic lesson files; do not overwrite them automatically.

### Part B — make Windows show file extensions

1. In File Explorer, click **View**.
2. On Windows 11, click **Show**, then click **File name extensions** so a
   checkmark appears.
3. On Windows 10, click the **View** tab and select the **File name
   extensions** checkbox.

What this does: Windows now shows endings such as `.txt`, `.md`, and `.json`.
This prevents `notes.md.txt` from looking like `notes.md`.

### Part C — create a Markdown file in Notepad

1. In File Explorer, first look for `process-notes.md`.
   - If it is absent, continue to step 2.
   - If it exists, open it in Notepad and inspect it. If it already contains
     the exact guided synthetic content, close it without saving and continue
     at Part D. If it is your own incomplete attempt, correct only that attempt
     and keep the required fictional values, save it, close it, and continue at
     Part D. If it is unfamiliar or contains real data, close it without saving
     and use a new retry folder.
2. Press the Windows key once.
3. Type `Notepad`.
4. Click **Notepad** in the search result.
5. For a new file, type or paste these exact four lines:

   ```markdown
   # Synthetic request notes

   - Request ID: REQ-001
   - Contains real business data: no
   ```

6. In Notepad, click **File**, then **Save as**.
7. In the Save As window, browse to your selected lesson-attempt folder, for
   example:

   ```text
   Documents\controlled-ai-course-practice\foundation-01
   ```

8. In **File name**, type:

   ```text
   process-notes.md
   ```

9. Set **Save as type** to **All files (*.*)**.
10. Set **Encoding** to **UTF-8**.
11. Click **Save**.

What this does: it saves plain text with the intended `.md` extension instead
of silently adding `.txt`.

### Part D — create a JSON file in Notepad

1. In File Explorer, first look for `request.json`.
   - If it exists, open and inspect it before changing anything. If it already
     contains the exact guided synthetic content, close it without saving and
     continue at Part E. If it is your own incomplete attempt, correct only
     that attempt, save it, close it, and continue at Part E. If it is
     unfamiliar or contains real data, close it without saving and use a new
     retry folder.
   - If it is absent, continue to step 2.
2. In Notepad, click **File**, then **New tab**. If **New tab** is unavailable,
   close and reopen Notepad.
3. For a new file, type or paste this exact content:

   ```json
   {
     "request_id": "REQ-001",
     "status": "new",
     "contains_real_data": false
   }
   ```

4. Click **File**, then **Save as**.
5. Save it in the same selected lesson-attempt folder.
6. Use this file name:

   ```text
   request.json
   ```

7. Set **Save as type** to **All files (*.*)**.
8. Set **Encoding** to **UTF-8**.
9. Click **Save**.

What this does: it creates structured data. The quotation marks, colon,
commas, braces, lowercase `false`, and final extension are part of the format.

### Part E — verify what Windows actually saved

1. Return to the File Explorer window.
2. If the files are not visible, press the `F5` function key once to refresh.
3. For a new attempt before the recreation, confirm the folder contains
   exactly:

   ```text
   process-notes.md
   request.json
   ```

   A resumed attempt that already completed the recreation may also contain
   `case-card.md` and `case.json`. No unfamiliar or real-data file should be
   present.

4. Double-click `process-notes.md`. If Windows asks which program to use,
   select Notepad.
5. Confirm the heading and two list items are still present. Close that tab or
   window.
6. Right-click `request.json`, click **Open with**, then click **Notepad**.
7. Confirm all five JSON lines are still present.
8. Return to File Explorer, click once in the address bar, and press `Ctrl+C`.

What the final action does: it copies the full path of this one practice folder.
Keep it available for the Codex check below.

### Expected result — exact

Before the recreation, a new lesson-attempt folder contains exactly two files,
not folders:

```text
process-notes.md
request.json
```

Neither name ends in `.txt`. The Markdown file contains `REQ-001` and the JSON
file contains `"status": "new"` and `"contains_real_data": false`. A resumed
attempt may already include the two recreation files as well; that is not an
error.

### Troubleshooting

- If the name is `process-notes.md.txt`, turn on file-name extensions, right-click
  the file, click **Rename**, remove only the final `.txt`, and accept the
  extension warning.
- If Notepad saved in another folder, use **File > Save as** again and select
  the exact `foundation-01` folder.
- If curly quotation marks appear in JSON, replace them with the straight
  quotation mark `"`. JSON does not accept typographic “smart quotes.”
- If you accidentally used real information, close the file, replace it with
  the fictional content above, and do not paste the real content into Codex.

## Now recreate it yourself

In the same selected lesson-attempt folder, create two new files without
copying the guided filenames:

1. `case-card.md` containing:
   - a heading `Synthetic case card`;
   - case ID `CASE-742`;
   - owner role `operations`;
   - the statement `Contains real business data: no`.
2. `case.json` containing a JSON object with:
   - `"case_id": "CASE-742"`;
   - `"state": "waiting"`;
   - `"contains_real_data": false`.

Use Notepad, **All files (*.*)**, and **UTF-8**. Reopen both files and verify the
contents. This uses different names, fields, and values so you demonstrate that
you understood the method rather than merely copied it.

Before creating either recreation file, check whether its name already exists.
If it does, inspect it first. Resume your own incomplete synthetic attempt or
leave a completed file unchanged. If it is unfamiliar or contains real data,
use a new retry folder and repeat the guided work there. Do not automatically
replace an existing file.

## Ask Codex to check your work

Before sending the prompt, replace `[PASTE THE FULL FOLDER PATH]` with the one
full path copied from File Explorer. The authorisation applies only to that
folder.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE FULL FOLDER PATH]

Do not create, edit, move, rename, or delete anything. Do not run a command
that changes files, settings, or external systems.

Check and report PASS or NOT YET for each criterion:
1. process-notes.md exists and does not end in .txt.
2. request.json exists, is valid JSON, and contains REQ-001, status new, and
   contains_real_data false.
3. case-card.md exists and contains CASE-742, owner role operations, and the
   no-real-data statement.
4. case.json exists, is valid JSON, and contains CASE-742, state waiting, and
   contains_real_data false.
5. No extra extension is hidden in any of those four names.

Explain a NOT YET result in beginner language, but make no changes.
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

- [ ] I created or safely resumed the selected lesson-attempt folder myself:
      either `foundation-01` or the numbered `foundation-01-retry-XX` folder
      whose full path I gave to Codex.
- [ ] File Explorer visibly shows file-name extensions.
- [ ] `process-notes.md` and `case-card.md` do not end in `.txt`.
- [ ] Both JSON files reopen with straight quotation marks and the intended
      values.
- [ ] I can explain file, folder, path, extension, plain text, Markdown, JSON,
      and UTF-8 in my own words.
- [ ] I attest that all information I entered was synthetic practice
      information and that I did not intentionally add secrets or real
      personal, employer, or client data.
- [ ] Codex reported PASS for every read-only check, or I corrected each
      NOT YET item myself and requested another read-only check.
