import React, { useState, useEffect } from 'react';
import CarList from './components/CarList';
import './App.css';

const mockCars = [
  {
    name: 'Sail',
    image: '/chevrolet-sail.jpg',
    logo: '/Chevrolet.png',
    brand: 'Chevrolet',
    rating: 4.2,
    summary: 'Loading...',
  },
  {
    name: 'Gol',
    image: 'volkswagen-gol.jpg',
    logo: '/Volkswagen.png',
    brand: 'Volkswagen',
    rating: 3.8,
    summary: 'Loading...',
  },
  {
    name: 'Hilux',
    image: '/toyota-hilux.jpg',
    logo: '/path-to-toyota-logo.png',
    brand: 'Toyota',
    rating: 4.7,
    summary: 'Loading...',
  },
];

const App = () => {
  const [selectedBrand, setSelectedBrand] = useState(null);
  const [cars, setCars] = useState(mockCars);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummaries = async () => {
      try {
        const updatedCars = await Promise.all(
          mockCars.map(async (car) => {
            // Construye la URL correctamente con el formato adecuado
            const response = await fetch(`http://localhost:5000/api/opinions?model=${car.brand.toLowerCase()}/${car.name.toLowerCase().replace(/\s+/g, '-')}`);
            const data = await response.json();
            return { ...car, summary: data.summary };
          })
        );
        setCars(updatedCars);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching summary:', error);
      }
    };

    fetchSummaries();
  }, []);

  const filterByBrand = (brand) => {
    setSelectedBrand(selectedBrand === brand ? null : brand);
  };

  return (
    <div className="App">
      <header className="header">
        <img src="/opinautos-logo.png" alt="Company Logo" />
        <h1>Miles de personas con el mismo auto... y los mismos problemas</h1>
        <div className="brand-buttons">
          <img
            src="/Chevrolet.png"
            alt="Chevrolet"
            className="brand-logo"
            onClick={() => filterByBrand('Chevrolet')}
          />
          <img
            src="/Volkswagen.png"
            alt="Volkswagen"
            className="brand-logo"
            onClick={() => filterByBrand('Volkswagen')}
          />
          <img
            src="/Toyota.png"
            alt="Toyota"
            className="brand-logo"
            onClick={() => filterByBrand('Toyota')}
          />
        </div>
      </header>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <CarList cars={selectedBrand ? cars.filter(car => car.brand === selectedBrand) : cars} />
      )}
    </div>
  );
};

export default App;
