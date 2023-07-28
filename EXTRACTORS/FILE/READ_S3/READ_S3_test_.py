import pytest
import io
import boto3
import moto
import pandas as pd
from flojoy import DataFrame

# Test dataframe to write as parquet file
@pytest.fixture
def test_dataframe():
    return pd.DataFrame.from_dict({"a": [1, 2, 3], "b": [4, 5, 6]})


# This creates a fake bucket under s3://test_bucket with a file under s3://test_bucket/test_df.parquet
@pytest.fixture
def mock_bucket(test_dataframe):
    moto_fake = moto.mock_s3()
    try:
        moto_fake.start()
        conn = boto3.resource('s3')
        conn.create_bucket(Bucket="test_bucket")
        test_bucket = conn.Bucket("test_bucket")
        # Write a parquet file to the bucket
        with io.BytesIO() as f:
            test_dataframe.to_parquet(f)
            test_bucket.put_object(Key="test_df.parquet", Body=f.getvalue())
        yield conn
    finally:
        moto_fake.stop()


def test_READ_S3(
    mock_flojoy_decorator,
    mock_flojoy_cache_directory,
    mock_bucket,
    test_dataframe
    ):

    import READ_S3

    output = READ_S3.READ_S3("test", "test_bucket", "test_df.parquet")
    assert output.m.equals(test_dataframe)