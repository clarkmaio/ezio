
import polars as pl
import altair as alt
from typing import Optional, List, Tuple

from ezio.base.rule import NearestRule
from ezio.base.bar import SignBarChart
from ezio.base.chart import BaseChart



class LineChart(BaseChart):

    def __init__(self, 
                 data: pl.DataFrame,
                 x: str, 
                 y: List[str],
                 yview: List[str] = None,
                 colors: List[str] = None,
                 ytitle: str = None,
                 xtitle: str = None,
    ):
        
        self.data = data
        self.x = x
        self.y = y
        self.colors = colors
        self.ytitle = ytitle
        self.xtitle = xtitle


        super(LineChart, self).__init__()   

    def _build_components(self):
        return {
            'zoom': None,
            'view': None,
            'interval_selection': None,
            'legend_selection': None,
            'scatter_selection': None,
            'vrule': None,
            'scale': None,
            'bar': None,
            'scatter': None,
        }

    def add_scatter(self, x: str, y: str, position: str = 'right', color: str = 'black', hue: str = None, highlight_color: str = 'red') -> None:
        """
        Adds a cross-filter component to the chart.
        
        Args:
            x (str): The x-axis field for the cross-filter.
            y (str): The y-axis field for the cross-filter.
            position (str): The position of the cross-filter in the chart layout.
        """
        self._components['scatter'] = {
            'x': x,
            'y': y,
            'position': position,
            'color': color,
            'hue': hue,
            'highlight_color': highlight_color,
            'plot': None
        }
        return self
    
    def add_bar(self, y: str, color: str = None, ytitle: str = None):
        
        self._components['bar'] = {
            'y': y,
            'color': color,
            'ytitle': ytitle,
            'plot': None
        }
        
        return self
    
    def add_view(self, y: List[str], position: str = 'top'):
        """
        Adds view component to the chart.
        
        Args:
            x (str): The x-axis field for the cross-filter.
            y (str): The y-axis field for the cross-filter.
            position (str): The position of the cross-filter in the chart layout.
        """

        self._components['view'] = {
            'y': y,
            'position': position,
            'plot': None
        }
        return self   

    def add_vrule(self, color: str = 'black'):
        """
        Adds a vertical rule to the chart.
        
        Args:
            color (str): The color of the vertical rule.
        """
        self._components['vrule'] = {
            'color': color,
            'plot': None
        }
        return self
    
    def _render_scatter(self):
        """
        Render scatter component
        """

        # scatter_base = alt.Chart(self.data).mark_circle().encode(
        #     x = alt.X(self._components['scatter']['x'], title=None),
        #     y = alt.Y(self._components['scatter']['y'], title=None),
        #     color = alt.value(self._components['scatter']['color']),
        #     opacity = alt.value(0.05)
        # )

        # scatter = scatter_base.encode(
        #     opacity=alt.value(1.)
        # ).transform_filter(
        #     self._components['interval_selection']
        # ).add_params(
        #     self._components['scatter_selection']
        # )

        # return scatter_base + scatter


        scatter_base = alt.Chart(self.data).mark_circle().encode(
            x=alt.X(self._components['scatter']['x'], title=None),
            y=alt.Y(self._components['scatter']['y'], title=None),
            color=alt.value(self._components['scatter']['color']),
            opacity=alt.condition(self._components['interval_selection'], alt.value(1), alt.value(0.05))
        ).add_params(
            self._components['scatter_selection']
        )
    
        return scatter_base
    
    def _render_vrule(self):
        """
        Render vertical rule
        """
        vrule = NearestRule(data=self.data, 
                            x=self.x, 
                            color=self.components['vrule']['color'], 
                            filters=[self.components['interval_selection']])
        self._components['vrule']['plot'] = vrule
        return vrule


    def _render_bar(self):
        """
        Render bar chart
        """
        bar = SignBarChart(data=self.data, 
                        x=self.x, y=self.components['bar']['y'], 
                        ytitle = self.components['bar']['ytitle'], filters=[self.components['interval_selection']])

        self._components['bar']['plot'] = bar
        return bar
    

    def _render_zoom(self):
        """
        Render main line plot
        """

        zoom = alt.Chart(self.data).transform_fold(
            self.y, as_=['variable', 'value']
        ).mark_line(
            #interpolate='step'
        ).encode(
            x=alt.X(self.x, title=None),
            y=alt.Y('value:Q', title=self.ytitle),
            color=alt.Color('variable:N', title=None, 
                            legend=alt.Legend(orient='top', symbolType='circle', symbolStrokeWidth=3.),
                            scale=self.components['scale'],
                        ),
            opacity=alt.condition(self._components['legend_selection'], alt.value(1), alt.value(0.2)),
        ).add_params(
            self._components['legend_selection'],
        )

        if self.components['scatter']:
            scatter_selection = alt.Chart(self.data).mark_circle().encode(
                x=alt.X(self.x, title=None),
                y=alt.Y(self.y[0], title=self.ytitle),
                color=alt.value(self._components['scatter']['highlight_color']),
            ).transform_filter(
                self.components['scatter_selection']
            )
            zoom = zoom + scatter_selection


        if self.components['view']:
            zoom = zoom.transform_filter(self.components['interval_selection'])

        return zoom

    def _render_view(self):
        """
        Render view plot
        """

        view = alt.Chart(self.data).transform_fold(
            self.components['view']['y'], as_=['variable', 'value']
        ).mark_line(
            interpolate='step'
        ).encode(
            x=alt.X(self.x, title=None),
            y=alt.Y('value:Q', title=None),
            color=alt.Color('variable:N', title=None, scale=self.components['scale']),
        ).add_params(
            self.components['interval_selection'], 
            self.components['legend_selection']
        )
        return view

    def assemble(self, components, width, height):
        self.components['interval_selection'] = alt.selection_interval(encodings=['x'], empty='all')
        self.components['legend_selection'] = alt.selection_point(fields=['variable'], bind='legend')
        self.components['scatter_selection'] = alt.selection_interval(encodings=['x', 'y'], empty=False)
        self.components['nearest_rule'] = NearestRule(data=self.data, x=self.x, color='black', filters=[self.components['interval_selection']])
        self.components['scale'] = alt.Scale(domain=self.y, range=self.colors) if self.colors else alt.Scale(domain=self.y)


        zoom = self._render_zoom()
        if self.components['bar']:
            bar = self._render_bar()
            zoom = (zoom + bar).resolve_scale(y='independent')

        if self.components['vrule']:
            vrule = self._render_vrule()
            zoom = zoom + vrule

        if self.components['view']:
            view = self._render_view().properties(height=height * 1/5, width=width)
            zoom = zoom.properties(height=height * 4/5, width=width)
            self._chart = zoom & view
        else:
            zoom = zoom.properties(height=height, width=width)
            self._chart = zoom

        if self.components['scatter']:
            cf = self._render_scatter().properties(height=height, width=height)
            self._chart = self._chart | cf




        return self._chart


