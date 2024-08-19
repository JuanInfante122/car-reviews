import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import './CarCard.css';
import { ArrowUpward, ArrowDownward, ArrowForward } from '@mui/icons-material';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const CarCard = ({ name, image, rating, summary, isExpanded, onClick, starDistribution, ratingChange }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [],
      hoverBackgroundColor: []
    }]
  });

  useEffect(() => {
    if (starDistribution && Object.keys(starDistribution).length > 0) {
      const labels = ['1 Estrella', '2 Estrellas', '3 Estrellas', '4 Estrellas', '5 Estrellas'];
      const values = [];
      const colors = ['#FF6384', '#FF9F40', '#FFCD56', '#4BC0C0', '#36A2EB'];

      for (let i = 1; i <= 5; i++) {
        values.push(starDistribution[i] || 0);
      }

      const newChartData = {
        labels,
        datasets: [{
          data: values,
          backgroundColor: colors,
          hoverBackgroundColor: colors
        }]
      };

      setChartData(newChartData);
    }
  }, [starDistribution]);

  const handleFlip = (e) => {
    e.stopPropagation();
    setIsFlipped(!isFlipped);
  };

  const handleExpand = () => {
    onClick();
    setIsFlipped(false);
  };

  const getRatingChangeElement = () => {
    if (ratingChange === undefined || ratingChange === null) {
      return (
        <div className="rating-change neutral">
          <ArrowForward />
          <span>Sin cambios</span>
        </div>
      );
    }

    const isPositive = ratingChange > 0;
    const changeClass = isPositive ? 'positive' : 'negative';
    const ArrowIcon = isPositive ? ArrowUpward : ArrowDownward;

    return (
      <div className={`rating-change ${changeClass}`}>
        <ArrowIcon />
        <span>{Math.abs(ratingChange.toFixed(4))} puntos</span>
      </div>
    );
  };

  return (
    <div className={`car-card ${isFlipped ? 'flipped' : ''} ${isExpanded ? 'expanded' : ''}`} onClick={handleExpand}>
      <div className="car-card-inner">
        <div className="car-card-front">
          <img src={image} alt={`${name}`} className="car-image" />
          <h2>{name}</h2>
          <p className="rating">Rating: {rating} / 5</p>
          {getRatingChangeElement()}
          <div className="summary">{summary}</div>
          <button className="button" onClick={handleFlip}>Ver más detalles</button>
        </div>
        <div className="car-card-back">
          <h2>Calificaciones del vehiculo</h2>
          {chartData.datasets[0].data.length > 0 && (
            <Pie data={chartData} options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      let label = context.label || '';
                      if (context.parsed) {
                        label += `: ${context.parsed} opiniones`;
                      }
                      return label;
                    }
                  }
                }
              }
            }} />
          )}
          <button className="button" onClick={handleFlip}>Volver</button>
        </div>
      </div>
    </div>
  );
};

export default CarCard;
