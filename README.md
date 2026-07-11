# Colombian Labor Market Data Pipeline
### DANE – GEIH (Módulo Ocupados, Marzo 2026)

An end-to-end Data Engineering pipeline that ingests public microdata from Colombia's national statistics agency (DANE), loads it into a local PostgreSQL instance, runs advanced SQL analytical queries, and produces automated labor market visualizations.

---

## What This Project Does

1. **Extracts** raw CSV microdata from the DANE GEIH survey (Módulo Ocupados)
2. **Loads** it into a local PostgreSQL database via a Python ETL script
3. **Transforms** the data using advanced SQL (window functions, aggregations)
4. **Visualizes** the results as high-resolution PNG plots

---

## Tech Stack

| Layer | Technology |
|---|---|
| OS Environment | Windows 11 + WSL2 (Ubuntu 22.04 LTS) |
| Language | Python 3 (virtualenv) |
| Database | PostgreSQL 14 |
| ORM / Connector | SQLAlchemy + Psycopg2 |
| Data Processing | Pandas |
| Visualization | Matplotlib, Seaborn |
| IDE | PyCharm Professional |

---

## Architecture

```
DANE Website (CSV download)
        │
        ▼
data/Ocupados.CSV
        │
        ▼
scripts/extract_load.py  ──►  PostgreSQL (DB: dane_pipeline)
                                      │
                                      ▼
                          sql/window_functions_analysis.sql
                                      │
                                      ▼
                          scripts/generate_plots.py
                                      │
                                      ▼
                             reports/*.png
```

---

## Project Structure

```text
dane_data_pipeline/
├── data/                               # Raw DANE CSV microdata
│   └── Ocupados.CSV
├── sql/                                # Analytical SQL transformations
│   └── window_functions_analysis.sql  # Window functions (LAG, LEAD, PARTITION BY)
├── scripts/                            # ETL and visualization scripts
│   ├── extract_load.py                 # Ingestion pipeline (CSV → PostgreSQL)
│   └── generate_plots.py              # Query results → PNG plots
├── reports/                            # Auto-generated high-resolution plots
└── README.md
```

---

## Data Source

Data comes from the **Gran Encuesta Integrada de Hogares (GEIH)** published monthly by DANE.

- **Source:** [microdatos.dane.gov.co](https://microdatos.dane.gov.co/index.php/catalog/ENChogares)
- **Survey:** GEIH – Módulo de Ocupados
- **Period used:** Marzo 2026
- **File:** `Ocupados.CSV`

> **To download the data:**
> 1. Go to the DANE microdata catalog above
> 2. Search for "Gran Encuesta Integrada de Hogares"
> 3. Select the March 2026 edition
> 4. Download the **Ocupados** module and place the CSV in the `data/` folder

---

## Setup & Installation

### Prerequisites

- WSL2 with Ubuntu 26.04
- Python 3.10+
- PostgreSQL 18 installed inside WSL2

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/dane_data_pipeline.git
cd dane_data_pipeline
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Start the PostgreSQL service and create the database:

```bash
sudo service postgresql start
psql -U postgres -c "CREATE DATABASE dane_pipeline;"
```

> The pipeline connects to PostgreSQL on port `5433`. If your instance runs on the default port `5432`, update the connection string in `extract_load.py`.

### 5. Configure environment variables

Create a `.env` file at the project root:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5433
DB_NAME=dane_pipeline
```

---

## Usage

### Step 1 – Load the data

```bash
python scripts/extract_load.py
```

This reads `data/Ocupados.CSV` and loads it into the `ocupados` table in PostgreSQL.

### Step 2 – Run SQL analysis

```bash
psql -U postgres -d dane_pipeline -f sql/window_functions_analysis.sql
```

Applies window function transformations (e.g., ranking occupations by income, computing period-over-period deltas with `LAG`/`LEAD`).

### Step 3 – Generate visualizations

```bash
python scripts/generate_plots.py
```

Queries the transformed data and outputs PNG plots to the `reports/` folder.

---

## Sample Output

> *(Add a screenshot of one of your plots here)*
> `![Income distribution by occupation](reports/sample_plot.png)`

---

## Key Analytical Questions

- What is the income distribution across occupation categories?
- How does occupational composition shift across demographic segments?
- Which occupations show the highest variance in reported hours worked?

---

## License

This project uses public microdata from DANE under Colombia's open data policy.
Project code is licensed under MIT.E.md             # Project documentation