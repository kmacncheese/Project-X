# AI-Driven Cache Replacement Policy Simulator
> CSCE 489 Operating Systems   
> Instructor: Lt Col. Mark Duncan

This project is a proof-of-concept simulator developed to explore the viability of using a machine learning model as an intelligent cache replacement policy. It demonstrates that a learned policy, trained via imitation learning, can significantly outperform traditional static heuristics like LRU (Least Recently Used) and FIFO (First-In, First-Out) on complex, adversarial workloads.

## Setup and Installation

#### 2\. Create and Activate a Virtual Environment

**On Windows (PowerShell):**

```powershell
# Create the environment
python -m venv ai_venv

# Allow scripts to run for this session (may be required)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate the environment
.\ai_venv\Scripts\Activate.ps1
```

**On macOS / Linux:**

```bash
# Create the environment
python3 -m venv ai_venv

# Activate the environment
source ai_venv/bin/activate
```

#### 3\. Install Dependencies

`pip install` the following dependencies into the venv:

```
pandas
scikit-learn
joblib
matplotlib
```

-----

## How to Reproduce the Final Results

#### Step 1: Generate the Synthetic Trace Files

This guide will only walk you through benchmarking with the thrashing trace, since that produced the best results.  There are more traces you can generate on there if you like.

```bash
# Generate the high-locality trace (for baseline testing)
python traces/generate_fake_trace.py

# Generate the definitive thrashing+scan trace (for the final test)
python traces/generate_thrashing_trace.py
```

#### Step 2: Generate the Labeled Training Data

This runs the oracle on both traces to create clean, isolated datasets.

```bash
# Process the locality trace
python data_generator.py --trace_file traces/fake_locality_trace.txt --output_csv locality_data.csv

# Process the thrashing+scan trace
python data_generator.py --trace_file traces/thrashing_scan_trace.txt --output_csv scan_data.csv
```

#### Step 3: Combine Datasets and Train the Model

This creates the final "encyclopedia" for the AI and trains the model.

```bash
# Combine the two clean datasets
python combine_csvs.py

# Train the final, stride-aware AI model
python train_model.py
```

This will create the `cache_model.joblib` file, which is the "brain" of the model.

#### Step 4: Run the Final Benchmarks

This is the final test that compares the policies on the thrashing trace.

```bash
# Test FIFO on the thrashing trace
python simulator.py --policy fifo --trace traces/thrashing_scan_trace.txt

# Test LRU on the thrashing trace
python simulator.py --policy lru --trace traces/thrashing_scan_trace.txt

# Test AI on the thrashing trace
python simulator.py --policy ai --trace traces/thrashing_scan_trace.txt

```

**If you want to test out other traces, just change the `--trace` option to the right `.txt` file.**

-----

## 📁 Project Structure

  - **`simulator.py`**: The main simulation engine. Reads a trace and runs the chosen policy.
  - **`cache.py`**: Contains the `Cache` class that models the cache's state and behavior.
  - **`policies.py`**: Contains the logic for all replacement policies: `LRU_Policy`, `FIFO_Policy`, and the final `AI_Policy`.
  - **`data_generator.py`**: The "oracle" script that implements Bélády's algorithm to generate labeled training data from a trace file.
  - **`combine_csvs.py`**: A memory-efficient script to combine multiple CSV datasets. Used to make training the model easier.
  - **`train_model.py`**: Loads the final `training_data.csv`, trains the Decision Tree model, and saves it to `cache_model.joblib`.
  - **Trace Generators**: `traces/generate_*.py` scripts create the synthetic workloads for testing.
