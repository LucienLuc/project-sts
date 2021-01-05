import React, {useState} from 'react'
import axios from 'axios'
import { withRouter } from 'react-router-dom';
import {Menu, Drawer, Button, Form, Input, Alert} from 'antd'
import {UserOutlined} from '@ant-design/icons'
import SubMenu from 'antd/lib/menu/SubMenu'

import {BASE_URL} from './Constants'

function Navbar(props){
    const [loginVisible, setLoginVisible] = useState(false)
    const [auth, setAuth] = useState(false) 
    const [authFail, setAuthFail] = useState(false) 

    function handleShowDrawer() {
        setLoginVisible(true)
    }
    
    function onClose() {
        setLoginVisible(false)
    }

    const onFinish = (values) => {
        const data = {
            username: values.username,
            password: values.password
        }
        axios.post(BASE_URL + '/auth/jwt/create/', data).then(response => {
            setAuthFail(false)
            if (response.status === 200) {
                localStorage.setItem('auth', response.data.access)
                setAuth(true)
                setLoginVisible(false)
            }
        })
        .catch(err => {
            if (err.response.status === 401) {
                console.log('here')
                setAuthFail(true)
            }
        })
        // console.log('Success:', values);
    }

    return(
        <div>
            {/* Menu Bar */}
            <Menu mode='horizontal' theme = 'dark'>
                <Menu.Item style = {{
                    float: 'left',
                    margin: '5px'
                }}>
                Home
                </Menu.Item>

                {auth && <SubMenu icon = {<UserOutlined/>} style= {{
                    float: 'right',
                    margin: '5px'
                }}>
                    <Menu.Item style = {{
                    }}>
                        Profile
                    </Menu.Item>
                    <Menu.Item style = {{
                    }}>
                        Logout
                    </Menu.Item>
                </SubMenu>}
                    {!auth && <Menu.Item ghost = 'true' size = 'large' onClick = {handleShowDrawer} style = {{
                        float: 'right',
                        margin: '5px'
                    }}>Login</Menu.Item>}
            </Menu>

            {/* Login drawer */}
            <Drawer width = {512} title = 'Login' placement = 'right' onClose = {onClose} visible = {loginVisible}
            footer={
                <div
                  style={{
                    textAlign: 'right',
                  }}
                >
                  <Button danger = {true} onClick={onClose} style={{ marginRight: 8 }}>
                    Cancel
                  </Button>
                </div>
              }>
                {authFail && <Alert showIcon type ='error' description = 'Invalid username and password combination.' style = {{margin: '5px'}}/>}
                <Form
                name="basic"
                initialValues={{
                    remember: true,
                }}
                onFinish={onFinish}
                >
                <Form.Item
                    label="Username"
                    name="username"
                    validateStatus = {authFail ? 'error' : 'success'}
                    rules={[
                    { 
                        required: true,
                        message: 'Please input your username!',
                    },
                    ]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    label="Password"
                    name="password"
                    validateStatus = {authFail ? 'error' : 'success'}
                    // help = {authFail ? 'Invalid username and password combination.' : ''}
                    rules={[
                    {
                        required: true,
                        message: 'Please input your password!',
                    },
                    ]}
                >
                    <Input.Password />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit">
                    Login
                    </Button>
                </Form.Item>
                </Form>
            </Drawer>
        </div>
    )
}

export default withRouter(Navbar)