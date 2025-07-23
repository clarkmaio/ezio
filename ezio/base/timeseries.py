
import polars as pl
import altair as alt
from typing import Optional, List, Tuple

from ezio.base.rule import NearestRule
from ezio.base.bar import SignBarChart
from ezio.base.chart import BaseChart



class TimeseriesChart(BaseChart):

    def __init__(self, 
                 data: pl.DataFrame,
                 x: str, 
                 y: List[str],
                 yview: List[str] = None,
                 colors: List[str] = None,
                 signbar: str = None,
                 title: str = None,
                 ytitle: str = None,
                 ytitlebar: str = None,
                 cross_filter: Optional[Tuple[str, str]] = None):
        
        self.data = data
        self.x = x
        self.y = y
        self.yview = yview
        self.colors = colors
        self.signbar = signbar
        self.title = title
        self.ytitle = ytitle
        self.ytitlebar = ytitlebar
        self.cross_filter = cross_filter


        super(TimeseriesChart, self).__init__()        

    def _build_components(self):

        # Selection tools
        interval_selection = alt.selection_interval(encodings=['x'])
        legend_selection = alt.selection_point(fields=['variable'], bind='legend')
        nearest_rule = NearestRule(data=self.data, x=self.x, color='black', filters=[interval_selection])

        # bar
        bar = None
        if self.signbar is not None:
            bar = SignBarChart(data=self.data, 
                               x=self.x, y=self.signbar, 
                               ytitle = self.ytitlebar, filters=[interval_selection])


        # zoom
        yview = self.yview if self.yview is not None else self.y
        ytot = self.y + [yy for yy in yview if yy not in self.y]
        scale = alt.Scale(domain=ytot, range=self.colors) if self.colors else alt.Scale(domain=ytot)
        zoom = alt.Chart(self.data).transform_fold(
            self.y, as_=['variable', 'value']
        ).transform_filter(
            interval_selection
        ).mark_line(
            interpolate='step'
        ).encode(
            x=alt.X(self.x, title=None),
            y=alt.Y('value:Q', title=self.ytitle),
            color=alt.Color('variable:N', title=None, 
                            legend=alt.Legend(orient='top', symbolType='circle', symbolStrokeWidth=3.),
                            scale=scale,
                        ),
            opacity=alt.condition(legend_selection, alt.value(1), alt.value(0.2)),
        ).add_params(
            legend_selection,
        )


        # view
        view = alt.Chart(self.data).transform_fold(
            yview, as_=['variable', 'value']
        ).mark_line(
            interpolate='step'
        ).encode(
            x=alt.X(self.x, title=None),
            y=alt.Y('value:Q', title=None),
            color=alt.Color('variable:N', title=None, scale=scale),
        ).add_params(
            interval_selection, legend_selection
        )

        components = {
            'interval_selection': interval_selection,
            'legend_selection': legend_selection,
            'nearest_rule': nearest_rule,
            'zoom': zoom,
            'view': view,
            'signbar': bar,
            'cross_filter': None
        }

        return components

    def assemble(self, components, width, height):
        
        zoom = components['zoom'].properties(height=height * 4/5, width=width)
        view = components['view'].properties(height=height * 1/5, width=width)
        bar = components['signbar']
        nr = components['nearest_rule']
        cf = components['cross_filter']

        if self.signbar is not None:
            zoom_chart = (zoom + bar).resolve_scale(y='independent')
        else:
            zoom_chart = zoom
        self._chart = (zoom_chart + nr) & view

        if self.cross_filter is not None:
            self._chart = self._chart | cf

        if self.title:
            self._chart = self._chart.properties(title=alt.Title(text=self.title, anchor='middle', fontSize=15, fontWeight='bold'))

        return self._chart



# def TimeSeriesChart(data: pl.DataFrame, 
#                  x: str, y: List[str], 
#                  y_view: Optional[List[str]] = None,
#                  colors: Optional[List[str]] = None,
#                  sign_bar: Optional[str] = None,
#                  title: Optional[str] = None,
#                  ytitle: Optional[str] = None,
#                  ytitle_bar: Optional[str] = None,
#                  cross_filter: Optional[Tuple[str, str]] = None,
#                  height: int = 400, width: int = 1000) -> alt.Chart:
#     """
#     Create a time series chart with zoom and selection capabilities.

#     Parameters:
#     - data (pl.DataFrame): The data to plot.
#     - x (str): The column name for the x-axis (time).
#     - y (List[str]): The column names for the y-axis variables.
#     - y_view (Optional[List[str]]): The column names for the view variables. Defaults to y if not provided.

#     Returns:
#     - alt.Chart: The rendered Altair chart.
#     """

#     # Selection tools
#     interval_selection = alt.selection_interval(encodings=['x'])
#     legend_selection = alt.selection_point(fields=['variable'], bind='legend')


#     # ---------------- cross filter ----------------
#     if cross_filter is not None:
#         cf = alt.Chart(data).mark_point().encode(
#             x=alt.X(cross_filter[0], title=None),
#             y=alt.Y(cross_filter[1], title=None),
#             color=alt.value('black'),
#             opacity=alt.condition(interval_selection, alt.value(8.), alt.value(0.2))
#         ).properties(
#             height=height+50,
#             width=height
#         )

        

#     # ---------------- zoom plot ----------------

#     if sign_bar is not None:
#         bar = SignBar(data=data, 
#                       x=x, y=sign_bar, 
#                       ytitle = ytitle_bar, filters=[interval_selection])

#     nearest_rule = NearestRule(data=data, x=x, color='black', filters=[interval_selection])


#     scale = alt.Scale(domain=y, range=colors) if colors else alt.Scale(domain=y)
#     zoom = alt.Chart(data).transform_fold(
#         y,
#         as_=['variable', 'value']
#     ).transform_filter(
#         interval_selection
#     ).mark_line(
#         interpolate='step'
#     ).encode(
#         x=alt.X(x, title=None),
#         y=alt.Y('value:Q', title=ytitle),
#         color=alt.Color('variable:N', title=None, 
#                         legend=alt.Legend(orient='top', symbolType='circle', symbolStrokeWidth=3.),
#                         scale=scale,
#                     ),
#         opacity=alt.condition(legend_selection, alt.value(1), alt.value(0.2)),
#     ).add_params(
#         legend_selection,
#     ).properties(
#         height=height * 4/5, width=width
#     )

#     # ---------------- view plot ----------------
#     view = alt.Chart(data).transform_fold(
#         y_view if y_view is not None else y,
#         as_=['variable', 'value']
#     ).mark_line(
#         interpolate='step'
#     ).encode(
#         x=alt.X(x, title=None),
#         y=alt.Y('value:Q', title=None),
#         color=alt.Color('variable:N', title=None, scale=scale),
#     ).add_params(
#         interval_selection,
#         legend_selection
#     ).properties(
#         height=height * 1/5, width=width
#     )

#     if sign_bar is not None:
#         zoom_chart = (zoom + bar).resolve_scale(y='independent')
#     else:
#         zoom_chart = zoom
#     chart = (zoom_chart + nearest_rule) & view

#     if cross_filter is not None:
#         chart = chart | cf

#     if title:
#         chart = chart.properties(title=alt.Title(text=title, anchor='middle', fontSize=15, fontWeight='bold'))
#     return chart