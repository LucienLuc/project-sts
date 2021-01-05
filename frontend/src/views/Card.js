import React from 'react'

import { DragSource } from 'react-dnd'
import { useDrag } from 'react-dnd'
import {useState} from 'react'

import {ItemTypes} from './Constants'
import './card.css'

function Card(props){
    const shift = props.index/props.length * 100
    const center = shift/2
    const [isHovering, changeHover] = useState(false)

    function handleMouseEnter() {
        changeHover(true)
    }
    function handleMouseLeave() {
        changeHover(false)
    }

    const [{isDragging}, drag] = useDrag({
        item: { type: ItemTypes.CARD, card_name: props.card_name },
        end: (item, monitor) => {
                if (!monitor.didDrop()) {
                    return
                }
                // console.log(item)
                // console.log(monitor.getDropResult())
            },
        collect: monitor => ({
          isDragging: !!monitor.isDragging(),
        }),
      })

    return (
        <div>
             {<img className = 'card' ref = {drag} src = {`/assets/cards/${props.card_name}.png`} 
                onMouseEnter = {handleMouseEnter}
                onMouseLeave = {handleMouseLeave}
                style = {{
                left: `${shift}%`,
                opacity: isDragging ? 0.5 : 1,
                bottom: isHovering ? '50px' : '0px',
                zIndex: isHovering ? 10 : 0,
                // transform: `rotate(20deg)`
            }}/>}
        </div>
    )
}
export default Card
// export default DragSource(Types.CARD, cardSource, collect)(Card)