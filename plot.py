import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# -----------------------
# Configuration
# -----------------------
DATA_FOLDER = "./data"
CITIES = ["София", "Пловдив", "Варна", "Бургас", "Русе", "Стара Загора"]
OUTPUT_FOLDER_ALL = "./plots"
OUTPUT_FOLDER_BY_CATEGORY = "./plots_by_category"
IGNORE_SKILLS = {"english"}

# Use a professional, clean style
plt.style.use('seaborn-v0_8-whitegrid')

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
    if not os.path.exists(folder):
        print(f"Directory {folder} not found.")
        return []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                all_jobs.extend(data)
    return all_jobs

def plot_bar(counter, title, top_n=10, output_folder="./plots"):
    # Ensure all labels are Title Case for "Capital Letter" format
    items = [(str(k).title(), v) for k, v in counter.most_common(top_n)]

    if not items:
        print(f"No data to plot for {title}")
        return

    labels, values = zip(*items)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create a nice color gradient from dark blue to light blue
    colors = plt.cm.Blues(np.linspace(0.8, 0.4, len(values)))

    bars = ax.barh(labels, values, color=colors, edgecolor='white', linewidth=1)

    # Titles and labels
    ax.set_title(title.title(), fontsize=18, fontweight='bold', pad=25, color='#2c3e50')
    ax.set_xlabel("Frequency (Count)", fontsize=12, labelpad=10, fontweight='semibold')
    ax.invert_yaxis()  # Put the highest value at the top

    # Remove chart borders for a modern look
    for spine in ['top', 'right', 'bottom']:
        ax.spines[spine].set_visible(False)

    # Add vertical gridlines for easier scanning
    ax.xaxis.grid(True, linestyle='--', alpha=0.6)
    ax.set_axisbelow(True)

    # Calculate and add labels + percentage differences
    max_val = max(values)
    for i, bar in enumerate(bars):
        width = bar.get_width()

        # Calculate % difference from the bar above it
        diff_text = ""
        if i > 0:
            prev_width = bars[i-1].get_width()
            if prev_width > 0:
                diff = ((width - prev_width) / prev_width) * 100
                # Show percentage drop (e.g., -15.4%)
                diff_text = f" ({diff:+.1f}%)"

        # Position text slightly to the right of the bar
        ax.text(width + (max_val * 0.01),
                bar.get_y() + bar.get_height()/2,
                f'{int(width)}{diff_text}',
                va='center',
                ha='left',
                fontsize=11,
                fontweight='bold',
                color='#34495e')

    plt.tight_layout()

    os.makedirs(output_folder, exist_ok=True)
    # Sanitize filename (remove characters that might break file paths)
    safe_title = title.replace(' ', '_').replace('/', '_').replace('-', '_')
    filename = os.path.join(output_folder, f"{safe_title}.png")

    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved enhanced plot: {filename}")

# -----------------------
# Main Script
# -----------------------
def main():
    jobs = load_all_data(DATA_FOLDER)
    if not jobs:
        return

    skill_counter = Counter()
    location_counter = Counter()
    category_counter = Counter()
    skills_by_category = {}

    for job in jobs:
        category = job.get("category", "Unknown")

        # Process skills
        for skill in job.get("req", []):
            if skill.lower() in IGNORE_SKILLS:
                continue
            skill_counter[skill] += 1
            if category not in skills_by_category:
                skills_by_category[category] = Counter()
            skills_by_category[category][skill] += 1

        # Process locations
        loc = clean_location(job.get("location", ""))
        location_counter[loc] += 1

        # Process categories
        category_counter[category] += 1

    # Overall charts
    plot_bar(skill_counter, "Top Skills Required", top_n=15, output_folder=OUTPUT_FOLDER_ALL)
    plot_bar(location_counter, "Job Distribution By Location", top_n=10, output_folder=OUTPUT_FOLDER_ALL)
    plot_bar(category_counter, "Job Distribution By Category", top_n=13, output_folder=OUTPUT_FOLDER_ALL)

    # Per-category skill charts
    for category, counter in skills_by_category.items():
        plot_bar(counter, f"Top Skills For {category}", top_n=15, output_folder=OUTPUT_FOLDER_BY_CATEGORY)

if __name__ == "__main__":
    main()