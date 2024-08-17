import React from 'react';
import './CarCard.css';

const CarCard = ({ name, image, rating, summary }) => {
  return (
    <div className="car-card">
      <img src={image} alt={`${name}`} className="car-image" />
      <h2>{name}</h2>
      <p className="rating">Rating: {rating} / 5</p>
      <p className="summary">{summary}</p>
      <button className="button">Ver más detalles</button>
    </div>
  );
};

export default CarCard;
