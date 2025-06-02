import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import {initAuth} from "@/composables/useAuth.js";

async function bootstrapApp() {
  await initAuth() // ✅ Espera a que se sepa si el usuario está autenticado o no

  const app = createApp(App)
  app.use(router)
  app.mount('#app')
}

bootstrapApp()