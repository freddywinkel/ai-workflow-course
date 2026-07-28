const TASK_CHECK_ICON =
  '<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m5 12.5 4.2 4.2L19 7"/></svg>';

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

function safeLink(value) {
  const href = String(value).trim();
  if (
    href.startsWith("#") ||
    href.startsWith("/") ||
    href.startsWith("./") ||
    href.startsWith("../") ||
    /^[a-zA-Z0-9_.-]+(?:\/[a-zA-Z0-9_.#?&=%-]+)*$/.test(href)
  ) {
    return href;
  }
  try {
    const url = new URL(href);
    if (["https:", "http:", "mailto:"].includes(url.protocol)) return href;
  } catch {
    // Invalid or unsafe links become inert text targets.
  }
  return "#unsafe-link";
}

function renderInline(rawValue) {
  const tokens = [];
  let value = String(rawValue);

  value = value.replace(/`([^`\n]+)`/g, (_match, code) => {
    const token = `\u0000CODE${tokens.length}\u0000`;
    tokens.push(`<code>${escapeHtml(code)}</code>`);
    return token;
  });

  value = value.replace(/\[([^\]\n]+)\]\(([^)\n]+)\)/g, (_match, label, rawHref) => {
    const href = rawHref.trim().replace(/\s+"[^"]*"$/, "");
    const safe = safeLink(href);
    const external = /^https?:\/\//i.test(safe);
    const token = `\u0000LINK${tokens.length}\u0000`;
    tokens.push(
      `<a href="${escapeAttribute(safe)}"${external ? ' target="_blank" rel="noopener noreferrer"' : ""}>${escapeHtml(label)}</a>`,
    );
    return token;
  });

  value = value.replace(/<(https:\/\/[^<>\s]+)>/gi, (_match, rawHref) => {
    const safe = safeLink(rawHref);
    const token = `\u0000LINK${tokens.length}\u0000`;
    tokens.push(
      `<a href="${escapeAttribute(safe)}" target="_blank" rel="noopener noreferrer">${escapeHtml(rawHref)}</a>`,
    );
    return token;
  });

  // Protect strong spans before parsing emphasis. A label such as
  // **All files (*.*)** contains literal asterisks inside the bold text. If
  // those asterisks reach the emphasis expressions below, the visible file
  // picker label is silently changed.
  for (const [expression, tag] of [
    [/\*\*([^\n]+?)\*\*/g, "strong"],
    [/__([^\n]+?)__/g, "strong"],
  ]) {
    value = value.replace(expression, (_match, content) => {
      const token = `\u0000STRONG${tokens.length}\u0000`;
      tokens.push(`<${tag}>${escapeHtml(content)}</${tag}>`);
      return token;
    });
  }

  value = escapeHtml(value)
    .replace(/(^|[^\w])\*([^*\n]+)\*(?!\w)/g, "$1<em>$2</em>")
    .replace(/(^|[^\w])_([^_\n]+)_(?!\w)/g, "$1<em>$2</em>");

  let rendered = value;
  for (let pass = 0; pass <= tokens.length; pass += 1) {
    const expanded = rendered.replace(
      /\u0000(?:CODE|LINK|STRONG)(\d+)\u0000/g,
      (_match, index) => tokens[Number(index)] || "",
    );
    if (expanded === rendered) break;
    rendered = expanded;
  }
  return rendered;
}

function headingId(value) {
  return value
    .toLowerCase()
    .replace(/<[^>]+>/g, "")
    .replace(/&[a-z0-9#]+;/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function indentationWidth(value) {
  let width = 0;
  for (const character of value) {
    width += character === "\t" ? 4 : 1;
  }
  return width;
}

function parseListMarker(line) {
  const match = String(line).match(/^([ \t]*)([-*+]|\d+\.)\s+(.+)$/);
  if (!match) return null;
  const ordered = /^\d+\.$/.test(match[2]);
  return {
    indent: indentationWidth(match[1]),
    ordered,
    number: ordered ? Number.parseInt(match[2], 10) : null,
    content: match[3].trim(),
  };
}

function isBlockStart(lines, index) {
  const line = lines[index] || "";
  const next = lines[index + 1] || "";
  return (
    !line.trim() ||
    /^```/.test(line.trim()) ||
    /^#{1,6}\s+/.test(line) ||
    /^>\s?/.test(line) ||
    /^[-*_]{3,}\s*$/.test(line.trim()) ||
    parseListMarker(line) !== null ||
    (line.includes("|") && /^\s*\|?[\s:|-]+\|[\s:|-|]*\s*$/.test(next))
  );
}

function splitTableRow(line) {
  return line
    .trim()
    .replace(/^\||\|$/g, "")
    .split("|")
    .map((cell) => cell.trim());
}

function startsProtectedBlock(lines, index) {
  const line = lines[index] || "";
  const trimmed = line.trim();
  const next = lines[index + 1] || "";
  return (
    /^```/.test(trimmed) ||
    /^#{1,6}\s+/.test(trimmed) ||
    /^>\s?/.test(trimmed) ||
    /^[-*_]{3,}\s*$/.test(trimmed) ||
    (line.includes("|") && /^\s*\|?[\s:|-]+\|[\s:|-|]*\s*$/.test(next))
  );
}

function renderListItem(content, nestedLists, orderedValue = "") {
  const task = content.match(/^\[([ xX])\]\s+(.+)$/);
  if (task) {
    const checked = task[1].toLowerCase() === "x";
    return `<li class="markdown-task-item"${orderedValue}><span class="markdown-task${checked ? " checked" : ""}" aria-hidden="true">${TASK_CHECK_ICON}</span><span class="markdown-task-text">${renderInline(task[2])}</span>${nestedLists.join("")}</li>`;
  }
  return `<li${orderedValue}>${renderInline(content)}${nestedLists.join("")}</li>`;
}

function renderList(lines, startIndex) {
  const first = parseListMarker(lines[startIndex]);
  if (!first) return null;

  const items = [];
  let index = startIndex;

  while (index < lines.length) {
    const marker = parseListMarker(lines[index]);
    if (
      !marker ||
      marker.indent !== first.indent ||
      marker.ordered !== first.ordered
    ) {
      break;
    }

    const continuation = [marker.content];
    const nestedLists = [];
    const expectedNumber = first.ordered ? first.number + items.length : null;
    const orderedValue =
      first.ordered && marker.number !== expectedNumber
        ? ` value="${marker.number}"`
        : "";
    index += 1;

    while (index < lines.length) {
      if (!lines[index].trim()) {
        let lookahead = index + 1;
        while (lookahead < lines.length && !lines[lookahead].trim()) {
          lookahead += 1;
        }
        const afterBlank = parseListMarker(lines[lookahead] || "");
        const afterBlankIndent = indentationWidth(
          (lines[lookahead] || "").match(/^[ \t]*/)?.[0] || "",
        );
        if (
          afterBlank &&
          afterBlank.indent >= first.indent &&
          (afterBlank.indent > first.indent ||
            afterBlank.ordered === first.ordered)
        ) {
          index = lookahead;
          continue;
        }
        if (
          lookahead < lines.length &&
          afterBlankIndent > first.indent &&
          !startsProtectedBlock(lines, lookahead)
        ) {
          index = lookahead;
          continue;
        }
        break;
      }

      const nextMarker = parseListMarker(lines[index]);
      if (nextMarker) {
        if (nextMarker.indent > first.indent) {
          const nested = renderList(lines, index);
          nestedLists.push(nested.html);
          index = nested.index;
          continue;
        }
        break;
      }

      const leadingWhitespace = lines[index].match(/^[ \t]*/)?.[0] || "";
      if (
        indentationWidth(leadingWhitespace) > first.indent &&
        !startsProtectedBlock(lines, index)
      ) {
        continuation.push(lines[index].trim());
        index += 1;
        continue;
      }
      break;
    }

    items.push(
      renderListItem(continuation.join(" "), nestedLists, orderedValue),
    );
  }

  const tag = first.ordered ? "ol" : "ul";
  const start =
    first.ordered && first.number !== 1 ? ` start="${first.number}"` : "";
  return {
    html: `<${tag}${start}>${items.join("")}</${tag}>`,
    index,
  };
}

function renderMarkdown(markdown) {
  const lines = String(markdown).replace(/\r\n?/g, "\n").split("\n");
  const output = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();

    if (!trimmed) {
      index += 1;
      continue;
    }

    const fence = trimmed.match(/^```([a-zA-Z0-9_+-]*)\s*$/);
    if (fence) {
      const language = fence[1].toLowerCase();
      const codeLines = [];
      index += 1;
      while (index < lines.length && !/^```\s*$/.test(lines[index].trim())) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length) index += 1;
      const isCommand =
        /^(powershell|shell|bash|sh|console|terminal|cmd)$/.test(language) ||
        codeLines.some((codeLine) =>
          /^(git|python|py|docker|npm|npx|winget|curl|pytest|uvicorn)\b/.test(
            codeLine.trim(),
          ),
        );
      if (isCommand) {
        output.push(
          '<p class="command-warning"><span aria-hidden="true">◇</span><span>Beginner check: confirm the current folder and understand the command before copying it.</span></p>',
        );
      }
      output.push(
        `<div class="code-block"><button class="copy-code" type="button" aria-label="Copy code block">Copy</button><pre${language ? ` data-language="${escapeAttribute(language)}"` : ""}><code>${escapeHtml(codeLines.join("\n"))}</code></pre></div>`,
      );
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const rendered = renderInline(heading[2]);
      output.push(`<h${level} id="${headingId(rendered)}">${rendered}</h${level}>`);
      index += 1;
      continue;
    }

    if (/^[-*_]{3,}\s*$/.test(trimmed)) {
      output.push("<hr>");
      index += 1;
      continue;
    }

    if (
      line.includes("|") &&
      index + 1 < lines.length &&
      /^\s*\|?[\s:|-]+\|[\s:|-|]*\s*$/.test(lines[index + 1])
    ) {
      const headers = splitTableRow(line);
      index += 2;
      const rows = [];
      while (index < lines.length && lines[index].includes("|") && lines[index].trim()) {
        rows.push(splitTableRow(lines[index]));
        index += 1;
      }
      output.push(
        `<div class="table-wrap" tabindex="0" aria-label="Scrollable table"><table><thead><tr>${headers.map((cell) => `<th scope="col">${renderInline(cell)}</th>`).join("")}</tr></thead><tbody>${rows
          .map(
            (row) =>
              `<tr>${headers.map((_header, cellIndex) => `<td>${renderInline(row[cellIndex] || "")}</td>`).join("")}</tr>`,
          )
          .join("")}</tbody></table></div>`,
      );
      continue;
    }

    if (/^>\s?/.test(line)) {
      const quoteLines = [];
      while (index < lines.length && /^>\s?/.test(lines[index])) {
        quoteLines.push(lines[index].replace(/^>\s?/, ""));
        index += 1;
      }
      output.push(`<blockquote><p>${renderInline(quoteLines.join(" "))}</p></blockquote>`);
      continue;
    }

    if (parseListMarker(line)) {
      const list = renderList(lines, index);
      output.push(list.html);
      index = list.index;
      continue;
    }

    const paragraph = [trimmed];
    index += 1;
    while (index < lines.length && !isBlockStart(lines, index)) {
      paragraph.push(lines[index].trim());
      index += 1;
    }
    output.push(`<p>${renderInline(paragraph.join(" "))}</p>`);
  }

  return output.join("\n");
}

function stripLeadingDocumentTitle(markdown) {
  return String(markdown).replace(/^(?:\uFEFF)?# [^\r\n]+(?:\r?\n){1,2}/, "");
}

export {
  escapeAttribute,
  escapeHtml,
  renderInline,
  renderMarkdown,
  safeLink,
  stripLeadingDocumentTitle,
};
