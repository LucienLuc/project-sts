import React from 'react'

import {Badge} from 'antd'

function NextMove(props){
    return(
        <div style = {{position: 'relative', marginLeft: 'auto', marginRight: 'auto', width: '32px'}}>
            <Badge count = {props.value}  offset = {[-26,26]} 
                style = {{
                    backgroundColor: '#fff',
                    color: '#999',
                    boxShadow: '0 0 0 1px #d9d9d9 inset'
                }}>
                <img src = {`/assets/moves/${props.type}.png`}></img>
            </Badge>
        </div>
    )
}

export default NextMove