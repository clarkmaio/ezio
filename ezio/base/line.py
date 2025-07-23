
import altair as alt
import polars as pl
from typing import List, Optional, Dict
from ezio.base.chart import BaseChart



class LineChart(BaseChart):
    def __init__(self, 
                 data: pl.DataFrame,
                 x: str,
                 y: List[str], 
                 title: Optional[str] = None,
                 colors: Optional[List[str]] = None,
                 hoverdata: Optional[List[str]] = None,
                 ytitle: Optional[str] = None,
                 xtitle: Optional[str] = None):
        self.data = data
        self.x = x
        self.y = y
        self.title = title
        self.colors = colors
        self.ytitle = ytitle
        self.xtitle = xtitle
        self.hoverdata = hoverdata

        super(LineChart, self).__init__()


    def _build_components(self):

        # Selection tools
        legend_selection = alt.selection_point(fields=['variable'], bind='legend')


        scale = alt.Scale(domain=self.y, range=self.colors) if self.colors else alt.Scale(domain=self.y)
        line = alt.Chart(self.data).transform_fold(
            self.y,
            as_=['variable', 'value']
        ).mark_line().encode(
            x=alt.X(self.x, title=self.xtitle),
            y=alt.Y('value:Q', title=self.ytitle),
            color=alt.Color('variable:N', title=None, 
                            legend=alt.Legend(orient='top', symbolType='circle', symbolStrokeWidth=3.),
                            scale=scale,
                        ),
            opacity=alt.condition(legend_selection, alt.value(1), alt.value(0.2)),
            tooltip=[alt.Tooltip(h) for h in self.hoverdata] if self.hoverdata else []
        ).add_params(
            legend_selection,
        )

        components = {
            'legend_selection': legend_selection,
            'line': line,
        }
        return components

    def assemble(self, components: Dict, height: int = 300, width: int = 1000):
        line = components['line'].properties(
            height=height, width=width
        )
        self._chart = line
        
        if self.title:
            self._chart = self._chart.properties(title=alt.Title(text=self.title, anchor='middle', fontSize=15, fontWeight='bold'))

        return self._chart.interactive()


