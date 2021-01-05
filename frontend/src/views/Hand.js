import React from 'react'

import Card from './Card'

function Hand(props){
    const cards = ['strike', 'block', 'strike', 'block', 'strike', 'block']
    const cards_length = cards.length
    return(
        <div style = {{
            border :'5px solid green',
            width: '80%',
            left: '10%',
            right: '10%',
            position: 'absolute',
            bottom: '0px'
        }}>
            {cards.map((card, index) => {
                return <Card card_name = {card} index = {index} length = {cards_length}/>
            })}
        </div>
    )
}

export default Hand