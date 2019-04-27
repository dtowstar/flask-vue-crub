import Vue from 'vue'
import Router from 'vue-router'
import Ping from '@/components/Ping'
import GUI from '@/components/GUI'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'GUI',
      component: GUI
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    }
  ],
  mode: 'history'
})
