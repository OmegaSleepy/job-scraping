const api = typeof browser !== "undefined" ? browser : chrome;

api.runtime.onMessage.addListener((request, sender, sendResponse) => {
 if (request.action === "download_json") {
  // 1. Create a Blob from the data
  const jsonString = JSON.stringify(request.data, null, 2);
  const blob = new Blob([jsonString], { type: "application/json" });

  // 2. Create a URL for the blob
  // In the background script, this URL is not restricted by the website's CSP
  const url = URL.createObjectURL(blob);

  // 3. Trigger the download
  api.downloads.download({
   url: url,
   filename: `jobs_export_${Date.now()}.json`,
   saveAs: true
  }).then(() => {
   // 4. Clean up memory after download starts
   setTimeout(() => URL.revokeObjectURL(url), 10000);
  }).catch(err => {
   console.error("Download failed:", err);
   URL.revokeObjectURL(url);
  });
 }
});

// Extension icon click handler
(api.browserAction || api.action).onClicked.addListener((tab) => {
 api.tabs.executeScript(tab.id, { file: "content.js" });
});