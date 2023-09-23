import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web to pandas"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
    """fix dtype issues"""
    df['starttime'] = pd.to_datetime(df['starttime'])
    df['stoptime'] = pd.to_datetime(df['stoptime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> pd.DataFrame:
    """write DF as paquet file"""
    path = Path(f"Src/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@task
def write_gcs(path: Path) -> None:
    """upload paquet to gcs"""
    gcs_block = GcsBucket.load('citibikes-demo')
    gcs_block.upload_from_path(
        from_path=f"{path}",
        to_path=path
    )
    return

@flow()
def etl_web_to_gcs() -> None:
    """The main function"""
    year = 2013
    month = 8
    dataset_file = f"{year}0{month}-citibike-tripdata.zip"
    dataset_url = f"https://s3.amazonaws.com/tripdata/{dataset_file}"

    # save as a pandas data frame
    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file)
    write_gcs(path)

