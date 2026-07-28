const fileInput = document.querySelector("#document-file");
const syntheticCheck = document.querySelector("#synthetic-check");
const processButton = document.querySelector("#process-button");
const processStatus = document.querySelector("#process-status");
const reviewPanel = document.querySelector("#review-panel");
const decisionPanel = document.querySelector("#decision-panel");
const exportPanel = document.querySelector("#export-panel");
const decisionButton = document.querySelector("#decision-button");
const decisionStatus = document.querySelector("#decision-status");

let intakeResult = null;
let approvedExports = null;

function setText(selector, value) {
  document.querySelector(selector).textContent = String(value ?? "—");
}

function clearChildren(element) {
  while (element.firstChild) element.firstChild.remove();
}

function appendListItem(list, text, sourceIds = []) {
  const item = document.createElement("li");
  const copy = document.createElement("span");
  copy.textContent = text;
  item.append(copy);
  if (sourceIds.length) {
    const source = document.createElement("code");
    source.textContent = sourceIds.join(", ");
    item.append(source);
  }
  list.append(item);
}

function renderPackage(packageData) {
  setText("#case-id", packageData.case_id);
  setText("#run-state", packageData.state.replaceAll("_", " "));
  setText("#page-count", packageData.page_count);
  setText(
    "#provider-mode",
    packageData.processing_proof.provider_mode === "google"
      ? `${packageData.processing_proof.model_id} · European Union`
      : "Offline fake adapters",
  );

  const fieldRows = document.querySelector("#field-rows");
  clearChildren(fieldRows);
  for (const field of packageData.fields) {
    const row = document.createElement("tr");
    for (const value of [
      field.field_name,
      field.value ?? "Not found",
      field.status,
      field.evidence_ids.join(", ") || "No source",
    ]) {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.append(cell);
    }
    fieldRows.append(row);
  }

  const evidenceList = document.querySelector("#evidence-list");
  clearChildren(evidenceList);
  for (const evidence of packageData.evidence) {
    appendListItem(
      evidenceList,
      `Page ${evidence.page_number}: “${evidence.exact_quote}”`,
      [evidence.evidence_id],
    );
  }

  const summaryList = document.querySelector("#summary-list");
  clearChildren(summaryList);
  for (const statement of packageData.ai_draft.summary) {
    appendListItem(summaryList, statement.text, statement.evidence_ids);
  }

  const actionList = document.querySelector("#action-list");
  clearChildren(actionList);
  for (const action of packageData.ai_draft.proposed_actions) {
    appendListItem(
      actionList,
      `${action.action_type.replaceAll("_", " ")}: ${action.instruction}`,
      action.evidence_ids,
    );
  }

  const findingBox = document.querySelector("#finding-box");
  const findingList = document.querySelector("#finding-list");
  clearChildren(findingList);
  findingBox.hidden = packageData.findings.length === 0;
  for (const finding of packageData.findings) {
    appendListItem(findingList, finding);
  }

  reviewPanel.hidden = false;
  decisionPanel.hidden = false;
  exportPanel.hidden = true;
  decisionPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

function refreshProcessButton() {
  processButton.disabled = !(fileInput.files.length && syntheticCheck.checked);
}

fileInput.addEventListener("change", refreshProcessButton);
syntheticCheck.addEventListener("change", refreshProcessButton);

processButton.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file || !syntheticCheck.checked) return;
  processButton.disabled = true;
  processStatus.className = "status";
  processStatus.textContent = "Applying the allowlist and controlled pipeline…";
  intakeResult = null;
  approvedExports = null;
  reviewPanel.hidden = true;
  decisionPanel.hidden = true;
  exportPanel.hidden = true;

  try {
    const response = await fetch("/api/intake", {
      method: "POST",
      headers: {
        "Content-Type": "application/pdf",
        "X-Synthetic-Acknowledged": "true",
      },
      body: file,
      cache: "no-store",
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(
        `${payload.error?.code ?? "SAFE_STOP"}: ${
          payload.error?.message ?? "The intake stopped safely."
        }`,
      );
    }
    intakeResult = payload;
    processStatus.className = "status status-good";
    processStatus.textContent =
      "Draft ready. The temporary source file was deleted; inspect the evidence.";
    renderPackage(payload.package);
  } catch (error) {
    processStatus.className = "status status-error";
    processStatus.textContent = error.message;
  } finally {
    refreshProcessButton();
  }
});

decisionButton.addEventListener("click", async () => {
  if (!intakeResult) return;
  decisionButton.disabled = true;
  decisionStatus.className = "status";
  decisionStatus.textContent = "Recording the decision against the exact hash…";
  exportPanel.hidden = true;
  approvedExports = null;

  try {
    const response = await fetch("/api/decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        package: intakeResult.package,
        package_signature: intakeResult.package_signature,
        decision: document.querySelector("#decision").value,
        reviewer_alias: document.querySelector("#reviewer-alias").value,
        source_links_checked: document.querySelector("#source-review-check").checked,
        comment: document.querySelector("#decision-comment").value,
      }),
      cache: "no-store",
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(
        `${payload.error?.code ?? "SAFE_STOP"}: ${
          payload.error?.message ?? "The decision stopped safely."
        }`,
      );
    }
    if (payload.approval.approved_for_export) {
      approvedExports = payload;
      exportPanel.hidden = false;
      exportPanel.scrollIntoView({ behavior: "smooth", block: "start" });
      decisionStatus.className = "status status-good";
      decisionStatus.textContent =
        "Exact output approved. CSV and JSON downloads are now available.";
    } else {
      decisionStatus.className = "status";
      decisionStatus.textContent =
        "Decision recorded. No export was created because this draft was not approved.";
    }
  } catch (error) {
    decisionStatus.className = "status status-error";
    decisionStatus.textContent = error.message;
  } finally {
    decisionButton.disabled = false;
  }
});

function downloadText(text, mimeType, extension) {
  if (!approvedExports || !intakeResult) return;
  const blob = new Blob([text], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${intakeResult.package.case_id}-controlled-intake.${extension}`;
  link.click();
  URL.revokeObjectURL(url);
}

document.querySelector("#json-button").addEventListener("click", () => {
  downloadText(approvedExports?.json_export, "application/json", "json");
});

document.querySelector("#csv-button").addEventListener("click", () => {
  downloadText(approvedExports?.csv_export, "text/csv;charset=utf-8", "csv");
});
