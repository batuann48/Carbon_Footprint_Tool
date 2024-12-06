import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_carbon_footprint(filename="carbon_data.csv", output_file="static/graph.png"):

    """
       Creates a bar chart by reading data from CSV.
       Includes Name and Year information in the x-axis labels,sorted by Year in ascending order."""

    print(f"Graph rendering started: {filename}")


    # Read to CSV file.
    if not os.path.exists(filename):
        print(f"{filename} not found.Could not create Graph.")
        return
    
    try:


        df = pd.read_csv(filename)
        print("CSV file read successfully.")

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # If data not in the file , give error.
    if df.empty:
        print("No data found in CSV file.Could not create chart.")
        return
    
    # Ensure "name" and "year" column exist
    if "Name" not in df.columns or "Year" not in df.columns:
        print("Required columns 'Name' and 'Year' are missing in the CSV file.")
        return
    
    df = df.sort_values(by="Year")
    
    #combine name and year for x-axis labels.

    x_labels = df["Name"] + " (" + df["Year"].astype(str) + ")"

    #Create a total carbon footprint chart from the data.

    try:
        print("Creating graph.")
        plt.figure(figsize=(12,6))

        plt.bar(x_labels, df["Total (kg CO2)"], color = "skyblue")
        plt.xlabel("Name (Year)")
        plt.ylabel("Total Carbon Footprint (kg CO2)")
        plt.title("Carbon Footprint Overview")

        plt.xticks(rotation=45, ha="right", fontsize=10)

    # adjust layout to avoid label overlap
        plt.tight_layout()   

    # Save Static graph file.

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.savefig(output_file, bbox_inches="tight")
        plt.close()

        print(f"Graph successfully created: {output_file}")

    except Exception as e:
        print(f"Error reading CSV file: {e}")



    if __name__ == "__main__":
        plot_carbon_footprint()


