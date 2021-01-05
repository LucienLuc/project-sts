import React from 'react'
import {useState} from 'react'

import axios from 'axios'

import {Progress} from 'antd'
import StatusEffect from './StatusEffect'

function Player(props){
    const MaxHealth = 100
    const [CurrHealth, setCurrHealth] = useState(70)
    const [Percentage, setPercentage] = useState(100)

    const status_effects = [
        {
            'name': 'strength',
            'value': '1'
        },
        {
            'name': 'strength',
            'value': '3'
        }

    ]

    return(
        <div style = {{
            border :'5px solid brown', 
            position: 'absolute', 
            padding:'10px',
            float: 'left',
            height: '50%',
            width: '20%',
            left: '10%'}}>  
            <Progress 
                id ='health' 
                strokeColor = 'red' 
                format = {() => `${CurrHealth}/${MaxHealth}`}
                percent = {`${Percentage}`}
                // style = {{width: '100%'}}
            />
           {status_effects.map((effect, index) => {
               return <StatusEffect effect = {effect.name} value = {effect.value}></StatusEffect>
           })}
        </div>
    )
}

export default Player