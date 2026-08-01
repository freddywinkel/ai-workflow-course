# Foundation 4 — Application Programming Interfaces (APIs), Hypertext Transfer Protocol (HTTP), and JavaScript Object Notation (JSON)

## Outcome

You will create a fictional request and response, validate both JSON files
locally, and explain why an accepted request is not the same as completed or
correct work.

## Study plan — six blocks of no more than 60 minutes

**Time label: AUTHOR ESTIMATE — NOT BEGINNER MEASURED.** The published
5–6-hour range is a planning estimate, not measured novice completion time.
Use each row as a separate study segment. Stop when the row is complete or
when 60 focused minutes have elapsed, whichever happens first. Record the last
completed part using synthetic wording, save and close files, and take a break.
Run **Start or resume safely** in every new PowerShell session; never combine
blocks.

| Block | Maximum | Work and safe stopping point |
|---:|---:|---|
| 1 | 60 minutes | Learn the request, response, Hypertext Transfer Protocol (HTTP), Application Programming Interface (API), and JSON words plus the safety boundary. |
| 2 | 60 minutes | Run the start/resume block and make the explicit resume/retry decision. |
| 3 | 60 minutes | Complete Part B and verify the fictional request before continuing. |
| 4 | 60 minutes | Complete Part C and verify the fictional response before continuing. |
| 5 | 60 minutes | Complete Part D, compare the exact result, and troubleshoot only observed mismatches. |
| 6 | 60 minutes | Recreate the request/response with different content, ask Codex for the bounded check, and apply every pass criterion. |

## Words you need first

- A **client** is software that sends a request.
- A **server** is software that listens for requests and returns responses.
- An **application programming interface (API)** is an agreed way for software
  components to communicate.
- **Hypertext Transfer Protocol (HTTP)** is a common set of rules for web
  requests and responses.
- A **Uniform Resource Locator (URL)** is an address for a web resource.
- An **endpoint** is one HTTP method and path exposed by an API.
- A **method** describes the requested kind of operation. `GET` normally reads;
  `POST` normally submits or creates. The documentation, not the label alone,
  defines the actual behaviour.
- A **request** is the message sent by a client.
- A **response** is the server's answer.
- A **header** is request or response information such as content type.
- A **body** is the main data carried by a request or response.
- A **status code** is a three-digit result category such as `200`, `202`,
  `400`, or `500`.
- An **identifier (ID)** is a stable value that identifies one record, such as
  `WI-DEMO-21`.
- **Python** is the programming language used here to check the example files.
- A **Python module** is a reusable code component. This lesson uses Python's
  built-in `json.tool` module only as a local validator.
- **JavaScript Object Notation (JSON)** is a strict text format for structured
  data.
- A **JSON object** groups named fields between braces `{}`.
- A **JSON array** is an ordered collection of values between brackets `[]`.
- A **Boolean** is a true-or-false value; JSON writes these as lowercase `true`
  and `false`.
- **`null`** is JSON's explicit value for deliberately absent data.
- **PowerShell** is the Windows command shell used to create and check the
  files. **Notepad** is the Windows plain-text editor used to enter them.
- A **synthetic** record is deliberately fictional practice data.
- **Metadata** is data that describes another record, such as its identifier
  and status.
- **Authentication** checks who or what is making a request.
- **Authorisation** checks what that identity may do. Some product
  documentation uses the American spelling **authorization**.
- An **API key** or **access token** is a secret credential that can grant
  software access to a service.
- A **private address** is a URL intended only for authorised, non-public use.
- **Codex** is the artificial intelligence (AI) assistant used for the final
  read-only check. The check prompt limits file inspection to one practice
  folder and permits only the exact project Python file to validate the named
  local JSON files without making a change.

`202 Accepted` means a request was accepted for processing. It does not prove
processing finished or that the result is factually correct.

## Safety boundary

This lesson makes no network request. It stores only fictional request and
response examples. Do not enter an API key, password, access token, private
address, or business record.

## Follow along — I show you exactly how

### Prerequisites and start state

- Foundations 1–3 are complete.
- Windows Setup is complete, including the project virtual environment at
  `Documents\AI-workflow-learning\operations-exception-assistant\.venv`.
- `Documents\controlled-ai-course-practice` exists.
- PowerShell is showing a ready prompt or is closed.

### Start or resume safely — run this at every new PowerShell session

PowerShell forgets variables when you close its window. Run this whole block
whenever you start or resume Foundation 4. On the first attempt, leave
`$lessonFolderName` as `foundation-04`. If the recovery instructions below
created a numbered retry folder, replace only that quoted value with the retry
folder name that PowerShell displayed:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$projectRoot = Join-Path $documentsPath "AI-workflow-learning\operations-exception-assistant"
$projectMarker = Join-Path $projectRoot "COURSE_PROJECT.md"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonFolderName = "foundation-04"
if ($lessonFolderName -notmatch '^foundation-04(?:-retry-\d{2,})?$') {
    throw "STOP: use foundation-04 or a displayed foundation-04-retry-XX name."
}
$lessonPath = Join-Path $practiceRoot $lessonFolderName

$expectedProjectMarker = @'
# Course 1 synthetic learner project

This folder is only for the fictional Course 1 practice project.
Never place real client, employer, medical, or personal data here.
'@
if (-not (Test-Path -LiteralPath $projectMarker -PathType Leaf)) {
    throw "STOP: the exact Course 1 project marker is missing. Return to Windows Setup."
}
$actualProjectMarker = (
    Get-Content -Raw -LiteralPath $projectMarker
) -replace "`r`n", "`n"
$normalizedExpectedProjectMarker = $expectedProjectMarker -replace "`r`n", "`n"
if ($actualProjectMarker -ne $normalizedExpectedProjectMarker) {
    throw "STOP: the Course 1 project marker is unfamiliar. Do not execute this folder."
}
$projectGitRoot = git -C $projectRoot rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "STOP: the marked Course 1 Git repository is missing or unreadable."
}
if (
    (Resolve-Path -LiteralPath $projectGitRoot).Path -ne
    (Resolve-Path -LiteralPath $projectRoot).Path
) {
    throw "STOP: Git resolves to a different repository root. Do not continue."
}
if (-not (Test-Path -LiteralPath $pythonExe -PathType Leaf)) {
    throw "STOP: the exact course Python file is missing. Return to Windows Setup; do not use a bare python command."
}
$pythonVersion = & $pythonExe --version
if ($LASTEXITCODE -ne 0 -or $pythonVersion -notmatch '^Python 3\.14\.\d+$') {
    throw "STOP: expected a stable Python 3.14 patch from the project virtual environment."
}
if (-not (Test-Path -LiteralPath $practiceRoot -PathType Container)) {
    throw "STOP: the controlled-ai-course-practice folder is missing. Return to Foundation 1."
}
if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
    throw "STOP: the selected Foundation 4 attempt is a file, not a folder. Do not rename or delete it; ask Codex to inspect read-only."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new Foundation 4 attempt folder: $lessonFolderName"
}
else {
    "Existing Foundation 4 attempt folder found; nothing was overwritten: $lessonFolderName"
}

Set-Location -LiteralPath $lessonPath
Get-Location
$pythonExe
$pythonVersion
Get-ChildItem -Force
```

This derives the exact project interpreter from your real Documents path,
requires the exact synthetic Course 1 identity marker, confirms Git resolves
to that project rather than a parent or different repository, checks that the
interpreter exists, accepts only a stable Python 3.14 patch, creates the lesson
folder only when it is absent, and shows any existing content before you edit.
The displayed executable path must end in
`AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`,
and the current location must end in
`controlled-ai-course-practice\foundation-04` or end in the selected numbered
retry folder.

If existing files are listed, inspect them before continuing. Resume only an
attempt whose existing files are your own complete synthetic lesson files;
files that are still absent may be created by the guarded steps below. Never
paste or save lesson content over an existing file. If an existing file is
incomplete, unfamiliar, or may contain real data, use
**Create a safe retry attempt** below.

### Create a safe retry attempt — only when an existing file is not complete

Do not edit, rename, delete, or overwrite the existing file. Close Notepad
without saving, then run this whole block:

```powershell
$retryNumber = 1
do {
    $lessonFolderName = "foundation-04-retry-{0:D2}" -f $retryNumber
    $lessonPath = Join-Path $practiceRoot $lessonFolderName
    $retryNumber += 1
} while (Test-Path -LiteralPath $lessonPath)

New-Item -ItemType Directory -Path $lessonPath -ErrorAction Stop | Out-Null
Set-Location -LiteralPath $lessonPath
"Created safe retry folder: $lessonFolderName"
(Get-Location).Path
```

Expected result: PowerShell displays a new name such as
`foundation-04-retry-01` and its full path. Write down that displayed folder
name. Use this new empty folder for all remaining guided and recreation files.
Whenever you resume in a new PowerShell window, put that exact displayed name
in the `$lessonFolderName` line of the **Start or resume safely** block.

### Part B — create a fictional request

1. Run this create-once check:

   ```powershell
   $requestPath = Join-Path $lessonPath "request.json"
   if (Test-Path -LiteralPath $requestPath -PathType Container) {
       throw "STOP: request.json is a folder. Do not rename or delete it; use a safe retry attempt."
   }
   if (Test-Path -LiteralPath $requestPath -PathType Leaf) {
       "Existing request.json found. It was not opened for editing or overwritten."
       Get-Content -LiteralPath $requestPath
   }
   else {
       New-Item -ItemType File -Path $requestPath -ErrorAction Stop | Out-Null
       "Created request.json once. Enter the guided content, then save it."
       notepad $requestPath
   }
   ```

2. Read the output:
   - If PowerShell displayed the existing file, compare it with the exact JSON
     below. If it matches, do not open or save it; skip to Part C.
   - If the existing file is incomplete, different, unfamiliar, or may contain
     real data, do not edit it. Follow **Create a safe retry attempt**, then
     repeat this create-once check in the new empty attempt folder.
   - Only if PowerShell displayed `Created request.json once` should you type or
     paste the following content into the Notepad window:

   ```json
   {
     "method": "POST",
     "path": "/work-items/check",
     "body": {
       "work_item_id": "WI-DEMO-21",
       "status": "new"
     }
   }
   ```

3. Click **File > Save**, then close Notepad.

What this represents: a fictional client asks the endpoint
`POST /work-items/check` to accept metadata for one synthetic work item.
Nothing is sent to a server.

### Part C — create a fictional response

1. Run this create-once check:

   ```powershell
   $responsePath = Join-Path $lessonPath "response.json"
   if (Test-Path -LiteralPath $responsePath -PathType Container) {
       throw "STOP: response.json is a folder. Do not rename or delete it; use a safe retry attempt."
   }
   if (Test-Path -LiteralPath $responsePath -PathType Leaf) {
       "Existing response.json found. It was not opened for editing or overwritten."
       Get-Content -LiteralPath $responsePath
   }
   else {
       New-Item -ItemType File -Path $responsePath -ErrorAction Stop | Out-Null
       "Created response.json once. Enter the guided content, then save it."
       notepad $responsePath
   }
   ```

2. Read the output:
   - If PowerShell displayed the existing file, compare it with the exact JSON
     below. If it matches, do not open or save it; skip to Part D.
   - If the existing file is incomplete, different, unfamiliar, or may contain
     real data, do not edit it. Follow **Create a safe retry attempt**, then
     repeat Parts B and C in the new empty attempt folder.
   - Only if PowerShell displayed `Created response.json once` should you enter:

   ```json
   {
     "status_code": 202,
     "body": {
       "work_item_id": "WI-DEMO-21",
       "state": "received"
     }
   }
   ```

3. Save and close Notepad.

What this represents: a server accepted the request and recorded the state
`received`. It does not say the check completed.

### Part D — validate and read both files

1. Run:

   ```powershell
   & $pythonExe -m json.tool ".\request.json"
   ```

   What this does: `-m` asks Python to run its installed `json.tool` module.
   The module reads and validates JSON, then prints it in an indented form. It
   does not contact the internet or change the file.

2. Run:

   ```powershell
   & $pythonExe -m json.tool ".\response.json"
   ```

3. Run:

   ```powershell
   Get-ChildItem
   ```

4. Run:

   ```powershell
   (Get-Location).Path
   ```

   Keep this exact full path for the Codex prompt.

What the last two commands do: `Get-ChildItem` lists the saved files, and
`(Get-Location).Path` prints the exact full folder path. Neither changes a file.

### Expected result — exact

- Both `& $pythonExe -m json.tool` commands print indented JSON and return to
  the prompt without an error.
- The request output contains `"method": "POST"` and
  `"work_item_id": "WI-DEMO-21"`.
- The response output contains `"status_code": 202` and
  `"state": "received"`.
- `Get-ChildItem` lists exactly `request.json` and `response.json` before the
  recreation exercise.

### Troubleshooting

- If validation reports a line and column error, compare quotation marks,
  commas, braces, and spelling with the sample. Do not remove the validator.
- If a file ends in `.json.txt`, correct the extension using Foundation 1.
- If `$pythonExe` is missing, not recognised, or reports the wrong version,
  rerun the complete **Start or resume safely** block. If it still stops,
  return to Windows Setup. Do not use a bare `python` command and do not
  install an unverified package with a similar name.
- If a selected Foundation 4 attempt already exists, do not delete it or save
  guided content over any file. Inspect existing files with the create-once
  checks. Skip an exact completed file; use a safe retry attempt for any file
  that is incomplete, different, unfamiliar, or may contain real data.

## Now recreate it yourself

In the same selected Foundation 4 attempt folder, create two different valid
JSON files:

1. `get-request.json` representing:
   - method `GET`;
   - path `/tickets/TICKET-77`;
   - no request body.
2. `get-response.json` representing:
   - status code `200`;
   - a body containing ticket ID `TICKET-77`;
   - state `waiting`;
   - Boolean field `contains_real_data` set to `false`.

Before creating either file, run these create-once checks:

```powershell
$getRequestPath = Join-Path $lessonPath "get-request.json"
$getResponsePath = Join-Path $lessonPath "get-response.json"

foreach ($path in @($getRequestPath, $getResponsePath)) {
    if (Test-Path -LiteralPath $path -PathType Container) {
        throw "STOP: an expected JSON file name is a folder. Do not change it; use a safe retry attempt."
    }
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        "Existing file found; it was not opened or overwritten: $path"
        Get-Content -LiteralPath $path
    }
    else {
        New-Item -ItemType File -Path $path -ErrorAction Stop | Out-Null
        "Created once: $path"
    }
}
```

If either file existed, inspect the displayed content. If both are already
complete, skip creation and continue to validation. If either is incomplete,
different, unfamiliar, or may contain real data, do not edit or overwrite it;
use a safe retry attempt and repeat Parts B–D first.

Only for files for which PowerShell displayed `Created once`, open the path in
Notepad, create a clear JSON object shape yourself, then save and close it:

```powershell
notepad $getRequestPath
notepad $getResponsePath
```

Validate both files with the exact project interpreter:

```powershell
& $pythonExe -m json.tool ".\get-request.json"
& $pythonExe -m json.tool ".\get-response.json"
```

Do not reuse `WI-DEMO-21`, `POST`, or state `received`.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PRACTICE-FOLDER PATH]` with the full path output from
`(Get-Location).Path`. Replace `[PASTE THE EXACT PROJECT PYTHON PATH]` with the
full path printed for `$pythonExe` by the **Start or resume safely** block.

```text
You may access exactly these two locations, for only these purposes:
1. Inspect READ-ONLY this one practice folder:
   [PASTE THE EXACT PRACTICE-FOLDER PATH]
2. Execute, but do not edit or replace, this one project Python file:
   [PASTE THE EXACT PROJECT PYTHON PATH]

Do not browse, list, read, or inspect any other folder or file. Do not create,
edit, move, rename, or delete anything. Do not contact an external service,
install a package, or change settings.

Report PASS or NOT YET for each criterion:
1. request.json is valid JSON and represents POST /work-items/check for
   WI-DEMO-21 with status new.
2. response.json is valid JSON and represents status code 202, WI-DEMO-21, and
   state received.
3. get-request.json is valid JSON and represents GET /tickets/TICKET-77 without
   a request body.
4. get-response.json is valid JSON and contains status code 200, ticket
   TICKET-77, state waiting, and contains_real_data false.
5. Report NOT YET if any file shows an apparent credential, a non-fictional
   URL, or apparent real business data. Otherwise report only that none was
   apparent in this bounded inspection, not that none exists.

You may use only the authorised project Python file with its built-in json.tool
module to validate request.json, response.json, get-request.json, and
get-response.json in the authorised practice folder. This execution is part of
the read-only check: it may print validated JSON but must not change anything.
Do not use a bare python command. Explain NOT YET in beginner language.
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

- [ ] All four files pass local JSON validation.
- [ ] The exact Course 1 project marker and resolved Git root matched before
      project Python ran.
- [ ] Every validation used the derived project `$pythonExe`, which reports a
      stable Python 3.14 patch.
- [ ] I can identify method, path, body, response, and status code.
- [ ] I can explain why `202 Accepted` does not mean completed or correct.
- [ ] I can explain authentication versus authorisation.
- [ ] I know an API contract defines data shape and behaviour, not truth.
- [ ] No network request was made. I attest that all information I entered was
      synthetic and that I did not intentionally use a credential or real
      data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
