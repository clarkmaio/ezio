
import polars as pl
import altair as alt
from typing import Optional, List, Dict
from ezio.base.chart import BaseChart


class ScatterChart(BaseChart):

    def __init__(self, data: pl.DataFrame):

        super().__init__()

    def _build_components(self):
        pass

    def assemble(self, components: Dict, height: int = 300, width: int = 1000):
        pass




def ScatterChart(data: pl.DataFrame, x: str, y: str, hue: Optional[str] = None, 
            color: str = 'blue',
            marginaly: Optional[str] = None,
            marginalx: Optional[str] = None,
            title: Optional[str] = None, height: int = 400, width: int = 1000) -> alt.Chart:
    

    selection = alt.selection_interval(encodings=['x', 'y'])
    legend_selection = alt.selection_point(fields=[hue], bind='legend')
    


    base = alt.Chart(data)
    base_bar = alt.Chart(data).mark_bar(binSpacing=0, opacity=0.5)

    scatter_base = base.mark_point().encode(
        x=alt.X(x, title=None),
        y=alt.Y(y, title=None),
        color=alt.Color(hue, title=None, legend=alt.Legend(orient='top')) if hue else alt.value(color),
        opacity=alt.condition(selection, alt.value(0.8), alt.value(0.1)),
        tooltip=[x, y] + ([hue] if hue else [])
    ).add_params(
        selection
    ).properties(
        height=height,
        width=width
    )

    # if marginaly:
    #     marginaly_chart = HistogramChart(
    #         data=data,
    #         x=y,
    #         hue=hue,
    #         color=color,
    #         orientation='vertical'
    #     ).properties(
    #         height=height,
    #         width=100
    #     )
    
    if marginalx:
        marginalx_chart_base = base_bar.encode(
            x=alt.X(x, title=None, axis=alt.Axis(ticks=False)).bin(maxbins=20),
            y=alt.Y('count()', title=None),
            color=alt.Color(hue, title=None, legend=alt.Legend(orient='top')) if hue else alt.value(color)
        ).properties(
            height=100,
            width=width
        )

        marginalx_chart_selection = base_bar.transform_filter(
            selection
        ).encode(
            x=alt.X(x, title=None, axis=alt.Axis(ticks=False)).bin(maxbins=20),
            y=alt.Y('count()', title=None),
            color=alt.Color(hue, title=None, legend=alt.Legend(orient='top')) if hue else alt.value(color),
        ).properties(
            height=100,
            width=width
        )

        marginalx_chart = marginalx_chart_selection



        # marginalx_chart = HistogramChart(
        #     data=data,
        #     x=x,
        #     hue=hue,
        #     color=color,
        #     orientation='horizontal'
        # ).properties(
        #     height=100,
        #     width=width
        # )

    if marginaly and marginalx:
        chart = marginalx_chart & (scatter_base | marginaly_chart)
    elif marginaly:
        chart = scatter_base | marginaly_chart
    elif marginalx:
        chart = marginalx_chart & scatter_base
    else:
        chart = scatter_base




    if title:
         chart = chart.properties(title=alt.Title(text=title, anchor='middle', fontSize=15, fontWeight='bold'))
    return chart