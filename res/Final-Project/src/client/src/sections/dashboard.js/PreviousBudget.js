import React, { useState } from 'react';
import ReactApexChart from 'react-apexcharts';

const PreviousBudget = () => {
  const [options] = useState({
    annotations: {
      points: [
        {
          x: '',
          seriesIndex: 0,
          label: {
            borderColor: '#775DD0',
            offsetY: 0,
            style: {
              color: '#fff',
              background: '#775DD0',
            },
          },
        },
      ],
    },
    chart: {
      height: 350,
      type: 'bar',
    },
    plotOptions: {
      bar: {
        borderRadius: 10,
        columnWidth: '30%',
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      width: 2,
    },

    grid: {
      row: {
        colors: ['#fff', '#f2f2f2'],
      },
    },
    xaxis: {
      labels: {
        rotate: -45,
      },
      categories: [
        'תשתיות',
        'החזרי חוב',
        ' ביטחון וסדר ציבורי',
        'שירותים חברתיים',
        'ענפי משק',
        'משרדי מטה',
        'הוצאות אחרות',
      ],
      tickPlacement: 'on',
    },

    fill: {
      type: 'gradient',
      gradient: {
        shade: 'light',
        type: 'horizontal',
        shadeIntensity: 0.25,
        gradientToColors: undefined,
        inverseColors: true,
        opacityFrom: 0.85,
        opacityTo: 0.85,
        stops: [50, 0, 100],
      },
    },
  });

  const [series] = useState([
    {
      name: 'Amount in Billion',
      data: [48.29, 57.62, 98.74, 225.38, 10.14, 28.65, 32.31],
    },
  ]);

  return (
    <div id="chart">
      <ReactApexChart options={options} series={series} type="bar" height={350} style={{ textAlign: 'center' }} />
    </div>
  );
};

export default PreviousBudget;
