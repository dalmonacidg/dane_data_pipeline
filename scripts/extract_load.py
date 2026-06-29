import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
host = os.environ['DB_HOST']
user = os.environ['DB_USER']
password = os.environ['DB_PASS']
port = os.environ['DB_PORT']

# Configure the connection to Postgres on your Linux
# Structure: dialecto+driver://usuario:contraseña@host:puerto/nombre_basededatos

ENGINE = create_engine(f'postgresql://{user}:{password}@{host}:{port}/dane_project')

def load_ocupados():
    path = '/home/dsag2/dane_data_pipeline/data/Ocupados.CSV' # Adjust your username here
    print ("reading DANE dataset (this may take a few saconds)...")

    # Key columns: Period, Month, Department, Labor Income, Activity Branch, Hours worked
    columns_to_keep = ['PERIODO', 'MES', 'DPTO', 'INGLABO', 'RAMA2D_R4', 'P6800']

    # We read with Latin-1 encoding because DANE uses accents and ñ's in the Windows style
    df = pd.read_csv(
        path,
        sep = ';',
        encoding='latin-1',
        usecols = columns_to_keep
    )

    # Basic cleaning of null data in revenue
    df['INGLABO'] = df['INGLABO'].fillna(0)

    print(f"📊 Registros cargados en memoria: {len(df)}")
    print("💾 Inyectando datos en PostgreSQL...")

    # Enviamos los datos a Postgres a una tabla llamada 'raw_ocupados'
    df.to_sql('raw_ocupados', ENGINE, if_exists='replace', index=False, chunksize=10000)
    print("✅ ¡Datos cargados con éxito en la tabla 'raw_ocupados'!")

if __name__ == '__main__':
    load_ocupados()
