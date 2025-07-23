
import polars as pl
import altair as alt
from typing import Optional, List

def DistributionChart(data: pl.DataFrame, x: str, color: str = 'blue', hue: str = None, type: str = 'histogram', orientation: str = 'horizontal'):
    '''
    Create a distribution chart based on the specified type.
    '''

    if type == 'histogram':
        return HistogramChart(data=data, x=x, hue=hue, color=color)
    else:
        raise NotImplementedError(f"Distribution type '{type}' is not implemented.")    
    




def HistogramChart(data, x: str, hue: str = None, color: str = 'blue', orientation: str = 'horizontal'):
    '''
    Create a histogram chart for the specified variable.
    '''

    if orientation not in ['horizontal', 'vertical']:
        raise ValueError("Orientation must be either 'horizontal' or 'vertical'.")
    if orientation == 'horizontal':
        x, y = x, 'count()'
    else:
        x, y = 'count()', x
    

    # Create the histogram chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(x, title=None, axis=alt.Axis(ticks=False)).bin(maxbins=20).stack(None) if orientation == 'horizontal' else alt.X(x, title=None).stack(None),
        y=alt.Y(y, title=None).stack(None) if orientation == 'horizontal' else alt.Y(x, title=None, axis=alt.Axis(ticks=False)).bin(maxbins=20).stack(None),
        color=alt.Color(hue, title=None) if hue else alt.value(color)
    )


    return chart

def DensityChart(data, x: str, hue: str = None, color: str = 'blue', orientation: str = 'horizontal'):
    '''
    Create a density chart for the specified variable.
    '''

    pass


def BoxPlotChart(data, x: str, y: str, hue: str = None, color: str = 'blue', orientation: str = 'horizontal'):
    '''
    Create a box plot chart for the specified variable.
    '''

    chart = alt.Chart(data).mark_boxplot().encode(
        x=alt.X(x, title=None) if orientation == 'horizontal' else alt.X(y, title=None),
        y=alt.Y(y, title=None) if orientation == 'horizontal' else alt.Y(x, title=None),
        color=alt.Color(hue, title=None) if hue else alt.value(color)
    )
    return chart

def ViolinChart(data, x: str, y: str, hue: str = None, color: str = None, orientation: str = 'horizontal'):
    '''
    Create a violin chart for the specified variable.
    '''

    chart = alt.Chart(data).mark_area().encode(
        x=alt.X(x, title=None) if orientation == 'horizontal' else alt.X(y, title=None),
        y=alt.Y(y, title=None) if orientation == 'horizontal' else alt.Y(x, title=None),
        color=alt.Color(hue, title=None) if hue else alt.value(color)
    )
    return chart