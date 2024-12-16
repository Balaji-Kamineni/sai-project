# Battery Aging Analysis with Plotly

This project uses the NASA Battery Dataset to analyze and visualize the changes in battery parameters (Battery Impedance, Electrolyte Resistance, and Charge Transfer Resistance) as the battery cell ages through charge/discharge cycles. The analysis is visualized using interactive plots generated with Plotly.

## Features

- Interactive plots showing how battery parameters change over time.
- Parameters analyzed :
  - **Battery Impedance**
  - **Re (Electrolyte Resistance)**
  - **Rct (Charge Transfer Resistance)**

## Dataset

The dataset used in this project is the [NASA Battery Dataset](https://www.kaggle.com/datasets/patrickfleith/nasa-battery-dataset). It contains information about battery aging, with columns like `Battery_impedance`, `Re` and`Rct`.

## Requirements

This project requires Python 3.8 or higher and the following Python packages:

- pandas
- numpy
- plotly
- kagglehub

## Setup Instructions
```bash
# Clone the repository
git clone https://github.com/AzariushHussain/ThinkClock-Innovation-Labs---internship.git

# Navigate inside the folder
cd folder_name

# Create a virtual environment
py -m venv _name_of_virtual_environment_ (Windows)
python -m venv _name_of_virtual_environment_ (Unix/MacOS)

# Activate the virtual environment
_name_of_virtual_environment_\Scripts\activate (Windows)
source _name_of_virtual_environment_/bin/activate (Unix/MacOS)

# Install requirements
pip install -r requirements.txt

# For creating another analysis HTML file.
python main.py

# ___ IMPORTANT___
A generated HTML file  is already provided for refrence
