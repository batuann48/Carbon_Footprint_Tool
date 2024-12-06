
from flask import Flask, render_template ,request
from calculations import calculate_energy_usage, calculate_waste,calculate_business_travel
from report_handler import save_to_csv
from visualization import plot_carbon_footprint
from pdf_generator import generate_pdf
import pandas as pd
import os
import threading
import tkinter as tk



app = Flask(__name__)


if not os.path.exists("carbon_data.csv"):
    df = pd.DataFrame(columns=["Name","Year","Electricity (kg CO2)", "Waste (kg CO2)","Travel (kg CO2)", "Total (kg CO2)"])
    df.to_csv("carbon_data.csv",index=False)


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
      
      try:
       
        #get data from form 
         name = str(request.form.get("name","").strip())
         year = int(request.form.get("year"))
         electricity = float(request.form.get("electricity", 0))
         gas = float(request.form.get("gas", 0))
         fuel = float(request.form.get("fuel", 0))
         waste = float(request.form.get("waste", 0))
         recycling = float(request.form.get("recycling", 0))
         kilometers = float(request.form.get("kilometers", 0))
         efficiency = float(request.form.get("efficiency", 0))
         
         # Add check for each data

         if electricity < 0 or gas < 0 or fuel < 0 or waste < 0 or recycling < 0 or kilometers < 0 or efficiency <= 0:
            raise ValueError ("All inputs must be positive and fuel efficiency must be greater than zero.")



        # Perform calculations

         energy = calculate_energy_usage(electricity, gas, fuel)
         waste_impact = calculate_waste(waste,recycling)
         travel = calculate_business_travel(kilometers, efficiency)
         total_footprint = energy + waste_impact + travel


        # Prepare the data in a dictionary format.
         data = {
            "Name":name,
            "Year":year,
            "Electricity (kg CO2)": energy,
            "Waste (kg CO2)": waste_impact,
            "Travel (kg CO2)": travel,
            "Total (kg CO2)": total_footprint
         }

        # Save data to CSV file.
         with open("carbon_data.csv","a",newline="")as f:
            pd.DataFrame([data]).to_csv(f, header=False, index=False)

        # create graph

         plot_carbon_footprint()
        
        #Create a pdf and save

         generate_pdf(data)

    
        # Show results in html page

         return render_template(
            "result.html", name=name, year=year, energy=energy, waste=waste_impact, travel=travel, total=total_footprint)
      
      except ValueError as e:
        return render_template("calculate.html",error_message=str(e))
            
    return render_template("calculate.html")

           


@app.route("/data")
def data():
    try:
       df =pd.read_csv("carbon_data.csv")
       return render_template("data.html", tables=[df.to_html(classes="table table-striped", index=False)])
    
    except FileNotFoundError:
       return "No data available yet.Please calculate your carbon footprint first." 

@app.route("/graph")
def graph(): 
    try:
       
       #create graph

       plot_carbon_footprint()       
       return render_template("graph.html", graph_url="/static/graph.png")
    
    except FileNotFoundError:
       return "Error: data file not found.Please calculate your carbon footprint first."
    
    except Exception as e:
       return f"Unexpected error: {e}"

    
def run_tkinter():
   """Start the tkinter GUI."""
   root=tk.Tk()
   root.title("Carbon Footprint Management")
   root.geometry("300x150")

   label = tk.Label(root,text="Flask is running. Visit: http://127.0.0.1:5000")
   label.pack(pady=10)

   button=tk.Button(root,text="Exit", command=root.destroy)
   button.pack(pady=10)

   root.mainloop()


    
if __name__ == "__main__":

   #run tkinter in a seperate thread.
   tkinter_thread = threading.Thread(target=run_tkinter)
   tkinter_thread.daemon=True
   tkinter_thread.start()

   #run flask app in the main thread.
   app.run(debug=True, threaded=True)


