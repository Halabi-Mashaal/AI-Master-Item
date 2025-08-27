# Master Item AI Agent

This project is designed to create an AI agent with the following capabilities:

- **Master Item NLP for Request Parsing**: Understands your company's technical jargon.
- **Predictive Attribute Suggestion**: Predicts required attributes based on historical item data.
- **Proactive Inventory and Planning Optimization**: Monitors item usage patterns and recommends inventory changes.
- **Confidence Score Thresholding**: Assigns confidence scores to decisions and routes requests based on confidence levels.
- **Active Learning**: Flags ambiguous requests for Data Stewards to improve learning.
- **Reinforcement Learning**: Learns from user behavior to improve search relevance and identify master records.
- **Error Pattern Detection**: Identifies recurring errors, traces sources, and suggests targeted training.
- **Audit Logging**: Maintains an immutable, detailed log for every master record, including metadata for compliance and troubleshooting.
- **Translating Operational Logs into Business KPIs**: Generates a dashboard with metrics like Duplicate Prevention ROI, Data Quality Impact on On-Time Delivery, and New Product Introduction Cycle Time.

## Project Structure
```
Master Item AI Agent/
│
├── data/                     # Data files for training and testing
│   ├── master_item_dataset/  # Folder for master item dataset
│   └── README.md             # Instructions for dataset usage
├── models/                   # Trained models
├── logs/                     # Audit logs
├── notebooks/                # Jupyter notebooks for experimentation
├── src/
│   ├── nlp/                  # NLP-related code
│   ├── predictive/           # Predictive attribute suggestion code
│   ├── inventory/            # Inventory optimization code
│   ├── logging/              # Audit logging code
│   ├── kpi/                  # KPI dashboard code
│   ├── teams_integration/    # Microsoft Teams integration code
│   └── app.py                # Main application entry point
│
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .env                      # Environment variables
```

## Getting Started
1. Add your master dataset to the `data/master_item_dataset/` folder.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the application using `python src/app.py`.

## Requirements
- Python 3.8+
- Libraries: See `requirements.txt` for details.
