

import altair as alt    
from typing import Optional, List
import polars as pl




def NearestRule(data: pl.DataFrame, x: str, filters: Optional[List] = [], color: str = 'black') -> alt.Chart:
    """
    Draw a line rule at the nearest point on the x-axis.
    This function creates a rule that highlights the nearest point on the x-axis when hovered over.

    Parameters:
    - data (pl.DataFrame): The data to plot.
    - x (str): The column name for the x-axis.
    - filters (Optional[List]): List of filters to apply.

    Returns:
    - alt.Chart: The Altair chart with the nearest rule.
    """
    nearest = alt.selection_point(nearest=True, on="pointerover", fields=[x], empty=False)

    selector = alt.Chart(data).mark_point().encode(
        x=alt.X(x, title=None),
        opacity=alt.value(0.)
    ).transform_filter(
        *filters
    ).add_params(
        nearest,
    )

    rule = alt.Chart(data).mark_rule(color=color).encode(
        x=alt.X(x, title=None),
    ).transform_filter(
        nearest,
        *filters
    )
    return selector + rule

