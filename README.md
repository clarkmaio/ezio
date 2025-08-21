

# ezio (an altair wrapper)


> I will dedicate my life to make people stop using plotly.
>
> -- <cite>Benjamin Franklin</cite>


The idea behind this package is quite simple: create a wrapper of [altair](https://altair-viz.github.io/) similar to what [plotly-express](https://plotly.com/python/plotly-express/) did for plotly.

My hope is to remove friction while creating simple plots. Big focus on interaction between subplots that I think is the killing feature of `altair`.

The motto of this packae is modularity. No fuctions with 1 billion parameters (I'm looking at you plotly) but rather multiple methods to concatenate at will.



## Demo

In this marimo you will find few examples.

Here a tiny demo:


```
import polars as pl
import ezioaltair as ez
import numpy as np
from datetime import date

N = 100
data = pl.DataFrame({
    'time': pl.date_range(start=date(2025, 1, 1), 
                          end=date(2025, 1, 1) + pl.duration(days=N-1), 
                          interval='1d',
                         eager=True),
    'var1': (np.random.randn(N) + np.linspace(0, 10, N)).tolist(),
    'var2': (np.random.randn(N)*0.2 + np.sin(np.linspace(0, 10, N))).tolist(),
})

(
    ez.LineChart(data=data, 
                    x='time', 
                    y=['var1', 'var2'],
                   colors=['red', 'black'], ytitle='y axis title', xtitle='x axis')
    .add_view(y=['var1'])
    .add_scatter(x='var1', y='var2', highlight_color='green', color='blue')
    .add_title('This is a title')
    .render(height=300, width=500)
)
```
