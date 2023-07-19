from flojoy import flojoy, run_in_venv, DataFrame, DataContainer
from typing import TypedDict


class ProphetPredictOutput(TypedDict):
    dataframe: DataFrame
    prophet_data: DataContainer


@flojoy(deps={"prophet": "1.1.4", "holidays": "0.26", "pystan": "2.19.1.1"})
@run_in_venv(
    pip_dependencies=[
        "prophet==1.1.4",
    ]
)
def PROPHET_PREDICT(
    default: DataFrame, run_forecast: bool = True, periods: int = 365
) -> ProphetPredictOutput:
    """The PROPHET_PREDICT node rains a Prophet model on the incoming dataframe.

    The DataContainer input type must be `dataframe`, and that dataframe must have its
    first column (or index) be of datetime type.

    This node always returns a DataContainer of type 'dataframe'. It will also
    always return an `extra` field with a key `prophet` whose value is the JSONified
    Prophet model, which can be loaded as follows:
        ```python
        from prophet.serialize import model_from_json

        model = model_from_json(dc_inputs.extra["prophet"])
        ```

    Parameters
    ----------
    run_forecast : bool
        If the True (default case), the returning DataContainer
        will have its dataframe (`m` parameter of the DataContainer) be the forecasted
        dataframe. It will also have an `extra` field with the key "original" which is
        the original dataframe passed in.

        If false, the returning dataframe will be the original data.

        This node will also always have an `extra` field "run_forecast" which matches
        that of the param passed in. This is for future nodes to know if a forecast
        has already been run

        Default True
    periods : int
        The number of periods to predict out. Only used if run_forecast is True.
        Default 365

    Returns
    -------
    DataFrame with param `df` which indicates either the original
        df passed in, or the forecasted df (depending on if `run_forecast` is True)

    DataContainer with param 'extra' containing keys "run_forecast" which correspond to the
        input param, and potentially "original" in the event that `run_forecast` is True
    """

    import os
    import sys
    import pandas as pd
    import numpy as np

    import prophet
    from prophet.serialize import model_to_json

    def _make_dummy_dataframe_for_prophet():
        """Generate random time series data to test if prophet works"""
        start_date = pd.Timestamp("2023-01-01")
        end_date = pd.Timestamp("2023-07-20")
        num_days = (end_date - start_date).days + 1
        timestamps = pd.date_range(start=start_date, end=end_date, freq="D")
        data = np.random.randn(num_days)  # Random data points
        df = pd.DataFrame({"ds": timestamps, "ys": data})
        df.rename(
            columns={df.columns[0]: "ds", df.columns[1]: "y"}, inplace=True
        )  # PROPHET model expects first column to be `ds` and second to be `y`
        return df


    def _apply_macos_prophet_hotfix():
        """This is a hotfix for MacOS. See https://github.com/facebook/prophet/issues/2250#issuecomment-1559516328 for more detail"""

        if not sys.platform == "darwin":
            return

        # Test if prophet works (i.e. if the hotfix had already been applied)
        try:
            _dummy_df = _make_dummy_dataframe_for_prophet()
            prophet.Prophet().fit(_dummy_df)
        except RuntimeError as e:
            print(f"Could not run prophet, applying hotfix...")
        else:
            return
        
        prophet_dir = prophet.__path__[0] # type: ignore
        # Get stan dir
        stan_dir = os.path.join(prophet_dir, "stan_model")
        # Find cmdstan-xxxxx dir
        cmdstan_basename = [x for x in os.listdir(stan_dir) if x.startswith("cmdstan")]
        assert len(cmdstan_basename) == 1, "Could not find cmdstan dir"
        cmdstan_basename = cmdstan_basename[0]
        # Run (from stan_dir) : install_name_tool -add_rpath @executable_path/<CMDSTAN_BASENAME>/stan/lib/stan_math/lib/tbb prophet_model.bin
        cmd = f"install_name_tool -add_rpath @executable_path/{cmdstan_basename}/stan/lib/stan_math/lib/tbb prophet_model.bin"
        cwd = os.getcwd()
        os.chdir(stan_dir)
        return_code = os.system(cmd)
        os.chdir(cwd)
        if return_code != 0:
            raise RuntimeError("Could not apply hotfix")

    _apply_macos_prophet_hotfix()

    df = default.m
    first_col = df.iloc[:, 0]
    if not pd.api.types.is_datetime64_any_dtype(first_col):
        raise ValueError(
            "First column must be of datetime type data for PROPHET_PREDICT!"
        )
    df.rename(
        columns={df.columns[0]: "ds", df.columns[1]: "y"}, inplace=True
    )  # PROPHET model expects first column to be `ds` and second to be `y`
    model = prophet.Prophet()
    model.fit(df)
    extra = {"prophet": model_to_json(model), "run_forecast": run_forecast}
    # If run_forecast, the return df is the forecast, otherwise the original
    return_df = df.copy()
    if run_forecast:
        future = model.make_future_dataframe(periods)
        forecast = model.predict(future)
        extra["original"] = df
        return_df = forecast
    return ProphetPredictOutput(
        dataframe=DataFrame(df=return_df), prophet_data=DataContainer(extra=extra)
    )
