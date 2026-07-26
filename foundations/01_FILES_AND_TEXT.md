# Foundation 1 — Files, Folders, Paths, and Plain Text

## Outcome

You will create a safe practice folder in Windows, make two correctly named
plain-text files, reopen them, and verify their exact contents.

This lesson assumes no technical experience.

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

### Part A — create the practice folder

1. Hold the Windows key and press `E`.

   What this does: it opens File Explorer.

2. In the left side of File Explorer, click **Documents**.

   What this does: it opens your Windows Documents folder. The full path may
   include **OneDrive**, Microsoft's cloud file-synchronisation service, on some
   computers; that is acceptable.

3. At the top, click **New**, then click **Folder**.

   If your version of Windows has no **New** button, right-click an empty area,
   click **New**, then click **Folder**.

4. Type this exact folder name and press Enter:

   ```text
   controlled-ai-course-practice
   ```

5. Double-click `controlled-ai-course-practice`.
6. Create another folder in it using the same method. Name it:

   ```text
   foundation-01
   ```

7. Double-click `foundation-01`.

   What this does: it gives this lesson one isolated folder. The folder should
   currently be empty.

### Part B — make Windows show file extensions

1. In File Explorer, click **View**.
2. On Windows 11, click **Show**, then click **File name extensions** so a
   checkmark appears.
3. On Windows 10, click the **View** tab and select the **File name
   extensions** checkbox.

What this does: Windows now shows endings such as `.txt`, `.md`, and `.json`.
This prevents `notes.md.txt` from looking like `notes.md`.

### Part C — create a Markdown file in Notepad

1. Press the Windows key once.
2. Type `Notepad`.
3. Click **Notepad** in the search result.
4. Type or paste these exact four lines:

   ```markdown
   # Synthetic request notes

   - Request ID: REQ-001
   - Contains real business data: no
   ```

5. In Notepad, click **File**, then **Save as**.
6. In the Save As window, browse to:

   ```text
   Documents\controlled-ai-course-practice\foundation-01
   ```

7. In **File name**, type:

   ```text
   process-notes.md
   ```

8. Set **Save as type** to **All files (*.*)**.
9. Set **Encoding** to **UTF-8**.
10. Click **Save**.

What this does: it saves plain text with the intended `.md` extension instead
of silently adding `.txt`.

### Part D — create a JSON file in Notepad

1. In Notepad, click **File**, then **New tab**. If **New tab** is unavailable,
   close and reopen Notepad.
2. Type or paste this exact content:

   ```json
   {
     "request_id": "REQ-001",
     "status": "new",
     "contains_real_data": false
   }
   ```

3. Click **File**, then **Save as**.
4. Save it in the same `foundation-01` folder.
5. Use this file name:

   ```text
   request.json
   ```

6. Set **Save as type** to **All files (*.*)**.
7. Set **Encoding** to **UTF-8**.
8. Click **Save**.

What this does: it creates structured data. The quotation marks, colon,
commas, braces, lowercase `false`, and final extension are part of the format.

### Part E — verify what Windows actually saved

1. Return to the File Explorer window.
2. If the files are not visible, press the `F5` function key once to refresh.
3. Confirm the folder contains exactly:

   ```text
   process-notes.md
   request.json
   ```

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

The `foundation-01` folder contains exactly two files, not folders:

```text
process-notes.md
request.json
```

Neither name ends in `.txt`. The Markdown file contains `REQ-001` and the JSON
file contains `"status": "new"` and `"contains_real_data": false`.

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

In the same `foundation-01` folder, create two new files without copying the
guided filenames:

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
This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] I created and opened the exact `foundation-01` folder myself.
- [ ] File Explorer visibly shows file-name extensions.
- [ ] `process-notes.md` and `case-card.md` do not end in `.txt`.
- [ ] Both JSON files reopen with straight quotation marks and the intended
      values.
- [ ] I can explain file, folder, path, extension, plain text, Markdown, JSON,
      and UTF-8 in my own words.
- [ ] The folder contains only synthetic practice information.
- [ ] Codex reported PASS for every read-only check, or I corrected each
      NOT YET item myself and requested another read-only check.
