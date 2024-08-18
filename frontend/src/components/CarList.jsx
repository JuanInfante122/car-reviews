import React, { useState } from 'react';
import CarCard from './CarCard';
import './CarList.css';

const CarList = ({ cars }) => {
  const [expandedCar, setExpandedCar] = useState(null);

  const handleCardClick = (car) => {
    setExpandedCar(expandedCar === car ? null : car);
  };

  return (
    <div className="car-list">
      {cars.map((car) => (
        <CarCard
          key={car.name}
          name={car.brand + " " + car.name}
          image={car.image}
          rating={car.rating}
          summary={car.summary}
          isExpanded={expandedCar === car}
          onClick={() => handleCardClick(car)}
          starDistribution={car.starDistribution}
          ratingChange={car.ratingChange} // Pasar ratingChange
        />
      ))}
    </div>
  );
};

export default CarList;
