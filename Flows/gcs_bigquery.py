import pandas as pd
import numpy as np
from typing import List
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(year: int, month: int) -> Path:
    """download citibikes data from gcs"""
    gcs_path = f"Src/{year}{month:02}-citibike-tripdata.zip.parquet"
    gcs_block = GcsBucket.load("citibikes-block")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../")
    return Path(f"../{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """clean the data"""
    df = pd.read_parquet(path)
    df['birth year'] = df['birth year'].replace('\\N', np.nan).fillna(2023).astype(str)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

@task
def write_bq(df: pd.DataFrame) -> None:
    """wrtie DataFrame to big query"""

    # load gcp cred block
    gcp_credentials_block = GcpCredentials.load("citibikes-gcp-creds")

    df.to_gbq(
        destination_table='dbt_training.Citibikes',
        project_id='red-atlas-389804',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists='append'
    )

@flow()
def etl_gcs_bq(year: int, month: int):
    """main ETL to load data to Big query"""

    path = extract_from_gcs(year, month)
    df = transform(path)
    write_bq(df)

@flow()
def big_query(year: int = 2013, months: List[int] = [1,2]):
    for month in months:
        etl_gcs_bq(year, month)


