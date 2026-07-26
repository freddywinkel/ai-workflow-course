# Foundation 1 — Files, Folders, Paths, and Text

## Outcome

You can locate a file, recognise its type, create a safe practice folder, and
edit plain text without accidentally changing a file extension.

## The basic mental model

A **folder** holds files and other folders. A **file** is stored information. A
**path** is the address of a file or folder.

Example Windows path:

```text
C:\Users\YourName\Documents\controlled-ai-workflow\README.md
```

Read it from left to right:

- `C:` is a drive;
- each backslash enters another folder;
- `README.md` is the file;
- `.md` is its extension.

A full path starts at a drive. A relative path starts at the folder you are
currently using. If your current folder is
`C:\Users\YourName\Documents\controlled-ai-workflow`, then `docs\runbook.md` is
relative to it.

## File types used in this course

These are all plain text unless stated otherwise:

| Extension | Purpose | Important rule |
|---|---|---|
| `.md` | Notes and documentation using Markdown | safe to read in any text editor |
| `.py` | Python source code | running it can change files or call services |
| `.json` | Strict machine-readable data | quotes, commas, and brackets must be exact |
| `.jsonl` | One complete JSON object per line | one broken line can fail a dataset |
| `.yaml` / `.yml` | Indented configuration | spaces and indentation matter |
| `.env` | local secret/configuration values | never commit the real file |
| `.sql` | database instructions | review before execution |
| `.pdf` / `.docx` | source documents | binary formats; do not edit as plain text |

Turn on file-name extensions in Windows Explorer: **View → Show → File name
extensions**. This prevents `notes.md.txt` from masquerading as `notes.md`.

## Markdown is just text

This:

```markdown
# Heading

- first item
- second item

**Important:** review the evidence.
```

is stored as text and rendered with formatting. Markdown is documentation, not
executable code.

## Configuration is not prose

JSON is strict:

```json
{
  "state": "received",
  "retry_count": 0,
  "approved": false,
  "error": null
}
```

The values mean:

- `"received"`: text, also called a string;
- `0`: a number;
- `false`: a Boolean value;
- `null`: deliberately no value.

Do not add comments to JSON. Do not use a curly “smart quote” in place of `"`.

YAML uses indentation:

```yaml
model:
  id: configured-at-runtime
  store: false
```

An `.env` file normally uses one `NAME=value` pair per line:

```dotenv
APP_ENV=dev
KILL_SWITCH=true
```

The course commits `.env.example` with empty or harmless example values. The
real `.env` stays local and ignored by Git.

## Practice

Use Windows Explorer for this exercise:

1. Create `Documents\course-practice`.
2. Inside it, create `notes.md`.
3. Add a heading, a three-item list, and today's date.
4. Create `example.json` containing the JSON example above.
5. Confirm Explorer displays the extensions `.md` and `.json`.
6. Open both files again and confirm their contents survived.

Do not use real names, credentials, customer information, or source documents.

## Chapter check

Without looking back, explain:

1. the difference between a full and relative path;
2. why `notes.md.txt` is not a Markdown file;
3. why `.env.example` may be committed but `.env` may contain secrets;
4. why a missing comma can break JSON while ordinary prose remains readable.
