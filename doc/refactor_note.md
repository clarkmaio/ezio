

# Syntax notes

```
(
    TimeseriesChart(data=data, 
             x='x', 
             y=['a', 'b', 'y'], 
             color=[])
    .add_signbar(y='sign', position='bottom')
    .add_view(y=['a', 'b'])
    .add_crossfilter(x='x', y='y', position='left')
    .render()
)
```