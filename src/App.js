import React, { useEffect, useState } from 'react';
import Select from "react-select";
import './App.css';

var gameIntensity=false;

function App() {
  const [data, setData] = useState([]);
  const [stage, setStage] = useState(0);
  const [message, setMessage] = useState('Please select your game intensity');
  const [selectedButton, setSelectedButton] = useState('');
  const [selectedPokemon, setPokemon] = useState('');
  const [generatedText, setGeneratedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (stage === 2 || (stage===3 && !gameIntensity)) {
      fetch(`http://localhost:5000/get-file-data/${selectedButton}`)
        .then(response => response.json())
        .then(data => setData(data))
        .catch(error => console.error(error));
    }
    else if (stage === 4) {
      setIsLoading(true);
      fetch('http://localhost:5000/generate-pokemon-team', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: selectedPokemon }),
      })
      .then(response => response.json())
      .then(data => {
        setGeneratedText(data.generated_text);
        console.log("Loading done")
        setIsLoading(false);  // Move this line here
      })
      .catch((error) => {
        console.error('Error:', error);
      })
    }
  }, [stage, selectedButton,selectedPokemon]);

  const handleButtonClick = async (buttonLabel) => {  
    setSelectedButton(buttonLabel);
  
    // Send the selected button to the backend and wait for it to complete
    await fetch('http://localhost:5000/add-user-route', {  
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
        if (buttonLabel==="Competitive"){
          gameIntensity=true;
        }
        setMessage('Please select your generation');
        setStage(1);        
        break;
      case 1:
        if(gameIntensity===true){
          setMessage('Please select your Format');
        setStage(2);
        }else{
          //Send a blank string in place of format if casual is selected
          fetch('http://localhost:5000/add-user-route', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_input: ' ' }),
          })
          .then(response => response.json())
          .then(data => console.log(data))
          .catch((error) => console.error('Error:', error));

          //skip format stage
          setStage(3);
        }
                
        break;
      case 2:
        
        setMessage('Please select your Pokemon');
        setStage(3);
        break;
      case 3:
        //Display team recommendation
        setMessage('Team Recommendations');
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
  stage 4 = Display Text
  */
  return (
  <div style={{ textAlign: 'center' }}>
  <h1>{message}</h1>
  {stage === 4 &&(
        <div>
        {isLoading ? <p>Loading...</p> : <pre>{generatedText}</pre>}
      </div>
      )}
   <div class ="pokeball">     
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
      
      <h2>Selected Button: {selectedButton}</h2>
    </div>
   </div>
  );
}

export default App;
