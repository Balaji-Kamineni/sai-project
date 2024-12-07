import kagglehub
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go

print("Processing NASA battery dataset...\nPlease wait...")

# Download dataset
file_path = kagglehub.dataset_download("patrickfleith/nasa-battery-dataset")
# Paths
base_path = f"{file_path}\\cleaned_dataset"
data_path = os.path.join(base_path, "data")
metadata_file = os.path.join(base_path, "metadata.csv")

# Load metadata
metadata = pd.read_csv(metadata_file)

# Initialize lists for combined data
battery_ids = []
relative_ages = []
charge_discharge_cycles = []
battery_impedance = []
electrolyte_resistance = []
charge_transfer_resistance = []

# Process each file in metadata
for battery_id in metadata["battery_id"].unique():
    # Filter metadata for the current battery ID
    battery_metadata = metadata[metadata["battery_id"] == battery_id]
    
    # Process each file for the current battery
    for relative_age, (_, row) in enumerate(battery_metadata.iterrows()):
        filename = row['filename']
        file_path = os.path.join(data_path, filename)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        # Load the data from the file (assume CSV format)
        test_data = pd.read_csv(file_path)
        
        # Calculate impedance magnitude if real and imaginary parts are present
        if 'Battery_impedance' in test_data.columns:
            real_imag_parts = test_data['Battery_impedance'].str.extract(r"\((.+)\+(.+)j\)")
            real_part = pd.to_numeric(real_imag_parts[0], errors='coerce')
            imag_part = pd.to_numeric(real_imag_parts[1], errors='coerce')
            magnitude = np.sqrt(real_part**2 + imag_part**2)
            avg_impedance = magnitude.mean()
        else:
            avg_impedance = None
        
        # Append extracted and calculated values
        battery_ids.append(row['battery_id'])
        relative_ages.append(relative_age)  # Start aging from 0 for each battery
        charge_discharge_cycles.append(row['test_id'])
        battery_impedance.append(avg_impedance)
        electrolyte_resistance.append(row['Re'])
        charge_transfer_resistance.append(row['Rct'])

# Combine data into a DataFrame
combined_data = pd.DataFrame({
    'Age': relative_ages,
    'Battery ID': battery_ids,
    'Charge/Discharge Cycle': charge_discharge_cycles,
    'Battery Impedance': battery_impedance,
    'Re (Electrolyte Resistance)': electrolyte_resistance,
    'Rct (Charge Transfer Resistance)': charge_transfer_resistance,
})

# Create the interactive plot with dropdowns
fig = go.Figure()

# Initially, do not show any data
parameters = ["Battery Impedance", "Re (Electrolyte Resistance)", "Rct (Charge Transfer Resistance)"]

# Add traces for each parameter, set visibility to False initially
for parameter in parameters:
    fig.add_trace(go.Scatter(
        x=[],  # Empty x-axis
        y=[],  # Empty y-axis
        mode='markers+lines',
        name=parameter,
        visible=False  # All parameters hidden initially
    ))

# Update layout with dropdown menus
fig.update_layout(
    title="Battery Aging Analysis",
    xaxis_title="Age (Charge/Discharge Cycle)",
    yaxis_title="Parameter Value",
    updatemenus=[
        # Dropdown for selecting the parameter to display
        dict(
            buttons=[dict(label="Select Topic", method="update", args=[{"visible": [False] * len(parameters)}, {"yaxis": {"title": "Select Topic"}}])]
            + [
                dict(label=param,
                     method="update",
                     args=[{"visible": [p == param for p in parameters] + [True] * len(parameters)},
                           {"yaxis": {"title": param}}])
                for param in parameters
            ],
            direction="down",
            showactive=True,
            x=0.15,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
        # Dropdown for selecting the battery ID
        dict(
            buttons=[dict(label="Select Battery ID", method="update", args=[{"x": [], "y": []}, {"title": "Select Battery ID"}])]
            + [
                dict(label=f"Battery {battery_id}",
                     method="update",
                     args=[
                         {
                             "x": [combined_data.loc[combined_data["Battery ID"] == battery_id, "Age"]],
                             "y": [
                                 combined_data.loc[combined_data["Battery ID"] == battery_id, param]
                                 for param in parameters
                             ],
                         },
                         {"title": f"Battery ID {battery_id}"}
                     ])
                for battery_id in combined_data["Battery ID"].unique()
            ],
            direction="down",
            showactive=True,
            x=0.35,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )
    ]
)

# Show the plot
fig.write_html("battery_aging_analysis.html")
print("Plot saved. Open 'battery_aging_analysis.html' in a browser.")
