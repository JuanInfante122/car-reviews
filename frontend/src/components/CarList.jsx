import React from 'react';
import CarCard from './CarCard';
import './CarList.css'; // Estilos específicos para la lista

const CarList = ({ cars }) => {
  return (
    <div className="car-list">
      {cars.map(car => (
        <CarCard
          key={car.name}
          name={car.brand + " " + car.name}
          image={car.image}
          rating={car.rating}
          summary={car.summary}
        />
      ))}
    </div>
  );
};

export default CarList;
