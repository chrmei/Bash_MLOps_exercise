# Graphics Card Sales Prediction Pipeline

Automated MLOps pipeline for collecting graphics card sales data, preprocessing it, and training an XGBoost prediction model.

## Overview

This pipeline automates:
- **Data Collection**: Queries API every minute for sales data (rtx3060, rtx3070, rtx3080, rtx3090, rx6700)
- **Preprocessing**: Cleans and transforms raw data into features
- **Model Training**: Trains XGBoost model for sales prediction

## Setup

### Install Dependencies

    python3 -m venv .venv
    source .venv/bin/activate
    pip install uv
    uv sync

### Extract API into root directory

    tar -xvf resources/api.tar

### Start API Server

    chmod +x api
    ./api &

### Setup Cron Job

    crontab scripts/cron.txt
    crontab -l    # list all cron jobs to verify installation
    tail -f logs/cron.log # monitor cron jobs


## Usage

### Run Pipeline Manually

    make bash

### Run Tests

    make tests

Test logs are saved in `logs/tests_logs/`.


### Optional Dependencies for Development

    uv pip install -r pyproject.toml --extra dev


note: tests_logs in requirements vs automatically created "tests_logs" directory through pytest files...
