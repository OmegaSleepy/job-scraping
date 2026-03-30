const api = typeof browser !== "undefined" ? browser : chrome;
const ROOT_SELECTOR = "#listContainer";

// ------------------------
// Skill normalization (optional but useful)
function normalizeSkill(skill) {
 const map = {
  "node.js": "node",
  "postgresql": "postgres",
  "js": "javascript",
  "английски": "english",
  "немски": "german"
 };

 return map[skill] || skill;
}

window.addEventListener("keydown", (e) => {
 if (e.ctrlKey && e.shiftKey && e.key === "n") {
  downloadJobsAsJSON('json');
 }
});
function injectDownloadButton() {
 const btn = document.createElement("button");
 btn.innerText = "Download JSON";
 btn.style.position = "fixed";
 btn.style.bottom = "20px";
 btn.style.right = "20px";
 btn.style.zIndex = "9999";
 btn.style.padding = "10px 15px";
 btn.style.backgroundColor = "#4CAF50";
 btn.style.color = "white";
 btn.style.border = "none";
 btn.style.borderRadius = "5px";
 btn.style.cursor = "pointer";

 btn.onclick = downloadJobsAsJSON;
 document.body.appendChild(btn);
}

injectDownloadButton();


// ------------------------
// 2. Updated Extraction Logic
// ------------------------
function extractJob(el) {
 const link = el.querySelector("a.black-link-b");
 let rawTitle = link?.innerText || "";

 // Clean Position: Remove icons, take first line, and strip leading language keywords
 let position = rawTitle
  .replace(/(star(_half)?|location_on|chair|3p|groups|person_add|work_outline)/g, "")
  .split("\n")[0]
  .replace(/^(python|javascript|js|java|php|c#|\.net|react|angular|vue|node|html\/css|html|css)\s+/i, "")
  .trim();

 // Clean Location: Map "Дистанционна работа" to "Fully Remote"
 let rawLocation = el.querySelector(".card-info")?.innerText || "";
 let location = rawLocation.split(";")[0].replace("location_on", "").trim();
 if (location.includes("Дистанционна работа")) {
  location = "Fully Remote";
 }

 const companyName = el.querySelector(".secondary-text")?.innerText.trim() || null;

 // Clean Requirements: Normalize, then split "html/css" into two separate entries
 let req = Array.from(el.querySelectorAll(".skill img"))
  .map(img => img.alt?.toLowerCase())
  .filter(Boolean)
  .map(normalizeSkill)
  .flatMap(skill => {
   // If skill is "html/css", return ["html", "css"], otherwise [skill]
   return skill.includes("/") ? skill.split("/") : [skill];
  });

 return {
  category: "Software Development",
  companyName,
  position,
  location,
  req,
  date: "Today",
  url: link?.href || null
 };
}

// ------------------------
// 3. Updated Process Function (The Guard Clause)
// ------------------------
function process() {
 const root = document.querySelector(ROOT_SELECTOR);
 if (!root) return;

 const items = root.querySelectorAll("ul > li");
 let results = [];

 items.forEach(el => {
  if (el.dataset.processed) return;
  if (!isRealJob(el)) return;

  el.dataset.processed = "true";
  const job = extractJob(el);

  if (!job.url || seen.has(job.url)) return;
  seen.add(job.url);

  // Fix: Using job.req instead of job.skills
  if (!job.req || job.req.length === 0) return;

  results.push(job);
  markAsRead(el);
 });

 if (results.length > 0) {
  api.storage.local.get("jobs").then(res => {
   const existing = res.jobs || [];
   return api.storage.local.set({ jobs: existing.concat(results) });
  });
 }
}
/**
 * Fetches all jobs from local storage and triggers a .json file download
 */
/**
 * Fetches jobs, sends them to background for download, and clears local storage
 */
function downloadJobsAsJSON() {
 api.storage.local.get("jobs").then(res => {
  const jobs = res.jobs || [];

  if (jobs.length === 0) {
   alert("No new jobs to download!");
   return;
  }

  // 1. Send the data to the background script
  api.runtime.sendMessage({
   action: "download_json",
   data: jobs
  });

  // 2. Clear the storage so the next download is "fresh"
  api.storage.local.set({ jobs: [] }).then(() => {
   console.log("Storage cleared after download.");
  });

  // 3. Clear the 'seen' Set so previously processed jobs
  // on the current page can be re-scanned if necessary
  seen.clear();

  alert(`Exporting ${jobs.length} jobs. Storage has been reset.`);
 }).catch(err => {
  console.error("Error during download/clear cycle:", err);
 });
}

// Call this from your button or console
function triggerDownload() {
 api.storage.local.get("jobs").then(res => {
  const jobs = res.jobs || [];
  if (jobs.length > 0) {
   api.runtime.sendMessage({
    action: "download_json",
    data: jobs
   });
  } else {
   console.log("No jobs found in storage.");
  }
 });
}

// ------------------------
// Filter valid job elements
// ------------------------
function isRealJob(el) {
 if (el.classList.contains("edu-links")) return false;
 return el.querySelector("a");

}

// ------------------------
// Hide element safely (no freezing)
// ------------------------
function markAsRead(el) {
 if (el.dataset.read) return;

 el.dataset.read = "true";

 el.style.opacity = "0.4";
 el.style.border = "2px solid #4CAF50";
 el.style.backgroundColor = "#f0fdf4"; // light green
}

// ------------------------
// Deduplication (by URL)
// ------------------------
const seen = new Set();

// ------------------------
// Initial run
// ------------------------
process();

// ------------------------
// Observe dynamic loading (infinite scroll / SPA)
// ------------------------
const observer = new MutationObserver(() => process());

observer.observe(document.body, {
 childList: true,
 subtree: true
});