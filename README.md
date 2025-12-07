##  Introduction to Programming Final Project

## Chosen Dataset
**Bird Population & Environmental Trends in Asia**

----------

## **Research Questions**

The project investigates the following research questions, each led by a team member:

-   **Md Hafijur Rahman**:  
    _How do environmental conditions (temperature, precipitation, and human activity) shape habitat suitability patterns for different bird species across Asia between 1980 and 2010?_
    
-   **Mahfuzur Rahman Masum**:  
    _How does bird species diversity vary across countries, and which country stands out as the richest habitat?_
    
-   **Hafsa Akter**:  
    _Can bird movement patterns (Shift_km) be used as early-warning indicators of climate and land-use change across Asian ecosystems from 1980–2010?_
    
-   **Spyridon Mitsis**:  
    _How have bird populations of climate-sensitive species changed across Asia, and how are these changes associated with regional trends in temperature, precipitation, and urbanization?_
    

----------

## **Repository Structure**

```
project/
│
├── app.py                       # Main Dash application
├── analysis/
│   └── rs1.py                   # Data preparation and analysis functions
│
├── data/
│   └── cleaned_bird_data.csv    # Preprocessed dataset
│
├── README.md                    # This document
└── requirements.txt             # Project dependencies

```

----------

## **Installation & Setup**

### **1. Create virtual environment (recommended)**

```bash
python3 -m venv venv
source venv/bin/activate      # MacOS/Linux
venv\Scripts\activate         # Windows

```

### **2. Install dependencies**

```bash
pip install -r requirements.txt

```

----------

## **Running the Application**

From the project directory, run:

```bash
python main.py

```

Then visit the application in your browser at:

```
http://127.0.0.1:8050/

```

----------

## **Credits**

**Project Group:**

-   Md Hafijur Rahman
    
-   Mahfuzur Rahman Masum 
    
-   Hafsa Akter

-   Spyridon Mitsis 
    

**Course:** DSK801 Programming for Data Science / DSK811 Introduction to Programming  
**Instructor:** Prof. Alexandra Diehl  
**Teaching Assistants:** Rheannon Lefever | Mona Petersen Skriver

----------

