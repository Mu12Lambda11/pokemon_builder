import React, { useEffect, useState } from 'react';
import Select from "react-select";
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [stage, setStage] = useState(0);
  const [message, setMessage] = useState('Please select your game intensity');
  const [selectedButton, setSelectedButton] = useState('');
  const [gameIntensity, setGameIntensity] = useState(false);
  const [selectedPokemon, setPokemon] = useState('');

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
        //for now the application only supports selecting competitive
        if (selectedButton=='Competitive'){
          setGameIntensity(true);
        }
        setMessage('Please select your generation');
        setStage(1);        
        break;
      case 1:
        //Intensity selected
        setMessage('Please select your Format');
        setStage(2);        
        break;
      case 2:
        //Generation selected
        setMessage('Please select your Pokemon');
        setStage(3);
        break;
      case 3:
        //Display team recommendation
        setMessage('team_recommendations');
        setStage(4);
        break;
      default:
        break;
    }
  }

  /*
  stage 0 = [GAME INTENSITY]
  stage 1 = [GENERATION]
  stage 2 = [FORMAT]
  stage 3 = [POKEMON]
  */
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
      {stage === 2 && (
        <div>
          {['OU', 'Ubers', 'UU', 'RU', 'NU', 'PU', 'LC'].map((numeral) => (
            <button key={numeral} onClick={() => handleButtonClick(numeral)}>{numeral}</button>
          ))}
        </div>
      )}
      {stage === 3 &&(
        <div>
        <Select 
          options={data.map((item, index) => ({ label: item, value: index }))}
          styles={{ menu: (provided) => ({ ...provided, width: 300, height: 400 }) }}
          onChange={(selectedOption)=> setPokemon(selectedOption.label)}
        />
        <button onClick={() => handleButtonClick(selectedPokemon)}>Confirm</button>
      </div>
      )}
      <p>Selected Button: {selectedButton}</p>
    </div>
  );
}

export default App;
