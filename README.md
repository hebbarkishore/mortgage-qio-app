# Quantum-Inspired Mortgage Pool Optimization App

A Streamlit-based demo for secondary-market mortgage loan pooling using Quantum-Inspired Optimization (QIO)

## Overview
This project is an interactive demonstration of a Quantum-Inspired Optimization (QIO) framework applied to mortgage loan pooling, a critical step in secondary-market execution.

Lenders must form loan pools that simultaneously satisfy:
-   Credit overlays
-   Geographic concentration limits
-   Loan-to-Value (LTV) rules
-   Weighted-Average Coupon (WAC) constraints
-   Investor-specific eligibility requirements

Traditional heuristic and spreadsheet-based approaches struggle when these constraints overlap.
This app shows how a QUBO-based quantum-inspired model can evaluate large combinations of loans and recommend optimized pools that maximize execution value while respecting all rules.


## How the System Works

1. Data Ingestion
    -   Upload Excel loan tape
    -   Validate required fields
    -   Standardize structure

2. Feature Engineering
    -   Compute rate spreads
    -   Create FICO and LTV buckets
    -   Assign geographic markers
    -   Add high-risk flags and eligibility indicators

3. Baseline Heuristic

    A greedy algorithm sorts loans by proxy value (e.g., coupon) and selects top loans until pool size is met, ignoring constraints.

4. Quantum-Inspired Optimization

    The QIO solver:
    -   Builds a QUBO matrix encoding financial objectives + constraints
    -   Minimizes energy using simulated annealing–like search
    -   Identifies a feasible optimized pool

5. Scoring & Presentation

    The app presents:
    -   Selected loans from both methods
    -   Execution-value comparison
    -   Risk-metric comparison
    -   Constraint-violation analysis
    -   Composite score evaluation

    All outputs appear cleanly in Streamlit tables and graphs.

## Running the App with Docker (Recommended)
docker build -t qio-app . && docker run -p 8501:8501 qio-app

## Local Setup (Without Docker)
-   python3 -m venv venv
-   source venv/bin/activate   
-   for Windows: venv\Scripts\activate
-   pip install -r requirements.txt
-   streamlit run app.py

## Intended Use

This app is built for:
-   Research demos
-   Paper reproducibility
-   Academic presentations
-   FinTech workshops
-   Internal capital-markets engineering teams
-   Proof-of-concept evaluation

It is not intended for direct production-grade pooling or official investor submissions.

