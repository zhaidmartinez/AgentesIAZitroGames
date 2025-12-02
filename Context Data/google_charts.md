# Google Charts Basics

## 1. Introduction
Google Charts is a JavaScript library for data visualization. It allows developers to create dynamic and interactive charts from structured data like arrays or JSON.

## 2. Loading the Library
```html
<script src="https://www.gstatic.com/charts/loader.js"></script>
<script>
  google.charts.load('current', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(drawChart);
</script>
```

## 3. Creating a Basic Chart
```html
<div id="chart_div"></div>
<script>
  function drawChart() {
    const data = google.visualization.arrayToDataTable([
      ['Year', 'Sales', 'Expenses'],
      ['2021', 1000, 400],
      ['2022', 1170, 460],
      ['2023', 660, 1120],
      ['2024', 1030, 540]
    ]);

    const options = {
      title: 'Company Performance',
      curveType: 'function',
      legend: { position: 'bottom' }
    };

    const chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
</script>
```

## 4. Supported Chart Types
- LineChart
- ColumnChart
- PieChart
- AreaChart
- ComboChart
- BarChart
- ScatterChart
- Gauge
- GeoChart
- Table

### 4.1 Scatter Chart Example
Note: Scatter charts require NUMERIC data on BOTH axes. For categorical labels (like product names), use ColumnChart or BarChart instead.

```html
<div id="chart_div"></div>
<script>
  function drawChart() {
    const data = google.visualization.arrayToDataTable([
      ['Horas de Estudio', 'Calificación'],
      [2, 65],
      [3, 70],
      [4, 75],
      [5, 80],
      [6, 83],
      [7, 87],
      [8, 90],
      [9, 92],
      [10, 95]
    ]);

    const options = {
      title: 'Relación entre Horas de Estudio y Calificaciones',
      hAxis: { title: 'Horas de Estudio' },
      vAxis: { title: 'Calificación' },
      legend: 'none',
      pointSize: 5,
      colors: ['#2196f3']
    };

    const chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
</script>
```

### 4.1b Column Chart for Categorical Data
For data with text labels (like product names), use ColumnChart:

```html
<div id="chart_div"></div>
<script>
  function drawChart() {
    const data = google.visualization.arrayToDataTable([
      ['Producto', 'Rendimiento'],
      ['Producto A', 75],
      ['Producto B', 82],
      ['Producto C', 68],
      ['Producto D', 91],
      ['Producto E', 77]
    ]);

    const options = {
      title: 'Análisis de Rendimiento',
      hAxis: { title: 'Producto' },
      vAxis: { title: 'Rendimiento (%)' },
      legend: 'none',
      colors: ['#4caf50']
    };

    const chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
</script>
```

### 4.2 Radar Chart (Using Chart.js Alternative)
Note: Google Charts doesn't support radar charts natively. Use Chart.js for radar charts:
```html
<canvas id="radarChart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const ctx = document.getElementById('radarChart').getContext('2d');
  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Comunicación', 'Liderazgo', 'Técnico', 'Creatividad', 'Trabajo en equipo'],
      datasets: [{
        label: 'Evaluación de Competencias',
        data: [8, 7, 9, 6, 8],
        backgroundColor: 'rgba(33, 150, 243, 0.2)',
        borderColor: 'rgba(33, 150, 243, 1)',
        borderWidth: 2
      }]
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
          max: 10
        }
      }
    }
  });
</script>
```

### 4.3 Area Chart Example
Area charts display quantitative data visually with filled areas under lines:
```html
<div id="chart_div"></div>
<script>
  google.charts.load('current', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    const data = google.visualization.arrayToDataTable([
      ['Mes', 'Ventas'],
      ['Enero', 45000],
      ['Febrero', 52000],
      ['Marzo', 48000],
      ['Abril', 61000],
      ['Mayo', 58000],
      ['Junio', 65000]
    ]);

    const options = {
      title: 'Ventas Mensuales',
      hAxis: { title: 'Mes' },
      vAxis: { title: 'Ventas' },
      legend: 'none',
      colors: ['#4caf50']
    };

    const chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
</script>
```


## 5. Customizing Appearance
```js
const options = {
  title: 'Website Traffic',
  backgroundColor: '#f9f9f9',
  colors: ['#4caf50', '#2196f3'],
  chartArea: { width: '80%', height: '70%' },
  hAxis: { title: 'Month' },
  vAxis: { title: 'Visitors', minValue: 0 },
  legend: { position: 'bottom' }
};
```

## 6. Adding Interactivity
```js
google.visualization.events.addListener(chart, 'select', () => {
  const selection = chart.getSelection();
  if (selection.length > 0) {
    const row = selection[0].row;
    alert('You selected: ' + data.getValue(row, 0));
  }
});
```

## 7. Dashboards and Filters
```html
<div id="dashboard_div">
  <div id="filter_div"></div>
  <div id="chart_div"></div>
</div>

<script>
google.charts.load('current', { packages: ['corechart', 'controls'] });
google.charts.setOnLoadCallback(drawDashboard);

function drawDashboard() {
  const data = google.visualization.arrayToDataTable([
    ['Year', 'Sales', 'Expenses'],
    ['2020', 1000, 400],
    ['2021', 1170, 460],
    ['2022', 660, 1120],
    ['2023', 1030, 540]
  ]);

  const dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

  const yearFilter = new google.visualization.ControlWrapper({
    controlType: 'CategoryFilter',
    containerId: 'filter_div',
    options: {
      filterColumnLabel: 'Year',
      ui: { allowTyping: false, allowMultiple: false }
    }
  });

  const chart = new google.visualization.ChartWrapper({
    chartType: 'ColumnChart',
    containerId: 'chart_div',
    options: { title: 'Filtered Sales' }
  });

  dashboard.bind(yearFilter, chart);
  dashboard.draw(data);
}
</script>
```

## 8. Exporting Charts
```js
const imgURI = chart.getImageURI();
console.log('Exported chart image URI:', imgURI);
```

## 9. Complete Examples

### 9.1 Scatter Chart with Multiple Data Points
```html
<div id="chart_div"></div>
<script>
  google.charts.load('current', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    const data = google.visualization.arrayToDataTable([
      ['Producto', 'Rendimiento'],
      ['Producto A', 75],
      ['Producto B', 82],
      ['Producto C', 68],
      ['Producto D', 91],
      ['Producto E', 77]
    ]);

    const options = {
      title: 'Análisis de Rendimiento',
      hAxis: { title: 'Producto' },
      vAxis: { title: 'Rendimiento (%)' },
      legend: 'none',
      pointSize: 7,
      colors: ['#4caf50']
    };

    const chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
</script>
```

### 9.2 Radar Chart for Skills Assessment
```html
<canvas id="chart_div" width="400" height="400"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const ctx = document.getElementById('chart_div').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Comunicación', 'Liderazgo', 'Técnico', 'Creatividad', 'Trabajo en equipo'],
      datasets: [{
        label: 'Evaluación de Competencias',
        data: [8, 7, 9, 6, 8],
        fill: true,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        pointBackgroundColor: 'rgb(255, 99, 132)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(255, 99, 132)'
      }]
    },
    options: {
      elements: {
        line: {
          borderWidth: 3
        }
      },
      scales: {
        r: {
          angleLines: {
            display: true
          },
          suggestedMin: 0,
          suggestedMax: 10
        }
      }
    }
  });
</script>
```

### 9.3 Area Chart with Multiple Series
```html
<div id="chart_div"></div>
<script>
  google.charts.load('current', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    const data = google.visualization.arrayToDataTable([
      ['Mes', 'Producto A', 'Producto B'],
      ['Enero', 45000, 38000],
      ['Febrero', 52000, 42000],
      ['Marzo', 48000, 45000],
      ['Abril', 61000, 48000],
      ['Mayo', 58000, 52000],
      ['Junio', 65000, 55000]
    ]);

    const options = {
      title: 'Comparación de Ventas por Producto',
      hAxis: { title: 'Mes' },
      vAxis: { title: 'Ventas' },
      isStacked: false,
      colors: ['#4caf50', '#2196f3']
    };

    const chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
</script>
```
