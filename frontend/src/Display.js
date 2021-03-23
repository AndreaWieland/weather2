import React from 'react';

function Display(props){
    
    const weekdays = [ 
        'Monday',
        'Tuesday',
        'Wednesday', 
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
    ];
    

    const forecasts = props.data.forecasts.slice(0,5).map(f =>{
        let id=Math.random(); //react requires an id for mapping, i do not
        
        //importing images from local file
        const images = require.context('./images', true);
        //mapping the many different condition ids offered by the api to my limited representative images. images have naming convention images/[condition_id].png
        let cond_id = 800;
        if(f.condition_id > 800){
            cond_id = 803;
        }else if(f.condition_id < 800){
            cond_id = Math.floor(f.condition_id / 100) *100
        }
        let alt = 'Illustration of ' + f.conditions + ' conditions';
        let image = images('./' + cond_id + '.svg');
        let precip = Math.round(f.chance_of_precip * 100);
        return (
            <div className='forecast'
                key={id}>
                <h1>{weekdays[f.day]}</h1>
                <div className='forecast_content'>
                    <div className='top'>
                        <div className='condition_display'>
                            <img alt={alt} src={image}></img>
                            <p>{f.conditions}</p>
                        </div>
                        <div className='hilo'>
                            <p><span className='minor'>High</span>  {f.high_far}°</p>
                            <p><span className='minor'>Low</span>  {f.low_far}°</p>
                        </div>
                    </div>
                    <div className='bottom'>
                        <div className='stat'>
                            <p>Humidity:</p> 
                            <p>{f.humidity}%</p>
                        </div>
                        <div className='stat'>
                            <p>Precipitation:</p> 
                            <p>{precip}%</p>
                        </div>
                        <div className='stat'>
                            <p>Wind :</p> 
                            <p>{f.wind_imperial}mph</p>
                        </div>
                    </div>
                </div>
            </div>
        )
    });


    return (
        <div className='display'>
            <section id='current_conditions'
                className='current'>
                <h1>{props.data.current.fahrenheit_temp}°</h1>
                <h3>{props.data.current.conditions}</h3>
                <h3>Humidity: {props.data.current.humidity}%</h3>
                <h3>Wind: {props.data.current.wind_imperial}mph</h3>
            </section>
            <section className='forecasts'>
                {forecasts}
            </section>
        </div>
    );
}

export default Display