import React from 'react'

function Display(props){
    return(
        <div onClick={activateLasers}>
            Activate Lasers
        </div>
    )
}

function activateLasers() {
    fetch("http://127.0.0.1:5000/weather_api?location=bevagna%20italy")
    .then(response => response.json())
    .then(data => console.log(data));
  }

export default Display