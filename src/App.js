import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [stage, setStage] = useState(0);
  const [message, setMessage] = useState('Please select your game intensity');
  const [selectedButton, setSelectedButton] = useState('');

  useEffect(() => {
    if (stage === 2) {
      fetch(`http://localhost:5000/get-file-data/${selectedButton}`)
        .then(response => response.json())
        .then(data => setData(data))
        .catch(error => console.error(error));
    }
  }, [stage, selectedButton]);

  const handleButtonClick = (buttonLabel) => {
    setSelectedButton(buttonLabel);
    // Send the selected button to the backend
    fetch('http://localhost:5000/generate-pokemon-team', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: buttonLabel }),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => console.error('Error:', error));

    switch(stage) {
      case 0:
        setMessage('Please select your generation');
        setStage(1);
        break;
      case 1:
        setMessage('Please select your Pokemon');
        setStage(2);
        break;
      case 2:
        setMessage('team_recommendations');
        setStage(3);
        break;
      default:
        break;
    }
  }

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>{message}</h1>
      {stage === 0 && (
        <div>
          <button onClick={() => handleButtonClick('Casual')}>Casual</button>
          <button onClick={() => handleButtonClick('Competitive')}>Competitive</button>
        </div>
      )}
      {stage === 1 && (
        <div>
          {['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'].map((numeral) => (
            <button key={numeral} onClick={() => handleButtonClick(numeral)}>{numeral}</button>
          ))}
        </div>
      )}
      {stage === 2 &&(
        <div style={{ overflowY: 'scroll', maxHeight: '200px' }}>
        {data.map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>
      )}
      <p>Selected Button: {selectedButton}</p>
    </div>
  );
}

export default App;
