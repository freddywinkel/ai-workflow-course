# Foundation 2 — PowerShell and Command-Line Interface (CLI) Survival

**PowerShell** is the Windows command shell used in this course. A
**command-line interface (CLI)** is a text interface for giving a program exact
instructions.

## Outcome

You will open PowerShell, identify the **prompt** that shows it is ready, move to
one safe practice folder, run read and write commands one at a time, recognise
an **error** message that says an action failed, and return to a ready prompt.

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
guarded Part B block. It creates `foundation-02` only when absent, enters it,
and lists existing content. If you see your own synthetic lesson work, resume
at the first unfinished step. Do not repeat a write command for a file that
already exists until you inspect it. Stop if a name is unfamiliar, is the
wrong kind of item, or may contain real data.

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

   ```powershell
   $lessonPath = Join-Path (Get-Location).Path "foundation-02"
   if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
       throw "STOP: foundation-02 is a file, not a folder. Do not rename or delete it; ask Codex to inspect read-only."
   }
   if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
       New-Item -ItemType Directory -Path $lessonPath | Out-Null
       "Created a new foundation-02 folder."
   }
   else {
       "Existing foundation-02 folder found; nothing was overwritten."
   }
   Set-Location -LiteralPath $lessonPath
   Get-ChildItem -Force
   ```

   What this does: `Test-Path` first checks what exists. `New-Item` creates one
   new folder only when it is missing. `Set-Location` enters the selected
   folder, and `Get-ChildItem -Force` shows its contents without changing them.

3. Run:

   ```powershell
   Get-Location
   ```

   Expected output: the path ends in
   `controlled-ai-course-practice\foundation-02`.

### Part C — create, read, and list one synthetic file

The vertical bar `|`, called a **pipeline**, passes output from the command on
its left to the command on its right. `-LiteralPath` tells PowerShell to treat a
path exactly as written. **Unicode Transformation Format 8-bit (UTF-8)** is a
common text encoding; `-Encoding utf8` selects it for the saved file.

1. Run this non-overwriting version:

   ```powershell
   if (Test-Path -LiteralPath "terminal-note.txt") {
       "Existing terminal-note.txt found; it was not overwritten."
       Get-Content -LiteralPath "terminal-note.txt"
   }
   else {
       "Synthetic command-line practice" | Set-Content -LiteralPath "terminal-note.txt" -Encoding utf8
       "Created terminal-note.txt."
   }
   ```

   What this does: the pipeline sends the text on its left to `Set-Content`.
   `Set-Content` writes the named practice file, using the exact literal path
   and UTF-8 encoding declared in the command.

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

   Expected result: PowerShell still works and the location is still
   `foundation-02`.

5. Run:

   ```powershell
   (Get-Location).Path
   ```

   What this does: it prints the exact full folder path to use in the Codex
   prompt below.

### Expected result — exact

- The current location ends with `foundation-02`.
- `Get-Content` prints `Synthetic command-line practice`.
- `Get-ChildItem` lists `terminal-note.txt`.
- Reading `missing-file.txt` produces an error, then returns to a prompt.

### Troubleshooting

- If `foundation-02` already exists, the guarded block reports that nothing was
  overwritten and lists its contents. Resume only your synthetic practice.
- If `controlled-ai-course-practice` cannot be found, return to Foundation 1
  and confirm its spelling and Documents location.
- If a command appears to keep running, hold the Control key (`Ctrl`) and press
  `C` once, then wait for the prompt. Record the last output.
- If the path contains spaces, keep the quotation marks.

## Now recreate it yourself

Inside `foundation-02`, use the commands you learned to:

1. create a subfolder named `recreated-check`;
2. enter it;
3. create `status-note.txt` containing exactly `Recreated safely`;
4. read the file;
5. list the folder;
6. return to `foundation-02` using:

   ```powershell
   Set-Location ..
   ```

Do not reuse `terminal-note.txt` or its sentence. Confirm `Get-Location` ends in
`foundation-02` after you return. This creates a new nested folder and new
content rather than copying the guided file.

If `recreated-check` already exists, inspect it before entering it. Resume your
own incomplete synthetic recreation or leave a completed one unchanged. Do
not overwrite an existing `status-note.txt`; stop if the content is unfamiliar
or real.

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
This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] I can point to the prompt, command, output, and error.
- [ ] I ran one command at a time and read its complete result.
- [ ] `Get-Location` ends in `foundation-02`.
- [ ] Both expected text files exist with the exact synthetic contents.
- [ ] I can explain what `Get-Location`, `Set-Location`, `Get-ChildItem`,
      `Set-Content`, and `Get-Content` do.
- [ ] I know that an error is evidence and not permission to run destructive
      cleanup.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
