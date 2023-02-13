<template>
  <Bar
      id="my-chart-id"
      :data="chartData"
      :options="chartOptions"
  />
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: { Bar },

  props: {
    xValues: null,
    yValues: null,
    barColors: null,
    list_name: null
  },

  data() {
    return {
      chartData: {
        labels: this.xValues,
        datasets: [ {
          label: ["Total Number of Cards"],
          backgroundColor: this.barColors,
          data: this.yValues } ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: this.list_name,
            font: {
              size: 20,
              family: 'monospace'
            },
          },
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: "Card Status",
              color: this.fontColor,
            },
          },
          y: {
            display: true,
            title: {
              display: true,
              text: "Number of Cards",
              color: this.fontColor,
            },
          },
        },
      }
    }
  },

}
</script>

<style scoped>

</style>