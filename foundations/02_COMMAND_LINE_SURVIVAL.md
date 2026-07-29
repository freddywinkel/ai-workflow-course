# Foundation 2 — PowerShell and Command-Line Interface (CLI) Survival

**PowerShell** is the Windows command shell used in this course. A
**command-line interface (CLI)** is a text interface for giving a program exact
instructions.

## Outcome

You will open PowerShell, identify the **prompt** that shows it is ready, move to
one safe practice folder, run read and write commands one at a time, recognise
an **error** message that says an action failed, and return to a ready prompt.

## Study plan — seven blocks of no more than 60 minutes

**Time label: AUTHOR ESTIMATE — NOT BEGINNER MEASURED.** The published
6–7-hour range is a planning estimate, not measured novice completion time.
Use each row as a separate study segment. Stop when the row is complete or
when 60 focused minutes have elapsed, whichever happens first. Record the last
completed part using synthetic wording, close PowerShell, and take a break.
Use **Start or resume safely** at the next block; never combine blocks.

| Block | Maximum | Work and safe stopping point |
|---:|---:|---|
| 1 | 60 minutes | Learn the required words and safety boundary. Stop before **Follow along**. |
| 2 | 60 minutes | Open PowerShell, locate Documents, and complete Part A. Stop at a ready prompt. |
| 3 | 60 minutes | Complete Part B and verify the selected lesson folder. |
| 4 | 60 minutes | Apply the resume/retry decision and complete Part C. Stop after reading the synthetic file. |
| 5 | 60 minutes | Complete Part D, compare the exact expected result, and troubleshoot only the named symptom. |
| 6 | 60 minutes | Recreate the task in the different required folder and explain each command before running it. |
| 7 | 60 minutes | Ask Codex for the bounded read-only check, correct only observed gaps, and apply every pass criterion. |

## Words you need first

- A **terminal** is the window that hosts the shell.
- The **prompt** is the text showing that PowerShell is ready, such as
  `PS C:\Users\YourName>`. The letters `PS` label a PowerShell prompt; they are
  not part of the command. Do not copy the prompt as part of a command.
- A **command** is one instruction you enter.
- **Output** is information a command prints after it runs.
- An **error** is information explaining that the requested action did not
  complete.
- The **current location** is the folder a command will use when no full path is
  supplied.
- An **environment variable** is a named value supplied by Windows. This lesson
  uses the Windows Documents location without exposing private information.
- **Codex** is the artificial intelligence (AI) assistant used for the final
  read-only check. The check prompt limits it to one practice folder.
- A **code fence** is a block marked by three backticks above and below an
  example. A **backtick** is this mark: `` ` ``. Neither the backticks nor a
  language label such as `powershell` is part of the command.
- An **administrator command** runs with elevated system rights.
- An **execution policy** is a PowerShell setting that controls when scripts may
  run.
- A **downloaded script** is a file of commands obtained from another source;
  inspect and trust its source before considering whether to run it.
- A **server** is software that stays running to listen for requests.

In a code-fenced example such as:

```powershell
Get-Location
```

copy only `Get-Location`, not the three backticks or the word `powershell`.

## Safety boundary

Run one command at a time and read all output before continuing. Do not practise
deletion, administrator commands, execution-policy changes, downloaded scripts,
or commands aimed at a broad user or drive folder.

## Follow along — I show you exactly how

### Prerequisites and start state

- Foundation 1 is complete.
- `Documents\controlled-ai-course-practice` exists.
- No PowerShell window is currently running a server or installation.

### Start or resume safely

At every new PowerShell session, repeat Part A to reach Documents, then run the
guarded Part B block. On the first attempt, leave `$lessonFolderName` as
`foundation-02`. If the recovery instructions below created a numbered retry,
replace only that quoted value with the exact retry name PowerShell displayed.
The block creates only an absent selected attempt, enters it, and lists its
contents before any lesson file can be written.

### Part A — open PowerShell and locate Documents

1. Press the Windows key once.
2. Type `PowerShell`.
3. Click **Windows PowerShell** or **PowerShell** in the search result.
4. Look at the final line. It should begin with `PS` and end with `>`.

   What this does: it confirms the prompt is ready. Do not type the visible
   `PS ...>` text.

5. Type this exact command and press Enter:

   ```powershell
   Get-Location
   ```

   What this does: it reads the current location. It changes nothing.

6. Type this exact command and press Enter:

   ```powershell
   Set-Location ([Environment]::GetFolderPath("MyDocuments"))
   ```

   What this does: `GetFolderPath("MyDocuments")` asks Windows for your actual
   Documents path, including a redirected OneDrive path if applicable.
   `Set-Location` moves only the terminal's current location; it does not move
   files.

7. Run:

   ```powershell
   Get-Location
   ```

   Expected output: a path ending in `Documents`, or the Documents folder used
   by your Windows account.

### Part B — create and enter the lesson folder

1. Run:

   ```powershell
   Set-Location "controlled-ai-course-practice"
   ```

   What this does: it enters the practice root created in Foundation 1.

2. Run this guarded block exactly as shown. You do not need to memorise `if`
   yet: it means “perform the indented action only when the condition is true.”
   `function` gives a reusable name to a group of commands. The helper below
   finds and creates only the next unused retry folder when the recovery
   decision tells you to use it.

   ```powershell
   $practiceRoot = (Get-Location).Path
   $lessonFolderName = "foundation-02"
   if ($lessonFolderName -notmatch '^foundation-02(?:-retry-\d{2,})?$') {
       throw "STOP: use foundation-02 or a retry name created by this lesson."
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

   if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
       throw "STOP: the selected Foundation 2 attempt is a file, not a folder. Do not change it; use a fresh retry attempt."
   }
   if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
       New-Item -ItemType Directory -Path $lessonPath | Out-Null
       "Created a new Foundation 2 attempt: $lessonFolderName"
   }
   else {
       "Existing Foundation 2 attempt found; nothing was overwritten: $lessonFolderName"
   }
   Set-Location -LiteralPath $lessonPath
   Get-Location
   Get-ChildItem -Force
   ```

   What this does: `Test-Path` first checks what exists. `New-Item` creates one
   new selected attempt only when it is missing. `Set-Location` enters it,
   `Get-Location` prints its path, and `Get-ChildItem -Force` shows its contents
   without changing them. `New-FoundationRetryAttempt` is defined but does
   nothing until you deliberately call it after the decision below.

3. Run:

   ```powershell
   Get-Location
   ```

   Expected output: the path ends in
   `controlled-ai-course-practice\foundation-02` or in the selected numbered
   retry name.

### Decide whether to resume or use a fresh attempt

Apply this decision before Part C and again after every interruption:

1. An empty selected attempt continues at Part C.
2. The only expected items are `terminal-note.txt` and the
   `recreated-check` folder. Inside `recreated-check`, the only expected item is
   `status-note.txt`.
3. For an attempt containing only those expected items:
   - an existing file with exactly the complete synthetic lesson content stays
     unchanged and its creation step is skipped;
   - an absent expected item may be created by its guarded step;
   - an incomplete, different, unfamiliar, wrong-kind, or apparently
     real/sensitive item must not be edited, renamed, deleted, or overwritten.
4. An unexpected item also requires a fresh attempt.
5. For either stop condition, run:

   ```powershell
   $lessonPath = New-FoundationRetryAttempt -BaseName "foundation-02" -PracticeRoot $practiceRoot
   $lessonFolderName = Split-Path -Leaf $lessonPath
   Set-Location -LiteralPath $lessonPath
   "Selected fresh attempt: $lessonFolderName"
   ```

   `Split-Path -Leaf` reads only the final folder name from the complete retry
   path; it does not move or change the folder.

6. Write down the displayed retry name. In a new PowerShell session, replace
   only `"foundation-02"` in `$lessonFolderName` with that exact name. Restart
   at Part C in the new empty attempt.

### Part C — create, read, and list one synthetic file

The vertical bar `|`, called a **pipeline**, passes output from the command on
its left to the command on its right. `-LiteralPath` tells PowerShell to treat a
path exactly as written. **Unicode Transformation Format 8-bit (UTF-8)** is a
common text encoding; `-Encoding utf8` selects it for the saved file.

1. Run this create-once version:

   ```powershell
   $terminalNotePath = Join-Path $lessonPath "terminal-note.txt"
   if (Test-Path -LiteralPath $terminalNotePath -PathType Container) {
       throw "STOP: terminal-note.txt is a folder. Do not change it; use a fresh retry attempt."
   }
   if (Test-Path -LiteralPath $terminalNotePath -PathType Leaf) {
       "EXISTING — DO NOT EDIT OR OVERWRITE: terminal-note.txt"
       Get-Content -LiteralPath $terminalNotePath
   }
   else {
       "Synthetic command-line practice" | Set-Content -LiteralPath $terminalNotePath -Encoding utf8
       "CREATED ONCE: terminal-note.txt"
   }
   ```

   What this does: the pipeline sends the text on its left to `Set-Content`.
   `Set-Content` writes the named practice file, using the exact literal path
   and UTF-8 encoding declared in the command. If the file already exists, the
   block displays it without changing it. Leave it unchanged only if it exactly
   matches the complete guided sentence. Any other existing content requires a
   fresh retry attempt.

2. Run:

   ```powershell
   Get-Content -LiteralPath "terminal-note.txt"
   ```

   What this does: it reads the file without changing it.

   Expected output:

   ```text
   Synthetic command-line practice
   ```

3. Run:

   ```powershell
   Get-ChildItem
   ```

   What this does: it lists items in the current folder.

   Expected result: the listing contains `terminal-note.txt`.

### Part D — observe a safe, expected error

1. Run:

   ```powershell
   Get-Content -LiteralPath "missing-file.txt"
   ```

   What this does: it asks PowerShell to read a file that deliberately does not
   exist.

2. Read the error. It should name `missing-file.txt` and say that the path
   cannot be found.
3. Confirm a new `PS ...>` prompt appears after the error.
4. Run:

   ```powershell
   Get-Location
   ```

   Expected result: PowerShell still works and the location is still the exact
   selected Foundation 2 attempt.

5. Run:

   ```powershell
   (Get-Location).Path
   ```

   What this does: it prints the exact full folder path to use in the Codex
   prompt below.

### Expected result — exact

- The current location ends with `foundation-02` or the selected numbered retry
  name.
- `Get-Content` prints `Synthetic command-line practice`.
- `Get-ChildItem` lists `terminal-note.txt`.
- Reading `missing-file.txt` produces an error, then returns to a prompt.

### Troubleshooting

- If the selected attempt already exists, the guarded block reports that
  nothing was overwritten and lists its contents. Apply the attempt decision;
  incomplete, different, unfamiliar, wrong-kind, or apparently real content
  requires the next unused retry.
- If `controlled-ai-course-practice` cannot be found, return to Foundation 1
  and confirm its spelling and Documents location.
- If a command appears to keep running, hold the Control key (`Ctrl`) and press
  `C` once, then wait for the prompt. Record the last output.
- If the path contains spaces, keep the quotation marks.

## Now recreate it yourself

Inside the selected Foundation 2 attempt, first set and inspect the exact nested
path before creating anything:

```powershell
$recreatedPath = Join-Path $lessonPath "recreated-check"
if (Test-Path -LiteralPath $recreatedPath -PathType Leaf) {
    throw "STOP: recreated-check is a file, not a folder. Do not change it; use a fresh retry attempt."
}
if (Test-Path -LiteralPath $recreatedPath -PathType Container) {
    "EXISTING — inspect before entering recreated-check."
    Get-ChildItem -LiteralPath $recreatedPath -Force
}
else {
    "ABSENT — it is safe to create recreated-check with New-Item."
}
```

An absent folder is the case in which you perform the six recreation actions.
If the folder exists, leave a complete `status-note.txt` unchanged. Any
incomplete, different, unfamiliar, wrong-kind, or apparently real content
requires a fresh retry attempt; do not overwrite it.

For an absent folder, use the commands you learned to:

1. create a subfolder named `recreated-check`;
2. enter it;
3. create `status-note.txt` containing exactly `Recreated safely`;
4. read the file;
5. list the folder;
6. return to the selected attempt using:

   ```powershell
   Set-Location ..
   ```

Do not reuse `terminal-note.txt` or its sentence. Confirm `Get-Location` ends in
the exact selected attempt name after you return. This creates a new nested
folder and new content rather than copying the guided file.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, or delete anything. Do not run any command
that changes files, settings, or external systems.

Report PASS or NOT YET for each criterion:
1. terminal-note.txt exists directly in the authorized folder.
2. Its exact content is: Synthetic command-line practice
3. recreated-check exists as a subfolder.
4. recreated-check\status-note.txt exists and its exact content is:
   Recreated safely
5. No file named missing-file.txt was created.

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

- [ ] I can point to the prompt, command, output, and error.
- [ ] I ran one command at a time and read its complete result.
- [ ] `Get-Location` ends in `foundation-02` or the exact numbered
      `foundation-02-retry-XX` attempt whose full path I gave to Codex.
- [ ] Both expected text files exist with the exact synthetic contents.
- [ ] I can explain what `Get-Location`, `Set-Location`, `Get-ChildItem`,
      `Set-Content`, and `Get-Content` do.
- [ ] I know that an error is evidence and not permission to run destructive
      cleanup.
- [ ] I attest that all information I entered was synthetic practice
      information and that I did not intentionally add secrets or real
      personal, employer, or client data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
