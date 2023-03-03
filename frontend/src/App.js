import React, {useState} from 'react';
import './App.css';

function App() {
  const getMapUrl = 'http://localhost:8000/api/getMapUrl/';

  const [mapUrl, setMapUrl] = useState({url: '', count: 0});
  const [mapUrl2, setMapUrl2] = useState({url: '', count: 0});

  const updateMapUrl = () => {
    fetch(getMapUrl, {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      setMapUrl({url: data['ans'], count: mapUrl.count + 1});
      // console.log(' me ');
    });
  }

  const updateMapUrl2 = () => {
    const arr = document.getElementsByTagName('input');

    fetch(getMapUrl, {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'start': [arr[0].value, arr[1].value],
        'goal': [arr[2].value, arr[3].value]
      })
    })
    .then(response => response.json())
    .then(data => {
      setMapUrl2({url: data['ans'], count: mapUrl.count + 1});
      // console.log(' me ');
    });
  }

  return (
    <div className="App">
      <div>
        <img src={mapUrl.url} alt="Карта"/>
      </div>
      <div>
        <button onClick={updateMapUrl}><h1>Получить/Обновить изоображение карты с аномалиями и детекторами</h1></button>
        <h1>Построить маршрут</h1>

        <h4>Начальная точка</h4>

        <label>x</label>
        <input></input>

        <label>y</label>
        <input></input>

        <h4>Конечная точка</h4>

        <label>x</label>
        <input></input>

        <label>y</label>
        <input></input>

        <button onClick={updateMapUrl2}><h1>Построить</h1></button>
        <div>
          <img src={mapUrl2.url} alt="Карта"/>
        </div>

      </div>
    </div>
  );
}

export default App;
