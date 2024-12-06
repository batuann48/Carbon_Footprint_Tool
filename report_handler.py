import os
import pandas as pd 


def save_to_csv(data, filename="carbon_data.csv"):
    """saves data to in CSV file . Creates file if it does not exists. """
    # If the file does not exist , create a new DataFrame by adding the headers

    if not os.path.exists(filename):
        df = pd.DataFrame(columns=["Name","Year","Electricity (kg CO2)", "Waste (kg CO2)","Travel (kg CO2)", "Total (kg CO2)"])
        df.to_csv(filename,index=False)

    else:
        # Add to current file.
        df = pd.read_csv(filename)

    #New data add to DataFrame.
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    #Save to CSV file.
    df.to_csv(filename, index=False)
