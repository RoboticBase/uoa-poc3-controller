import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Stocks from '@/views/Stocks.vue'

Vue.use(VueRouter)
Vue.use(BootstrapVue)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    redirect: '/stocks'
  },
  {
    path: '/stocks',
    name: 'stocks',
    component: Stocks
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
