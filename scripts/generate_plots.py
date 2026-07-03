import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
host = os.environ['DB_HOST']
user = os.environ['DB_USER']
password = os.environ['DB_PASS']
port = os.environ['DB_PORT']

# 1. Configuring the connection to the database
ENGINE = create_engine(f'postgresql://{user}:{password}@{host}:{port}/dane_project')


def load_data():
    print("🔌 Connecting to PostgreSQL and extracting data...")
    # We only include the columns necessary to optimize memory.
    query = """
            SELECT dpto, mes, inglabo, p6800
            FROM raw_ocupados
            WHERE inglabo > 0 \
              AND p6800 > 0 \
              AND p6800 < 99; \
            """
    return pd.read_sql(query, ENGINE)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Find the absolute path of this script
    root_dir = os.path.dirname(script_dir) # Go up a level to reach the true root of the project
    reports_dir = os.path.join(root_dir, 'reports') # Define the correct path to the 'reports' folder in the root directory

    # Ensure that the reports folder exists
    os.makedirs('reports', exist_ok=True)

    # Load data
    df = load_data()
    print(f"📊 Data loaded successfully. Records to be processed: {len(df)}")

    # Configure Seaborn's overall aesthetic style
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams['figure.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 11

    # =========================================================================
    # GRAPH 1: Distribution of Labor Income
    # =========================================================================
    print("🎨 Generating Chart 1: Income Distribution...")
    plt.figure(figsize=(10, 5))
    # We use a logarithmic scale on X due to the high wage disparity
    sns.histplot(data=df, x='inglabo', kde=True, color='#2b5c8f', bins=50, log_scale=True)
    plt.title('Global Distribution of Labor Income (Logarithmic Scale))', pad=15)
    plt.xlabel('Labor Income ($ - Log Scale)')
    plt.ylabel('Frequency of Occupancy')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, '1_income_distribution.png'), dpi=300)
    plt.close()

    # =========================================================================
    # GRAPH 2: Average Salary by Department
    # =========================================================================
    print("🎨 Generating Chart 2: Comparison by Department...")
    # We grouped the average by department in the DataFrame to facilitate the graph
    dpto_summary = df.groupby('dpto')['inglabo'].mean().reset_index().sort_values(by='inglabo', ascending=False)
    plt.figure(figsize=(10, 6))

    sns.barplot(data=dpto_summary, x='inglabo', y='dpto', hue='dpto', palette='viridis', legend=False)

#    formatter = ticker.StrMethodFormatter('${x:,.0f}')
#    plt.gca().xaxis.set_major_formatter(formatter)

    plt.title('Average Monthly Salary by Department Code (DANE)', pad=15)
    plt.xlabel('Average Salary ($)')
    plt.ylabel('Department Code (Divipola)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, '2_average_dept_salary.png'), dpi=300)
    plt.close()

    # =========================================================================
    # GRAPH 3: Relationship between Hours Worked and Labor Income
    # =========================================================================
    print("🎨 Generating Graph 3: Correlation Hours vs. Income...")
    plt.figure(figsize=(10, 6))
    # We took a random sample of 5,000 records so that the graph would not become saturated.
    sample_df = df.sample(n=min(5000, len(df)), random_state=42)

    sns.scatterplot(data=sample_df, x='p6800', y='inglabo', alpha=0.4, color='#e67e22', edgecolor=None)
    # We added a linear trend line
    sns.regplot(data=sample_df, x='p6800', y='inglabo', scatter=False, color='#d35400',
                line_kws={"linewidth": 2, "linestyle": "--"})

    plt.title('Correlation Analysis: Hours Worked per Week vs. Income', pad=15)
    plt.xlabel('Weekly Hours Worked (p6800)')
    plt.ylabel('Employment Income ($)')
    plt.yscale('log')  # Logarithmic scale for handling high-income outliers
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, '3_correlation_hours_income.png'), dpi=300)
    plt.close()

    print("🚀 The 3 images have been saved in the folder 'reports/'.")


if __name__ == '__main__':
    main()