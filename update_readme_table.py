"""
Regenerates the dataset table in README.md from datasets.csv.
Only the content between <!-- TABLE:START --> and <!-- TABLE:END -->
is replaced -- everything else in the README is left untouched.
"""
import csv
import re

CSV_PATH = "datasets.csv"
README_PATH = "README.md"

# Columns to show in the README preview table (kept short and scannable).
# Full details (tasks, publication, license, channels, etc.) stay in the CSV.
DISPLAY_COLUMNS = ["Dataset Name", "Year", "Country", "EEG headset", "N", "dataset url"]
DISPLAY_HEADERS = ["Dataset", "Year", "Country", "Headset", "N", "Link"]


def build_table(csv_path: str) -> str:
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    header, *data = rows
    idx = {name: i for i, name in enumerate(header)}

    lines = [
        "| " + " | ".join(DISPLAY_HEADERS) + " |",
        "|" + "|".join(["---"] * len(DISPLAY_HEADERS)) + "|",
    ]
    for row in data:
        cells = []
        for col in DISPLAY_COLUMNS:
            value = row[idx[col]] if col in idx else ""
            if col == "dataset url" and value:
                value = f"[Link]({value})"
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def update_readme(readme_path: str, table_md: str) -> None:
    with open(readme_path, encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r"(<!-- TABLE:START -->\n)(.*?)(\n<!-- TABLE:END -->)",
        re.DOTALL,
    )
    if not pattern.search(content):
        raise ValueError(
            "Could not find <!-- TABLE:START --> / <!-- TABLE:END --> "
            "markers in README.md"
        )

    new_content = pattern.sub(rf"\1{table_md}\3", content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    table_md = build_table(CSV_PATH)
    update_readme(README_PATH, table_md)
    print("README.md table updated.")
