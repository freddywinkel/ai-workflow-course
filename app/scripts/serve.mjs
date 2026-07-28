import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import { extname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const outputRoot = resolve(
  process.env.COURSE_DIST_PATH ||
    fileURLToPath(new URL("../dist", import.meta.url)),
);
const port = Number(process.env.PORT || 4173);
const basePath = `/${String(process.env.BASE_PATH || "/ai-workflow-course/")
  .replace(/^\/+|\/+$/g, "")}/`;
const mimeTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".webmanifest": "application/manifest+json; charset=utf-8",
};

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url || "/", `http://${request.headers.host}`);
    if (!url.pathname.startsWith(basePath)) {
      response.writeHead(302, { Location: basePath });
      response.end();
      return;
    }
    const relativePath = decodeURIComponent(url.pathname.slice(basePath.length));
    const requestedPath = resolve(
      outputRoot,
      relativePath && !relativePath.endsWith("/") ? relativePath : "index.html",
    );
    if (
      requestedPath !== outputRoot &&
      !requestedPath.startsWith(`${outputRoot}${sep}`)
    ) {
      response.writeHead(403);
      response.end("Forbidden");
      return;
    }
    const fileStat = await stat(requestedPath);
    if (!fileStat.isFile()) throw new Error("Not a file");
    const headers = {
      "Content-Type": mimeTypes[extname(requestedPath)] || "application/octet-stream",
      "Cache-Control": requestedPath.endsWith("version.json")
        ? "no-store"
        : "no-cache",
    };
    if (requestedPath.endsWith("sw.js")) {
      headers["Service-Worker-Allowed"] = basePath;
    }
    response.writeHead(200, headers);
    if (request.method === "HEAD") response.end();
    else createReadStream(requestedPath).pipe(response);
  } catch {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("Not found");
  }
});

server.listen(port, "127.0.0.1", () => {
  process.stdout.write(`Course preview: http://127.0.0.1:${port}${basePath}\n`);
});
