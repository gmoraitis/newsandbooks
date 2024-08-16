import React, { useState } from 'react';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setProducts(data.products);
        setMessage('');
      } else {
        setMessage(data.message);
        setProducts([]);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('An error occurred. Please try again.');
    }
  };

  const handleLogout = async () => {
    await fetch('http://127.0.0.1:5000/logout', {
      method: 'POST',
    });
    setName('');
    setPassword('');
    setProducts([]);
    setMessage('');
  };

  return (
    <div className="App">
      <h1>News&Books</h1>
      {products.length === 0 ? (
        <div className="card">
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
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
