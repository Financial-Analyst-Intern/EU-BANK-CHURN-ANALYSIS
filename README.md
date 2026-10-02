# EU Bank Customer Churn Analytics

An interactive Streamlit dashboard for exploring customer segments and churn patterns in a European banking dataset.

## Features

- Filter by geography, gender, age, account balance, and activity status
- View churn metrics and balance lost to churn
- Compare churn by product count, activity, credit band, geography, age, and tenure
- Explore churn among high-value customers

## Requirements

Python 3.10 or newer is recommended.

## Install and run

From this directory, install the packages listed in `requirements.txt`, then start the dashboard:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app expects `european_bank_processed.csv` in this directory; that dataset is included in this repository.

## Dataset

The bundled CSV contains customer/account attributes and a binary `Exited` churn label, along with derived grouping columns used by the dashboard. Review the dataset's source and usage rights before redistributing it publicly.
