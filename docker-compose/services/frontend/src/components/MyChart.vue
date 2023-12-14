<script>
import Chart from 'chart.js/auto';
import { watch, onMounted, ref, nextTick } from 'vue';

export default {
  props: {
    stockData: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const chartRef = ref(null);
    let myChart = null;

    const createChart = () => {
      var ctx = chartRef.value.getContext('2d');
      myChart = new Chart(ctx, {
        type: 'line',
        data: getChartData(),
        options: getChartOptions(),
      });
    };

    const getChartData = () => {
      return {
        labels: props.stockData.map(item => new Date(item.timestamp * 1000).toLocaleDateString()),
        datasets: [{
          label: 'Stock Price',
          data: props.stockData.map(item => item.price),
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      };
    };

    const getChartOptions = () => {
      return {
        scales: {
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: 'Price'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Date'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Stock Price Over Time'
          }
        }
      };
    };

    const updateChart = () => {
      myChart.data = getChartData();
      myChart.update();
    };

    watch(() => props.stockData, (newVal, oldVal) => {
      if (newVal !== oldVal) {
        nextTick(() => {
          updateChart();
        });
      }
    });

    onMounted(createChart);

    return {
      chartRef
    };
  }
}
</script>

<template>
  <div>
    <canvas ref="chartRef"></canvas>
  </div>
</template>
