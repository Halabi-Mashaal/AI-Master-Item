import pandas as pd

# Create a simple test Excel file
data = {
    'Item_Code': ['CEM001', 'CEM002', 'CEM003'],
    'Cement_Grade': ['OPC 53', 'OPC 43', 'PPC'],
    'Quantity_Bags': [5000, 3500, 2800],
    'Strength_MPa': [53, 43, 33],
    'Unit_Price': [15.5, 14.2, 13.8]
}

df = pd.DataFrame(data)
df.to_excel('New Microsoft Excel Worksheet.xlsx', index=False)
print("✅ Created test Excel file: New Microsoft Excel Worksheet.xlsx")
