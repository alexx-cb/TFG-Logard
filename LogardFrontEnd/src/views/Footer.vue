<template>
  <hr class="divider" />
  <footer class="footer">
    <div class="footer-container">
      <div class="logo-section">
        <img src="../../public/img/Logard.png" alt="Logard" class="logo-image" />
      </div>

      <div class="contact-section">
        <div class="contact-info">
          <a class="contact-link">logardinfo@gmail.com</a>
          <a class="contact-link">+34 644 81 90 46</a>
        </div>
        <a href="https://www.instagram.com/logardbrand/" target="_blank" class="social-link" aria-label="Instagram">
          Instagram
        </a>
      </div>

      <div class="links-section">
        <a href="#" class="footer-link">Privacy</a>
        <a href="#" class="footer-link">FAQ</a>
        <a href="#" class="footer-link">Size Guide</a>
        <a href="#" class="footer-link">Terms of Service</a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterComponent'
}
</script>

<style scoped>
.divider{
  border: none;
  border-bottom: 1px solid #ffd700;
  margin: 0;
  width: 100%;
  box-shadow: 0 1px 8px #111a;
}

.footer {
  background-color: #000000;
  color: #ffd700;
  padding: 2rem 2rem 1.5rem;
  margin-top: auto;
  min-height: 120px;
  position: relative;
  overflow: hidden;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Logo Section */
.logo-section {
  display: flex;
  justify-content: center;
}

.logo-image {
  height: 5rem;
  width: auto;
}

.contact-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.contact-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.contact-link {
  color: #ffd700;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 400;
  transition: all 0.3s ease;
}

.contact-link:hover {
  color: #ffed4e;
  text-shadow: 0 0 8px rgba(255, 215, 0, 0.3);
}

.social-link {
  color: #ffd700;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 400;
  transition: all 0.3s ease;
  position: relative;
}

.social-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: linear-gradient(90deg, #ffd700, #ffed4e);
  transition: width 0.3s ease;
}

.social-link:hover {
  color: #ffed4e;
  text-shadow: 0 0 8px rgba(255, 215, 0, 0.3);
}

.social-link:hover::after {
  width: 100%;
}

/* Links Section */
.links-section {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}

.footer-link {
  color: #ffd700;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 400;
  transition: all 0.3s ease;
  position: relative;
  padding: 0.5rem 0;
}

.footer-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background: linear-gradient(90deg, #ffd700, #ffed4e);
  transition: width 0.3s ease;
}

.footer-link:hover {
  color: #ffed4e;
  transform: translateY(-1px);
}

.footer-link:hover::after {
  width: 100%;
}

/* Responsive Design */
@media (max-width: 768px) {
  .footer {
    padding: 1.5rem 1rem 1rem;
  }

  .footer-container {
    gap: 1rem;
  }

  .logo-image {
    height: 1.8rem;
  }

  .contact-link {
    font-size: 0.85rem;
  }

  .social-link {
    font-size: 0.9rem;
  }

  .links-section {
    gap: 1.2rem;
  }

  .footer-link {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .footer {
    padding: 1.2rem 1rem 0.8rem;
  }

  .footer-container {
    gap: 0.8rem;
  }

  .logo-image {
    height: 1.6rem;
  }

  .contact-info {
    gap: 0.3rem;
  }

  .contact-section {
    gap: 0.8rem;
  }

  .links-section {
    flex-direction: column;
    align-items: center;
    gap: 0.8rem;
  }

  .footer-link {
    font-size: 0.85rem;
  }

  .contact-link {
    font-size: 0.8rem;
  }

  .social-link {
    font-size: 0.85rem;
  }
}

@media (min-width: 1024px) {
  .footer-container {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
  }

  .logo-section {
    flex: 1;
    justify-content: flex-start;
  }

  .contact-section {
    flex: 1;
    justify-content: center;
    flex-direction: row;
    gap: 2rem;
  }

  .contact-info {
    align-items: flex-start;
  }

  .links-section {
    flex: 2;
    justify-content: flex-end;
    gap: 2rem;
  }
}

@media (min-width: 1200px) {
  .footer {
    padding: 2.5rem 2rem 2rem;
  }

  .logo-image {
    height: 7rem;
  }

  .links-section {
    gap: 2.5rem;
  }

  .footer-link {
    font-size: 1rem;
  }

  .contact-link {
    font-size: 0.95rem;
  }

  .social-link {
    font-size: 1.05rem;
  }
}
</style>