import React from 'react'

import {useState} from 'react'
import {Badge} from 'antd'

function StatusEffect(props){

    return(
        <div style = {{float: 'left'}}>
            <Badge count = {props.value} size = 'small' offset = {[-8,24]}>
                <img src = {`/assets/status_effects/${props.effect}.png`} style = {{height: 'auto', width: '80%'}}></img>
            </Badge>
        </div>
    )
}

export default StatusEffect