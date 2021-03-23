import React from 'react';
import Input from './Input.js'
import Display from './Display.js'
import './App.css';

class App extends React.Component {

  constructor(){
    super();
    this.state = {
      apidata:'',
      fetch_error: false
    }
    this.submitLocation = this.submitLocation.bind(this);
  }

  submitLocation(loc){
    let q = "http://www.andrealand.cis.cabrillo.edu/api?location=" + encodeURI(loc);
    fetch(q)
      .then(response => response.json())
      .then(data => this.setState({apidata: data}));
    console.log(this.state.apidata)
  }
  

  render(){
    //case: on page load, no weather data yet
    if (this.state.apidata === ''){
      return (
        <main className="App">
          <div className='welcome'>
            <h1>Welcome!</h1>
            <h2>Please enter your location.</h2>
            {/*<h5>(Or allow the browser to detect your location.)</h5>*/}
            <Input 
              css_class='center'
              submitLocation={this.submitLocation}/>
          </div>
        </main>
      );
    } 
    //case: backend returns error due to invalid location (or services down, to be built)
    else if (this.state.apidata !== '' && this.state.apidata.hasOwnProperty('status')){
      return(   
        <main className="App">
          <div className='data_error'>
            <h1>Uh-oh!</h1>
            <h2>It looks like we couldn't find that location. Please try another.</h2>
            <Input 
              css_class='center'
              submitLocation={this.submitLocation}/>
          </div>
        </main>
      )
    }
    //case: valid json data returned (future fix will be that valid responses have status too)
    else if (this.state.apidata !== '' && !this.state.apidata.hasOwnProperty('status')) {
      console.log(this.state.apidata)
      return (
        <div className="App">
            <Input 
              css_class='corner'
              submitLocation={this.submitLocation}/>
            <Display data={this.state.apidata} />
          </div>
      );
    }
    else{
      return(
        <div className="App">
            <h1>Big error. Please reload page.</h1>
        </div>
      )
    }
    
  }
  
}

export default App;

