import { createRouter, createWebHistory } from 'vue-router'

import Home from '../features/Home/Home.vue'
import Login from '../features/Login/Login.vue'
import Registration from '../features/Registration/Registration.vue'
import Chat from '../features/Chat/Chat.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Home,
        },
        {
            path: '/login',
            component: Login,
        },
        {
            path: '/registration',
            component: Registration, 
        },
        {
            path: '/chat',
            component: Chat,
        },
    ]
})


export default router;