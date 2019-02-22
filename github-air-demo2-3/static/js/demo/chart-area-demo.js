// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';


config2 = {
  type: 'line',
  data: {
    labels: ["00:00", "01:00"],
    datasets: [{
      label: '高雄-鳳山',
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointBorderWidth: 2,
      pointHitRadius: 50,
      data: [53, 53],
      fill: false,
    }],
  },
  options: {
    /*
    legend: {
      display: false
    }
    */
    responsive: true,
    title: {
      display: true,
      text: 'PM2.5'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },

  }
}
var ctx = document.getElementById("myAreaChart2");
var myLineChart2 = new Chart(ctx, config2);