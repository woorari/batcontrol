# Scripts Directory

This directory contains standalone test scripts and utilities for the batcontrol project.

## Purpose

The `scripts` folder is separate from the `tests` folder to avoid interference with the automated unit test suite (pytest). These scripts are meant for:

- Manual testing and debugging
- Integration testing with real APIs
- Development utilities
- Standalone demonstrations

## Available Scripts

### test_evcc.py

Standalone test script for the EVCC dynamic tariff module.

**Usage:**
```bash
# From project root
python scripts/test_evcc.py <url>

# Examples
python scripts/test_evcc.py http://evcc.local/api/tariff/grid
```

**Features:**
- Tests the EVCC API integration
- Shows both raw API data and processed prices
- Provides detailed error information for debugging
- Displays hourly prices with proper formatting

**Requirements:**
- Run from the project root directory
- Virtual environment should be activated or use full Python path
- pytz package must be installed

### create_load_profile_from_test_data.py

Script to convert test data CSV files to load_profile.csv format.

**Usage:**
```bash
# From project root, using default paths (creates file with timestamp)
python scripts/create_load_profile_from_test_data.py

# With custom input file (output file will have timestamp)
python scripts/create_load_profile_from_test_data.py <input_file>

# With custom input and output paths
python scripts/create_load_profile_from_test_data.py <input_file> <output_file>

# Examples
python scripts/create_load_profile_from_test_data.py
python scripts/create_load_profile_from_test_data.py "docs/test data/Rieck_01012025-31122025.csv"
python scripts/create_load_profile_from_test_data.py "docs/test data/Rieck_01012025-31122025.csv" config/load_profile_custom.csv
```

**Output File Naming:**
- If no output file is specified, the script automatically creates a file with timestamp: `load_profile_dd_mm_yyyy.csv`
- Example: `load_profile_05_01_2026.csv` (created on January 5, 2026)
- This ensures each run creates a new file without overwriting previous ones

**Features:**
- Converts test data with 5-minute intervals to hourly load profile
- Aggregates energy consumption by month, weekday, and hour
- Calculates average energy consumption for each combination
- Handles German date format (dd.MM.yyyy HH:mm)

**Input Format:**
- CSV file with columns: "Datum und Uhrzeit" (dd.MM.yyyy HH:mm), "Verbrauch" (Wh)
- Data should be in 5-minute intervals

**Output Format:**
- CSV file with columns: month (1-12), weekday (0-6, 0=Monday), hour (0-23), energy (Wh)
- Contains 2016 entries (12 months × 7 weekdays × 24 hours)

**Requirements:**
- Run from the project root directory
- pandas package must be installed
- Virtual environment should be activated or use full Python path

## Running Scripts

All scripts should be run from the project root directory:

```bash
# With virtual environment activated
python scripts/test_evcc.py <arguments>

# Or with full path to virtual environment Python
/path/to/venv/bin/python scripts/test_evcc.py <arguments>
```

## Adding New Scripts

When adding new standalone scripts:

1. Place them in this `scripts` directory
2. Include a shebang line: `#!/usr/bin/env python3`
3. Add proper documentation in the docstring
4. Update this README with usage information
5. Use relative imports and path manipulation to import project modules
