import React, { useState } from "react";
import keys from "./keys";

const api = {
  base: keys.BASE_URL,
};

function App() {
  const [query, setQuery] = useState("");
  const [forecast, setForecast] = useState({});
  async function search(e) {
    if (e.key === "Enter") {
      let response = await fetch(`${api.base}`, {
        method: 'post',
        body: JSON.stringify({
          zone_name: query
        }),
        headers: {
          'Content-Type':'application/json',
          'Origin': 'http://smartweather.info'
        },
        mode: 'no-cors'
      });
      let json_resp = await response.json()
      if (response.ok) {
        setQuery("");
        setForecast(json_resp);
        console.log(json_resp);
      } else {
        alert(json_resp.message);
      }
    }
  };

  return (
    <div
      className={
        typeof forecast.weather != "undefined"
          ? forecast.weather.current_temp > 18
            ? "App hot"
            : "App cold"
          : "App"
      }
    >
      <main>
      <div className="service-header">
        <h1>Smart Weather Forecast</h1>
      </div>
        <div className="search-container">
          <label>
            Enter Zone Name:
            <input
              type="text"
              placeholder="Zone name"
              className="search-bar"
              onChange={(e) => setQuery(e.target.value)}
              value={query}
              onKeyPress={search}
            />
          </label>
        </div>
        {typeof forecast.weather != "undefined" ? (
          <div>
            <div className="weather-container">
              <div className="temperature">
                {Math.round(forecast.weather.current_temp)}°C
              </div>
              <div className="weather"><h1>{forecast.clothing_recommendations}</h1> </div>
            </div>
          </div>
        ) : (
          ""
        )}
      </main>
    </div>
  );
}

export default App;
