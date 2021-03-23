import React from 'react'

class Input extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
          value: '',
        };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleKeyPress = this.handleKeyPress.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
        this.setState({value: event.target.value});
    }

    componentDidMount(){
      document.addEventListener("keydown", this.handleKeyPress);
    }

    handleKeyPress(event){
      let inp = document.getElementById('location_input');
      if (event.keyCode === 13 && this.state.value !== '' && document.activeElement === inp){
        this.handleSubmit();
      }
    }

    handleSubmit(){
      if (this.state.value !== ''){
        this.props.submitLocation(this.state.value);
      }
    }

    render() {
      let cssClass = 'input_holder ' + this.props.css_class;
      return (
        <div className={cssClass}>
            <input 
                id='location_input'
                className='location_input'
                placeholder="Enter your address"
                value={this.state.value}
                onChange={this.handleChange}> 
            </input>
            <div onClick={this.handleSubmit}>
            <i className='fas fa-search search-button'></i>
              </div>
            
        </div>
        
      );
    }
  }

export default Input