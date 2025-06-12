<script setup>
import { user } from "@/composables/useAuth.js";
</script>

<template>
  <div class="landing-page">
    <header>
      <div class="hero-masks">
        <img src="/img/alonso.jpg" alt="Máscaras teatrales">
      </div>
    </header>

    <main class="main-content">
      <section class="lifestyle-gallery">
        <div class="lifestyle-item">
          <img src="/img/alonso.jpg" alt="Hombre de espaldas con camiseta">
        </div>
        <div class="lifestyle-item">
          <img src="/img/alonso.jpg" alt="Hombre sujetando camiseta negra">
        </div>
        <div class="lifestyle-item">
          <img src="/img/alonso.jpg" alt="Hombre con pasamontañas">
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.landing-page {
  background-color: black;
  color: #ffd700;
  font-family: sans-serif;
}

header {
  padding: 20px;
  text-align: center;
}

.nav-links a {
  color: #ffd700;
  text-decoration: none;
  font-weight: bold;
}

.logo img {
  max-width: 150px;
}

.hero-masks {
  margin-bottom: 50px;
}

.hero-masks img {
  width: 100%;
  max-width: 600px; /* Ajusta el tamaño de las máscaras */
  height: auto;
}

.main-content {
  padding: 20px;
}

.lifestyle-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 50px;
}

.lifestyle-item img {
  width: 100%;
  height: auto;
  display: block; /* Para eliminar el espacio extra debajo de la imagen */
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.product-card {
  background-color: #333; /* Un gris oscuro para las tarjetas de producto */
  padding: 10px;
  text-align: center;
}

.product-card img {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
}

.product-info p {
  margin: 5px 0;
  font-size: 0.9em;
}

/* Media Queries para responsividad, si es necesario */
@media (max-width: 768px) {
  .nav {
    flex-direction: column;
    gap: 15px;
  }
  .nav-links {
    margin-top: 10px;
  }
}
</style>