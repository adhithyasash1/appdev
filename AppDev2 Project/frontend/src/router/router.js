/* eslint-disable */
import login from "@/components/login";
import register from "@/components/register";
import Home from "@/views/Home.vue";
import Summary from "@/views/Summary.vue";
import newList from "@/components/newList";
import newCard from "@/components/newCard";
import updateList from "@/components/updateList";
import updateCard from "@/components/updateCard";
import transferCards from "@/components/transferCards.vue";
import {createRouter, createWebHashHistory} from "vue-router";


const routes = [
    { path: '/', name: 'login', component: login, props: true },
    { path: '/register', name: 'register', component: register, props: true },
    { path: '/home/:id', name: 'Home', component: Home, props: true },
    { path: '/summary/:id', name: 'Summary', component: Summary, props: true },
    { path: '/home/:id/newList', name: 'newList', component: newList, props: true },
    { path: '/home/:id/list/:list_id/newCard', name: 'newCard', component: newCard, props: true },
    { path: '/home/:id/list/:list_id/updateList', name: 'updateList', component: updateList, props: true },
    { path: '/home/:id/list/:list_id/card/:card_id/updateCard', name: 'updateCard', component: updateCard, props: true },
    { path: '/home/:id/list/:list_id/transferCards', name: 'transferCards', component: transferCards, props: true },
];


export const router = createRouter({
    history: createWebHashHistory(),
    routes
})

