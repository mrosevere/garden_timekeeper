import matplotlib.pyplot as plt

# Data from your final category counts
categories = [
    "Authentication",
    "Dashboard",
    "Summernote / Rich Text",
    "HTML Validation",
    "Data Integrity",
    "Forms & UX",
    "Responsive UI",
    "Deployment",
    "Code Quality",
    "Routing / Templates"
]

counts = [8, 11, 6, 7, 4, 5, 3, 2, 3, 3]

# Professional, clean colour palette
colors = [
    "#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974",
    "#64B5CD", "#8C8C8C", "#E17C05", "#937860", "#5DA5DA"
]

plt.figure(figsize=(10, 10))
plt.pie(
    counts,
    labels=categories,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    textprops={"fontsize": 12}
)

plt.title("Garden Timekeeper — Bugs by Category", fontsize=16, pad=20)
plt.tight_layout()

# Save the image
plt.savefig("bugs_by_category.png", dpi=300)

# Show the chart
plt.show()
