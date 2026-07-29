(() => {
  try {
    const saved = JSON.parse(
      localStorage.getItem("ai-workflow-course-state-v1") || "null",
    );
    const appearance =
      saved?.storageFormat === "ai-workflow-course-storage-v1" ? saved.state : saved;
    if (["system", "light", "dark"].includes(appearance?.theme)) {
      document.documentElement.dataset.theme = appearance.theme;
    }
  } catch {
    // The default system theme remains safe when storage is unavailable or invalid.
  }

  window.__COURSE_APP__ = Object.freeze({
    basePath: "__BASE_PATH__",
    buildId: "__BUILD_ID__",
    courseVersion: "__COURSE_VERSION__",
    sourceVerifiedThrough: "__SOURCE_VERIFIED_THROUGH__",
    contentRevisionThrough: "__CONTENT_REVISION_THROUGH__",
    verifiedThrough: "__VERIFIED_THROUGH__",
    contentHash: "__CONTENT_HASH__",
    repositoryUrl: "https://github.com/freddywinkel/ai-workflow-course",
  });
})();
