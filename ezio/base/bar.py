
import polars as pl
import altair as alt
from typing import Optional, List, Tuple



def SignBarChart(data: pl.DataFrame, x: str, y: str, 
            ytitle: str = None, 
            scale_range: Optional[Tuple[float, float]] = None,
            filters: Optional[List[str]] = None,
            opacity: float = 0.8) -> alt.Chart:
    '''
    Simple bar chart using green and red colors to indicate positive and negative values.
    '''

    
    min_bar, max_bar = data[y].min(), data[y].max()
    range_bar = max_bar - min_bar
    scale = alt.Scale(domain=[min_bar, range_bar * 5]) if scale_range is None else alt.Scale(domain=scale_range)
    
    bar_base = alt.Chart(data).transform_fold(
        [y]
    ).transform_filter(
        *filters
    )


    bar_pos = bar_base.encode(
        x=alt.X(x, title=None),
        y=alt.Y('value:Q', title=ytitle,
                scale=scale),
        color=alt.value('lightgreen'),
        opacity=alt.condition(alt.datum.value > 0, alt.value(opacity), alt.value(0.0)),
    ).mark_bar(
        cornerRadiusEnd=10
    )

    bar_neg = bar_base.encode(
        x=alt.X(x, title=None),
        y=alt.Y('value:Q', title=ytitle,
                scale=scale),
        color=alt.value('red'),
        opacity=alt.condition(alt.datum.value < 0, alt.value(opacity), alt.value(0.0)),
    ).mark_bar(
        cornerRadiusBottomLeft=10,
        cornerRadiusBottomRight=10,
    )

    bar = bar_pos + bar_neg
    return bar