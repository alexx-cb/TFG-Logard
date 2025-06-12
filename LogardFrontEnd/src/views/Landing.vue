<script setup>
</script>

<template>
  <div class="landing-page">
    <header class="hero-section">
      <img src="/img/Hero.png" alt="Imagen principal">
    </header>

    <main class="main-content">
      <section class="gallery-section">
        <div class="gallery-row">
          <img src="/img/1-dual.png" alt="Imagen 1" />
          <img src="/img/2-dual.png" alt="Imagen 2" />
        </div>
        <div class="hero-section bottom-hero">
          <img src="/img/last.png" alt="Imagen final" />
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
  margin: 0;
  padding: 0;
}

.hero-section {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.hero-section img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.main-content {
  padding: 0;
}

.gallery-section {
  margin: 0;
}

.gallery-row {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
}

.gallery-row img {
  width: 50%;
  height: auto;
  display: block;
}

.bottom-hero {
  margin-top: 0;
}
</style>