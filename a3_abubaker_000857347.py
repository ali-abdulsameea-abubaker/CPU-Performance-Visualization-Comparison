import matplotlib.pyplot as plt
import pandas as pd
import re
# I, Ali Abubaker 000857347 certify that this material is my original", "work. I have not shared this file. No other person's work has been used without due acknowledgement.
MAX_D = 3000
FILE_PATH = "a3_multi_core_cpu_data.txt"
# Read data
data = []
try:
    with open(FILE_PATH, "r") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                parts = re.sub(r"\(\d+%\)", "", line).split()
                if len(parts) >= 3:
                    try:
                        name = " ".join(parts[:-2])
                        cpu_mark = int(parts[-2].replace(",", ""))
                        price = float(parts[-1].replace("$", "").replace(",", "")) if parts[-1] != "NA" else None
                        if price and price <= MAX_D:
                            brand = "AMD" if "AMD" in name else "Intel"
                            data.append({"name": name, "cpu_mark": cpu_mark, "price": price, "brand": brand})
                    except (ValueError, IndexError):
                        continue
except FileNotFoundError:
    print("File not found.")
    exit()
# DataFrame
df = pd.DataFrame(data)
if df.empty or "cpu_mark" not in df.columns or "price" not in df.columns:
    print("No valid data found.")
    exit()
df["performance_per_dollar"] = df["cpu_mark"] / df["price"]
# Find best AMD and Intel CPUs
best_amd = df[df["name"].str.contains("EPYC 7763")].iloc[0] if not df[df["name"].str.contains("EPYC 7763")].empty else None
best_intel = df[df["brand"] == "Intel"].sort_values(by="cpu_mark", ascending=False).iloc[0] if not df[df["brand"] == "Intel"].empty else None
# Create plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
# Add a main title to the figure
fig.suptitle(f"Best CPU under ${MAX_D}", fontsize=16)
for ax, y_col, ylabel, title in zip([ax1, ax2], ["cpu_mark", "performance_per_dollar"], ["CPU Mark", "CPU Mark / $"], ["Performance vs. Performance/ $", "Performance vs. Cost"]):
    for brand, color, marker in [("Intel", "blue", "$In$"), ("AMD", "red", "$A$")]:
        subset = df[df["brand"] == brand]
        ax.scatter(subset["price"], subset[y_col], color=color, marker=marker, label=brand)
    ax.set_xscale("log")
    ax.set_xlabel("Price in USD", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(f"{title} (MAX_D = ${MAX_D})", fontsize=14)
    ax.set_xticks([50, 100, 250, 500, 1000, 2500, 5000])
    ax.set_xticklabels(["50", "100", "250", "500", "1000", "2500", "5000"], fontsize=10)
    ax.legend(loc="upper left", fontsize=12)
# Add annotations for best CPUs
for best_cpu in [best_amd, best_intel]:
    if best_cpu is not None:
        for ax, y_col in zip([ax1, ax2], ["cpu_mark", "performance_per_dollar"]):
            annotation_text = f"{best_cpu['name']} ${best_cpu['price']}"
            ax.annotate(
                annotation_text,
                xy=(best_cpu["price"], best_cpu[y_col]),
                xytext=(best_cpu["price"] * 1.1, best_cpu[y_col] * 1.1),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="gray"),
                fontsize=10
            )
# Note: CPU selection may also depend on factors like built-in graphics support, available memory, or motherboard configurations.
plt.tight_layout()
plt.show()