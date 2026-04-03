import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Detect from '@/views/Detect.vue'
import BatchDetect from '@/views/BatchDetect.vue'
import History from '@/views/History.vue'
import Stats from '@/views/Stats.vue'
import Models from '@/views/Models.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/detect',
    name: 'Detect',
    component: Detect
  },
  {
    path: '/batch',
    name: 'BatchDetect',
    component: BatchDetect
  },
  {
    path: '/history',
    name: 'History',
    component: History
  },
  {
    path: '/stats',
    name: 'Stats',
    component: Stats
  },
  {
    path: '/models',
    name: 'Models',
    component: Models
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
