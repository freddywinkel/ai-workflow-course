# Foundation 2 — PowerShell and Command-Line Survival

## Outcome

You can run one safe command at a time, know which folder it affects, distinguish
output from errors, and stop when the result is unexpected.

## What a command line is

PowerShell is a Windows program in which you type instructions. The
**command-line interface** (CLI) is the text-based way you interact with it.
It is not magic and it is not an AI chat box. A command can read, create, alter,
or delete things, so its exact text and current folder matter.

Open PowerShell from the Start menu. You will see a **prompt**, similar to:

```text
PS C:\Users\YourName>
```

Do not type the `PS C:\Users\YourName>` part. It tells you PowerShell is ready
and shows the current folder.

In a lesson, this is a code fence:

```powershell
Get-Location
```

Copy only `Get-Location`. Do not copy the three backticks or the word
`powershell`.

## The four parts of a terminal interaction

```text
PS C:\Users\YourName> Get-Location     ← prompt plus command

Path
----
C:\Users\YourName                     ← output
```

An error is usually red and explains that the requested action did not work.
An error is evidence. Do not hide it and do not repeatedly rerun a changing
command until something appears to work.

## Your safe starter commands

Run these one at a time:

```powershell
Get-Location
```

Shows your current folder. It changes nothing.

```powershell
Get-ChildItem
```

Lists items in the current folder. It changes nothing. `dir` and `ls` are common
aliases, but this course writes the full PowerShell command when clarity helps.

```powershell
Set-Location "$env:USERPROFILE\Documents"
```

Moves the terminal's current location to your Documents folder. It does not move
any files. The quotes keep a path containing spaces together.

```powershell
New-Item -ItemType Directory -Path "course-cli-practice"
```

Creates one folder inside the current folder. Before running it, confirm
`Get-Location` shows Documents.

```powershell
Set-Location "course-cli-practice"
Get-Location
```

The first line changes location. The second verifies it. Run them one line at a
time during your first sessions.

```powershell
"first note" | Set-Content -Path "note.txt"
Get-Content -Path "note.txt"
```

The first command writes a practice file and the second reads it. This example
is safe only because you deliberately created and selected the practice folder.
For course file edits, use your editor or the supplied patch workflow rather
than improvised overwrite commands.

## Copy/paste protocol

Before every unfamiliar command:

1. Read the complete command before copying.
2. Identify whether it only reads or might change something.
3. Run `Get-Location`.
4. Confirm the target path.
5. Copy only the command, not prompt text, output, bullets, or code fences.
6. Paste one command at a time.
7. Press Enter once.
8. Read all output before continuing.
9. Save the exact error if it fails.

Multiple lines in one code block are multiple commands unless the lesson says
otherwise. On your first pass, run them individually.

## Paths, spaces, and variables

Quote paths containing spaces:

```powershell
Set-Location "C:\Users\YourName\Business ventures"
```

`$env:USERPROFILE` asks Windows for your user-profile path:

```powershell
$env:USERPROFILE
```

It is safer than replacing `YourName` by hand. An environment variable is a
named value available to programs. A secret key may be placed in an environment
variable so it is not written into code, but it can still leak through
screenshots, logs, or careless commands.

## Starting and stopping programs

Some commands finish and return a prompt. A server command keeps running:

```powershell
python -m uvicorn supplier_review.api.main:app --reload --port 8000
```

While it runs, that terminal is occupied. Open a second PowerShell window for
the next command. Press **Ctrl+C** in the server's terminal to request that it
stop. Wait for the prompt to return.

If a command seems frozen:

1. wait briefly for normal startup;
2. read the last output;
3. press Ctrl+C once;
4. wait for the prompt;
5. record what happened.

Do not close Windows or end random processes as a first response.

## Command anatomy

```powershell
python -m pytest tests -q
```

- `python` is the program;
- `-m pytest` asks Python to run the installed `pytest` module;
- `tests` is an argument identifying the target folder;
- `-q` is an option requesting quieter output.

```powershell
git diff -- README.md
```

- `git` is the program;
- `diff` is its subcommand;
- `--` separates Git options from file paths;
- `README.md` is the target.

Never remove unfamiliar flags just to make a command shorter.

## Red-flag commands

Stop and ask for an explanation before running any command that:

- deletes recursively (`Remove-Item -Recurse`, `rm -rf`, `rmdir /s`);
- rewrites Git history or discards work (`git reset --hard`, forced checkout,
  forced push);
- changes execution policy;
- runs downloaded text directly;
- requests administrator privileges without a clear installation reason;
- targets a drive root, user-profile root, or broad wildcard;
- prints secrets or entire environment-variable sets;
- uploads files to an unfamiliar service.

For each, require the AI assistant to explain the exact resolved target, why it
is necessary, the recovery method, and a safer alternative.

## How to report an error

Send the coding assistant:

```text
Goal:
Exact command I ran:
Folder shown by Get-Location:
Complete output/error:
What I expected:
What changed since the last successful step:
```

Remove secrets, usernames, tokens, account IDs, and real data. Do not paraphrase
the error; exact text is often what identifies the cause.

## Practice

In `Documents\course-cli-practice`:

1. verify the current location;
2. list the folder;
3. read `note.txt`;
4. create a subfolder named `safe-test`;
5. enter it and verify the location;
6. return to the parent with `Set-Location ..`;
7. run a deliberately unknown command such as
   `this-command-does-not-exist`;
8. identify the command, error output, and returning prompt.

Keep the practice folder. Do not practise deletion commands.

## Chapter check

You pass when you can:

- point to the prompt, command, output, and error;
- explain why current location matters;
- stop a running server with Ctrl+C;
- explain why quotes are used around some paths;
- state why a recursive deletion or hard Git reset requires a pause.

