# Data Dictionary and Quality Check

Artifact ID:
Version/date:
Author/reviewer:
Dataset name/version:
Intended purpose:
System of record:
Source/export time:
Dataset status: FICTIONAL / REAL-DATA REVIEW REQUIRED

Course 1 permits only fictional or supplied synthetic data. If status is not
FICTIONAL, stop.

## Dataset boundary

Unit represented by one row/object:
Expected row count/range:
Unique identifier:
Permitted files/formats:
Untouched source location/hash:
Working-copy location:
Data owner role:
Access roles:
Retention/deletion rule:

## Data dictionary

| Field | Plain meaning | Type/format | Required? | Allowed values/range | Meaning of blank | Source | Owner | Sensitivity |
|---|---|---|:---:|---|---|---|---|---|
| | | | | | | | | |

Do not infer that blank means zero, false, or not applicable.

## Quality rule register

| Rule code | Dimension | Exact check | Fields | Severity | Failure/review route | Test case/evidence |
|---|---|---|---|---|---|---|
| R001 | completeness | | | | | |

Dimensions: completeness, validity, consistency, uniqueness, and timeliness.
Run format validation before comparisons that depend on a valid date or number.

## Input profile

| Check | Expected | Observed | Pass? | Evidence/issue |
|---|---:|---:|:---:|---|
| Row count | | | | |
| Column/header count | | | | |
| Unique IDs | | | | |
| Missing required values | | | | |
| Invalid formats/enums | | | | |
| Duplicate references | | | | |
| Date/amount range | | | | |
| Unexpected extra fields | | | | |

## Transformations and provenance

| Step/version | Input | Transformation | Output | Changed by | Reversible? | Verification |
|---|---|---|---|---|:---:|---|
| | | | | | | |

Source values corrected automatically? **No**
If a correction is proposed, where is it reviewed and recorded?

## Quality result

| Severity | Issue count | Owner/route | Blocks next stage? |
|---|---:|---|:---:|
| High | | | |
| Medium | | | |
| Low | | | |

Known blind spots:
Fields unsuitable for AI:
Human interpretation still required:
Decision: ACCEPT FOR SYNTHETIC TEST / REVISE / QUARANTINE
Reviewer/date:
