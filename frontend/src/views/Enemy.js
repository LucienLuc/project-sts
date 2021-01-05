import React from 'react'

import {ItemTypes} from './Constants'
import { useDrop } from 'react-dnd'
import {useState} from 'react'

import {Progress} from 'antd'
import StatusEffect from './StatusEffect'
import NextMove from './NextMove'

function Enemy(props){
    const shift = props.index/props.length * 100
    const center = shift/2

    const MaxHealth = 100
    const [CurrHealth, setCurrHealth] = useState(50)
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
    const [{ isOver }, drop] = useDrop({
        accept: ItemTypes.CARD,
        drop: (item, monitor) => {console.log(monitor.getItem()); return {'hello': 'world'}},
        collect: (monitor) => ({
          isOver: !!monitor.isOver(),
        })
      })

    return(
        <div ref = {drop} style = {{
            border: '5px solid red', 
            position: 'relative', 
            padding:'10px',
            float: 'left',
            height: '100%', 
            width: '25%',
            overflow:'auto'
            }}>
            {/* {props.enemy_name} */}
            <NextMove type = {'attack'} value = {8}/>
            <div className = 'seperator' style = {{height: '15%'}}/>
            <div className = {props.enemy_name} style = {{position: 'relative', marginLeft: 'auto', marginRight: 'auto'}}/>
            <Progress 
                id ='health' 
                strokeColor = 'red' 
                format = {() => `${CurrHealth}`}
                percent = {`${Percentage}`}
                style = {{width: '100%'}}
            />
           {status_effects.map((effect, index) => {
               return <StatusEffect effect = {effect.name} value = {effect.value}></StatusEffect>
           })}
        </div>
    )
}

export default Enemy