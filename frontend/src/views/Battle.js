import React from 'react'
import axios from 'axios'

import {useState} from 'react'
import './slime.css'
import './rat.css'
import Enemies from './Enemies'
import Hand from './Hand'
import Player from './Player'

import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

import {Button} from 'antd'

function Battle(props){
    return(
        <DndProvider backend = {HTML5Backend}>
            <div style = {{
                position: 'relative', 
                height: '93vh', 
                border :'5px solid blue'}}>
                <Player/>
                <Enemies/>
                <div style = {{position: 'absolute', border :'5px solid purple', top: '55%', width: '100%'}}>
                    <Button style = {{float: 'left'}}>Mana</Button>
                    <Button style = {{position: 'relative', float: 'right'}}>End Turn</Button>
                </div>
                <Hand/>
            </div>
        </DndProvider>
    )
}

export default Battle