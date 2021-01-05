import React from 'react'
import Enemy from './Enemy'

function Enemies(props){
    const enemies = ['rat', 'slime']
    const enemies_length = enemies.length
    return(
        <div style = {{
            border: '5px solid pink', 
            position: 'relative', 
            float: 'right',
            width: '70%',
            height: '50%'}}>
            {enemies.map((enemy,index) => {
                return <Enemy enemy_name = {enemy} index = {index} length = {enemies_length}/>
            })}
        </div>
    )
}

export default Enemies