# Foundation 4 — Application Programming Interfaces (APIs), Hypertext Transfer Protocol (HTTP), and JavaScript Object Notation (JSON)

## Outcome

You will create a fictional request and response, validate both JSON files
locally, and explain why an accepted request is not the same as completed or
correct work.

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
  read-only check. The check prompt limits it to one practice folder.

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
whenever you start or resume Foundation 4:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$projectRoot = Join-Path $documentsPath "AI-workflow-learning\operations-exception-assistant"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonPath = Join-Path $practiceRoot "foundation-04"

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
    throw "STOP: foundation-04 is a file, not a folder. Do not rename or delete it; ask Codex to inspect read-only."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new foundation-04 folder."
}
else {
    "Existing foundation-04 folder found; nothing was overwritten."
}

Set-Location -LiteralPath $lessonPath
Get-Location
$pythonExe
$pythonVersion
Get-ChildItem -Force
```

This derives the exact project interpreter from your real Documents path,
checks that it exists, accepts only a stable Python 3.14 patch, creates the
lesson folder only when it is absent, and shows any existing content before
you edit. The displayed executable path must end in
`AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`,
and the current location must end in
`controlled-ai-course-practice\foundation-04`.

If existing files are listed, inspect them before continuing. Resume only your
own synthetic lesson attempt. Do not overwrite unfamiliar material and do not
use a folder containing real data.

### Part B — create a fictional request

1. Run:

   ```powershell
   notepad "request.json"
   ```

2. If Notepad asks whether to create the file, click **Yes**.
3. Type or paste:

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

4. Click **File > Save**, then close Notepad.

What this represents: a fictional client asks the endpoint
`POST /work-items/check` to accept metadata for one synthetic work item.
Nothing is sent to a server.

### Part C — create a fictional response

1. Run:

   ```powershell
   notepad "response.json"
   ```

2. Enter:

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
- If `foundation-04` already exists, do not delete it. Enter it and confirm it
  contains only synthetic practice.

## Now recreate it yourself

Create two different valid JSON files in `foundation-04`:

1. `get-request.json` representing:
   - method `GET`;
   - path `/tickets/TICKET-77`;
   - no request body.
2. `get-response.json` representing:
   - status code `200`;
   - a body containing ticket ID `TICKET-77`;
   - state `waiting`;
   - Boolean field `contains_real_data` set to `false`.

Choose a clear JSON object shape yourself. Validate both files with the exact
project interpreter:

```powershell
& $pythonExe -m json.tool ".\get-request.json"
& $pythonExe -m json.tool ".\get-response.json"
```

Do not reuse `WI-DEMO-21`, `POST`, or state `received`.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, or delete anything. Do not contact an
external service or run any command that changes files or settings.

Report PASS or NOT YET for each criterion:
1. request.json is valid JSON and represents POST /work-items/check for
   WI-DEMO-21 with status new.
2. response.json is valid JSON and represents status code 202, WI-DEMO-21, and
   state received.
3. get-request.json is valid JSON and represents GET /tickets/TICKET-77 without
   a request body.
4. get-response.json is valid JSON and contains status code 200, ticket
   TICKET-77, state waiting, and contains_real_data false.
5. None of the files contains a credential, real URL, or real business data.

You may derive only
Documents\AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe
and use that exact executable with its built-in json.tool module as a
read-only JSON validator. Do not use a bare python command. Explain NOT YET in
beginner language and make no changes.
This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] All four files pass local JSON validation.
- [ ] Every validation used the derived project `$pythonExe`, which reports a
      stable Python 3.14 patch.
- [ ] I can identify method, path, body, response, and status code.
- [ ] I can explain why `202 Accepted` does not mean completed or correct.
- [ ] I can explain authentication versus authorisation.
- [ ] I know an API contract defines data shape and behaviour, not truth.
- [ ] No network request, credential, or real data was used.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
