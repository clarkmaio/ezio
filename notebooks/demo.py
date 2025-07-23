import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import sys
    from datetime import date, datetime
    import numpy as np
    import polars as pl
    import altair as alt
    import marimo as mo
    sys.path.append(os.getcwd())
    from ezio.base.line import LineChart
    from ezio.base.timeseries import TimeseriesChart
    return LineChart, TimeseriesChart, date, np, pl


@app.cell
def _(date, np, pl):
    N = 1000

    data = pl.DataFrame({
        'time': pl.date_range(start=date(2025, 1, 1), 
                              end=date(2025, 1, 1) + pl.duration(days=N-1), 
                              interval='1d',
                             eager=True),
        'x': np.linspace(0, 100, N).tolist(),
        'var1': (np.random.randn(N) + np.linspace(0, 10, N)).tolist(),
        'var2': (np.random.randn(N)*0.2 + np.sin(np.linspace(0, 10, N))).tolist(),
        'var3':  (np.random.randn(N)*0.3 + np.cos(np.linspace(0, 10, N))).tolist(),
        'class': np.random.choice(['a','b', 'c'], N).tolist()
    }).with_columns(
        lagvar1 = pl.col('var1').diff(1),
        diffvar2var3 = pl.col('var2') - pl.col('var3')
    )
    return (data,)


@app.cell
def _(LineChart, data):
    LineChart(
        data=data,
        x='x',
        y=['var1', 'var2'],
        ytitle='title y axis',
        colors=['green', 'red', 'black'],
        hoverdata=['var1'],
        title='My title',
    ).render(width=500, height=200)
    return


@app.cell
def _(TimeseriesChart, data):
    TimeseriesChart(
        data=data, 
        x='time', 
        y=['var1', 'var2'],
        yview=['var3'],
        title='This is a title',
        colors=['blue', 'black', 'orange'],
        ytitle='y value',
        ytitlebar='bar label'
    ).render(width=700, height=300)
    return


if __name__ == "__main__":
    app.run()
