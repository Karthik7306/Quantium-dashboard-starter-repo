import csv
import glob

csv_files = glob.glob("data/*.csv")
print("Files found:", csv_files)

all_data = []

for file in csv_files:
    print("Processing:", file)
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["product"].strip() == "Pink Morsels":
                try:
                    sales = int(row["quantity"]) * float(row["price"])
                    all_data.append({
                        "Sales": sales,
                        "Date": row["date"],
                        "Region": row["region"]
                    })
                except Exception as e:
                    print("Problem with row:", row, e)

with open("data_file.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Sales", "Date", "Region"])
    writer.writeheader()
    writer.writerows(all_data)

print("Done. See data_file.csv.")
