import json
import os
from collections import Counter
import matplotlib.pyplot as plt

# -----------------------
# Configuration
# -----------------------
DATA_FOLDER = "./data"  # folder containing your 13 JSON files
CITIES = ["София", "Пловдив", "Варна", "Бургас", "Русе", "Стара Загора"]
OUTPUT_FOLDER_ALL = "./plots"                 # for overall charts
OUTPUT_FOLDER_BY_CATEGORY = "./plots_by_category"  # for per-category skill charts
IGNORE_SKILLS = {"english"}  # skills to ignore in counting (case-insensitive)

# -----------------------
# Helper Functions
# -----------------------
def clean_location(raw_location: str) -> str:
    if not raw_location:
        return "Unknown"

    raw_location = raw_location.strip()

    if "Hybrid" in raw_location or "Комбиниран" in raw_location:
        return "Hybrid"

    for city in CITIES:
        if city in raw_location:
            return city

    if "Remote" in raw_location or "дистанционно" in raw_location.lower():
        return "Remote"

    return "Other"

def load_all_data(folder):
    all_jobs = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                all_jobs.extend(data)
    return all_jobs

def plot_bar(counter, title, top_n=10, output_folder="./plots"):
    items = counter.most_common(top_n)
    if not items:
        print(f"No data to plot for {title}")
        return

    labels, values = zip(*items)
    plt.figure(figsize=(10, 6))
    plt.barh(labels, values, color='skyblue')
    plt.title(title, fontsize=14)
    plt.xlabel("Count")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(output_folder, f"{title.replace(' ', '_')}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Saved plot: {filename}")

# -----------------------
# Main Script
# -----------------------
def main():
    jobs = load_all_data(DATA_FOLDER)

    # Overall counters
    skill_counter = Counter()
    location_counter = Counter()
    category_counter = Counter()

    # Skill breakdown by category
    skills_by_category = {}

    for job in jobs:
        category = job.get("category", "Unknown")

        # Count skills (filter out English)
        for skill in job.get("req", []):
            if skill.lower() in IGNORE_SKILLS:
                continue  # skip English
            skill_counter[skill] += 1
            if category not in skills_by_category:
                skills_by_category[category] = Counter()
            skills_by_category[category][skill] += 1

        loc = clean_location(job.get("location", ""))
        location_counter[loc] += 1

        category_counter[category] += 1

    # -----------------------
    # Overall charts
    # -----------------------
    plot_bar(skill_counter, "Top Skills", top_n=15, output_folder=OUTPUT_FOLDER_ALL)
    plot_bar(location_counter, "Job Locations", top_n=10, output_folder=OUTPUT_FOLDER_ALL)
    plot_bar(category_counter, "Job Categories", top_n=13, output_folder=OUTPUT_FOLDER_ALL)

    # -----------------------
    # Per-category skill charts
    # -----------------------
    for category, counter in skills_by_category.items():
        plot_bar(counter, f"Top Skills - {category}", top_n=15, output_folder=OUTPUT_FOLDER_BY_CATEGORY)

if __name__ == "__main__":
    main()