from fpdf import FPDF
import os
import pandas as pd 

class PDF(FPDF):
    def header(self):
        self.set_font('Arial','B',12)
        self.cell(0,10, 'Carbon Footprint Report',border=False, ln=True ,align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0,10,f'Page {self.page_no()}',align='C')

def generate_summary(csv_file="carbon_data.csv"):
   
   """ generate summart statistics across all reports"""
   if not os.path.exists(csv_file):
      return " no data available for summary this file."
   

   try:
      df = pd.read_csv(csv_file)

      #convert necessary columns to numeric.
      numeric_columns=["Electricity (kg CO2)","Waste (kg CO2)","Travel (kg CO2)","Total (kg CO2)"]
      for col in numeric_columns:
           df[col]=pd.to_numeric(df[col], errors='coerce')
      
      #calculate summaries all data


      total_average= df["Total (kg CO2)"].mean()
      max_total = df["Total (kg CO2)"].max()
      min_total=df["Total (kg CO2)"].min()

      return f"""
      Summary Statistic:
      - Average Total CO2: {total_average:.2f} kg 
      - Max Total CO2: {max_total:.2f} kg 
      - Min Total CO2: {min_total:.2f} kg 

      """
   except Exception as e:
      return f"Error generating summary: {e}"




def generate_pdf(data, graph_file="static/graph.png", csv_file="carbon_data.csv", output_folder="reports"):
    """Generate a PDF report for the given data and includes the graph."""

    #output folder check

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #PDF create filename

    filename= f"{output_folder}/{data['Name']}_{data['Year']}_report.pdf"

    pdf= PDF()
    pdf.add_page()
    pdf.set_font ('Arial', '', 12)

    #add user input data in to table.

    pdf.set_font('Arial','B',12)
    pdf.cell(0,10,"Input Data:", ln=True)
    pdf.set_font('Arial','',10)
    pdf.cell(50,10,"Field",border=1,align='C')
    pdf.cell(70,10,"Value",border=1,align='C')
    pdf.ln()

    for key, value in data.items():
       pdf.cell(50,10,key,border=1,align='C')
       pdf.cell(70,10,str(value),border=1,align='C')
       pdf.ln()
    
    pdf.ln(10)


    #add group and sort table
    pdf.set_font('Arial','B',12)
    pdf.cell(0,10, "Grouped and Sorted Data:", ln=True)
    pdf.set_font('Arial','',10)

    if os.path.exists(csv_file):
       try:
        df = pd.read_csv(csv_file)

        numeric_columns=["Year","Electricity (kg CO2)","Waste (kg CO2)","Travel (kg CO2)","Total (kg CO2)"]
        for col in numeric_columns:
           df[col]=pd.to_numeric(df[col], errors='coerce')

        #drop rows with NaN values
        df=df.dropna()

        #sort by Name alphabetically and Year.
        df=df.sort_values(by=["Name","Year"], ascending=[True,True])


        #add table header
        def add_table_header():
          
          pdf.set_font('Arial','B',10)
          pdf.cell(20,10, "Name", border=1,align='C')
          pdf.cell(15,10, "Year", border=1,align='C')
          pdf.cell(35,10, "Electricity (kg CO2)", border=1,align='C')
          pdf.cell(35,10, "Waste (kg CO2)", border=1,align='C')
          pdf.cell(35,10, "Travel (kg CO2)", border=1,align='C')
          pdf.cell(35,10, "Total (kg CO2)", border=1,align='C')
          pdf.ln()

        add_table_header()


        #add table rows
        pdf.set_font('Arial','',10)
        for _, row in df.iterrows():
           pdf.cell(20,10, row["Name"], border=1,align='C')
           pdf.cell(15,10, str(int(row['Year'])), border=1,align='C')
           pdf.cell(35,10, f"{row['Electricity (kg CO2)']:.2f}", border=1,align='C')
           pdf.cell(35,10, f"{row['Waste (kg CO2)']:.2f}", border=1,align='C')
           pdf.cell(35,10, f"{row['Travel (kg CO2)']:.2f}", border=1,align='C')
           pdf.cell(35,10, f"{row['Total (kg CO2)']:.2f}", border=1,align='C')
           pdf.ln()

           #Check if tha page is full and add a new page if necessary.
           if pdf.get_y() > 260:
              pdf.add_page()
              add_table_header()
              


       except Exception as e:
          pdf.cell(0,10,f"Error reading or processing data : {e}", ln=True) 
    else:
       pdf.cell(0,10, "Graph file not found. Could not include graph", ln=True)  

    pdf.ln(10)

    # add summary 
    pdf.set_font('Arial','B',12)
    pdf.cell(0,10, "Summary Statistics:", ln=True)
    pdf.set_font('Arial','',10)
    summary=generate_summary(csv_file)
    pdf.multi_cell(0,10,summary)

    pdf.ln(10)
    
           
    
    #add graph if it exists.

    pdf.set_font('Arial','B',12)
    pdf.cell(0,10, "Carbon Footprint Graph:", ln=True)

    if os.path.exists(graph_file):
      if pdf.get_y() > 200:
              pdf.add_page()
      pdf.image(graph_file, x=10 , y=pdf.get_y(), w=190)
    else:
      pdf.cell(0,10, "Graph file not found. Could not include graph", ln=True)


    pdf.output(filename)
    print(f"PDF report generated: {filename}")
