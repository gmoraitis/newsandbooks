import React, { useState, useEffect } from 'react';
import Keycloak from 'keycloak-js';
import './App.css';

function App() {
  const [keycloak, setKeycloak] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const initKeycloak = new Keycloak({
      url: 'http://localhost:8080/', 
      realm: 'news_books_realm',
      clientId: 'news_books_client',
    });

    initKeycloak.init({ onLoad: 'login-required' }).then(authenticated => {
      setKeycloak(initKeycloak);
      setAuthenticated(authenticated);
      if (authenticated) {
        fetchProducts(initKeycloak.token);
      }
    }).catch(error => {
      console.error('Keycloak initialization failed:', error);
      setMessage('Keycloak initialization failed. Please check console for details.');
    });
  }, []);

  const fetchProducts = async (token) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      console.log("Response Data:", data);

      if (response.ok) {
        setProducts(data.products);
        setMessage('');
      } else {
        setMessage(data.message);
        setProducts([]);
      }
    } catch (error) {
      console.error('Failed to fetch products:', error);
      setMessage('Failed to fetch products. Please try again.');
    }
  };

  const handleLogout = () => {
    if (keycloak) {
      keycloak.logout();
    }
  };

  return (
    <div className="App">
      <h1>News & Books</h1>
      {authenticated && products.length === 0 ? (
        <div className="card">
          <button onClick={() => fetchProducts(keycloak.token)}>Fetch Products</button>
          {message && <p>{message}</p>}
        </div>
      ) : (
        <div>
          <h2>Available Products</h2>
          <ul>
            {products.map((product, index) => (
              <li key={index}>{product}</li>
            ))}
          </ul>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
  );
}

export default App;
