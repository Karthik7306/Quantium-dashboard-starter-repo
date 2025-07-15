import csv
import glob

csv_files = glob.glob("data/*.csv")
data = []

for filename in csv_files:
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["product"] == "Pink Morsels":
                quantity = int(row["quantity"])
                price = float(row["price"])
                sales = quantity * price
                data.append({"Sales": sales, "Date": row["date"], "Region": row["region"]})
                
fields = ['Sales', 'Date', 'Region']

with open("data_file.csv", "w", newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames = fields)
    writer.writeheader()
    writer.writerows(data)
