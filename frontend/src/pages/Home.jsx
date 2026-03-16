import React, { useState, useEffect } from 'react';
import { Phone, Mail, MapPin, Star, MessageCircle, Wrench, Truck, Settings, CheckCircle, Menu, X } from 'lucide-react';
import '../styles/Home.css';

const Home = () => {
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    mensaje: ''
  });

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Smooth scroll for navigation links
    const handleSmoothScroll = (e) => {
      const href = e.currentTarget.getAttribute('href');
      if (href.startsWith('#')) {
        e.preventDefault();
        const element = document.querySelector(href);
        if (element) {
          const offset = 80; // Header height
          const elementPosition = element.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - offset;
          
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
          setMobileMenuOpen(false);
        }
      }
    };

    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
      link.addEventListener('click', handleSmoothScroll);
    });

    return () => {
      links.forEach(link => {
        link.removeEventListener('click', handleSmoothScroll);
      });
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock form submission
    alert('Gracias por tu mensaje. Te contactaremos pronto.');
    setFormData({ nombre: '', email: '', telefono: '', mensaje: '' });
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const whatsappNumber = '34634919257';
  const phoneNumber = '634919257';

  const services = [
    {
      title: 'Reparación de Motores de Camiones',
      description: 'Especialistas en diagnóstico y reparación completa de motores de camiones de todas las marcas.',
      icon: <Truck size={40} />
    },
    {
      title: 'Maquinaria Pesada',
      description: 'Mantenimiento y reparación de excavadoras, grúas y equipos de construcción.',
      icon: <Settings size={40} />
    },
    {
      title: 'Diagnóstico y Mantenimiento',
      description: 'Diagnóstico electrónico avanzado y mantenimiento preventivo de motores industriales.',
      icon: <Wrench size={40} />
    },
    {
      title: 'Motores Industriales y Marinos',
      description: 'Reparación especializada en motores industriales de alta potencia y algunos motores marinos.',
      icon: <Settings size={40} />
    }
  ];

  return (
    <div className="home-container">
      {/* Header */}
      <header className="dark-header">
        <div className="header-content">
          <div className="logo-section">
            <Truck size={32} className="logo-icon" />
            <h1 className="logo-text">Services Truck</h1>
          </div>
          <nav className={`dark-nav ${mobileMenuOpen ? 'mobile-open' : ''}`}>
            <a href="#inicio" className="dark-nav-link">Inicio</a>
            <a href="#servicios" className="dark-nav-link">Servicios</a>
            <a href="#sobre-nosotros" className="dark-nav-link">Nosotros</a>
            <a href="#contacto" className="dark-nav-link">Contacto</a>
            <a href={`tel:${phoneNumber}`} className="btn-primary mobile-cta">
              <Phone size={20} />
              Llamar Ahora
            </a>
          </nav>
          <a href={`tel:${phoneNumber}`} className="btn-primary header-cta desktop-only">
            <Phone size={20} />
            Llamar Ahora
          </a>
          <button 
            className="mobile-menu-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section id="inicio" className="hero-section">
        <div className="hero-overlay"></div>
        <img 
          src="https://images.unsplash.com/photo-1592838064575-70ed626d3a0e"
          alt="Maquinaria pesada"
          className="hero-image"
        />
        <div className="hero-content">
          <h1 className="hero-title">Especialistas en Motores de Maquinaria Pesada</h1>
          <p className="hero-subtitle">
            Reparación y mantenimiento profesional de camiones, excavadoras, grúas y motores industriales en Almería
          </p>
          <div className="hero-cta-group">
            <a href="#contacto" className="btn-primary btn-large">
              Solicitar Presupuesto
            </a>
            <a href={`tel:${phoneNumber}`} className="btn-secondary btn-large">
              <Phone size={20} />
              634 91 92 57
            </a>
          </div>
          <div className="hero-rating">
            <div className="stars">
              {[...Array(5)].map((_, i) => (
                <Star key={i} size={24} fill="#00FFD1" color="#00FFD1" />
              ))}
            </div>
            <span className="rating-text">5.0 estrellas · Valoración de clientes</span>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="sobre-nosotros" className="about-section">
        <div className="container-content">
          <div className="about-grid">
            <div className="about-text">
              <h2 className="section-title">Sobre Nosotros</h2>
              <p className="about-description">
                En <strong>Services Truck</strong> somos especialistas en la reparación y mantenimiento de motores de maquinaria pesada. 
                Con años de experiencia en el sector, ofrecemos un servicio profesional y atención personalizada para cada cliente.
              </p>
              <p className="about-description">
                Trabajamos con las últimas tecnologías de diagnóstico y contamos con un equipo altamente cualificado 
                para garantizar que tu maquinaria funcione al máximo rendimiento.
              </p>
              <div className="about-features">
                <div className="feature-item">
                  <CheckCircle size={24} className="feature-icon" />
                  <span>Servicio profesional especializado</span>
                </div>
                <div className="feature-item">
                  <CheckCircle size={24} className="feature-icon" />
                  <span>Atención personalizada</span>
                </div>
                <div className="feature-item">
                  <CheckCircle size={24} className="feature-icon" />
                  <span>Tecnología de diagnóstico avanzada</span>
                </div>
                <div className="feature-item">
                  <CheckCircle size={24} className="feature-icon" />
                  <span>Amplia experiencia en el sector</span>
                </div>
              </div>
            </div>
            <div className="about-image-container">
              <img 
                src="https://images.unsplash.com/photo-1501700493788-fa1a4fc9fe62"
                alt="Taller Services Truck"
                className="about-image"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="servicios" className="services-section">
        <div className="container-content">
          <h2 className="section-title centered">Nuestros Servicios</h2>
          <p className="section-subtitle centered">
            Soluciones completas para tu maquinaria pesada
          </p>
          <div className="services-grid">
            {services.map((service, index) => (
              <div key={index} className="service-card">
                <div className="service-icon">{service.icon}</div>
                <h3 className="service-title">{service.title}</h3>
                <p className="service-description">{service.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Reviews Section */}
      <section className="reviews-section">
        <div className="container-content">
          <h2 className="section-title centered">Lo Que Dicen Nuestros Clientes</h2>
          <div className="review-card">
            <div className="review-stars">
              {[...Array(5)].map((_, i) => (
                <Star key={i} size={32} fill="#00FFD1" color="#00FFD1" />
              ))}
            </div>
            <p className="review-text">
              "Excelente servicio, muy profesional todo, mil gracias."
            </p>
            <div className="review-rating">
              <span className="rating-score">5.0</span>
              <span className="rating-label">Valoración en Google</span>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contacto" className="contact-section">
        <div className="container-content">
          <h2 className="section-title centered">Contacto</h2>
          <p className="section-subtitle centered">
            Estamos aquí para ayudarte con tu maquinaria
          </p>
          <div className="contact-grid">
            <div className="contact-info">
              <div className="contact-item">
                <div className="contact-icon">
                  <MapPin size={28} />
                </div>
                <div>
                  <h3 className="contact-label">Dirección</h3>
                  <p className="contact-text">
                    P.º del Limonar, 3, Edificio Neptuno<br />
                    Piso 11D, 04720 Aguadulce<br />
                    Almería, España
                  </p>
                </div>
              </div>
              <div className="contact-item">
                <div className="contact-icon">
                  <Phone size={28} />
                </div>
                <div>
                  <h3 className="contact-label">Teléfono</h3>
                  <a href={`tel:${phoneNumber}`} className="contact-link">
                    634 91 92 57
                  </a>
                </div>
              </div>
              <div className="contact-item">
                <div className="contact-icon">
                  <MessageCircle size={28} />
                </div>
                <div>
                  <h3 className="contact-label">WhatsApp</h3>
                  <a 
                    href={`https://wa.me/${whatsappNumber}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="contact-link"
                  >
                    Enviar mensaje
                  </a>
                </div>
              </div>

              <form className="contact-form" onSubmit={handleSubmit}>
                <input
                  type="text"
                  name="nombre"
                  placeholder="Nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
                <input
                  type="tel"
                  name="telefono"
                  placeholder="Teléfono"
                  value={formData.telefono}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
                <textarea
                  name="mensaje"
                  placeholder="Mensaje"
                  value={formData.mensaje}
                  onChange={handleChange}
                  className="form-textarea"
                  rows="4"
                  required
                ></textarea>
                <button type="submit" className="btn-primary btn-full">
                  Enviar Mensaje
                </button>
              </form>
            </div>

            {/* Google Maps */}
            <div className="map-container">
              <iframe
                title="Ubicación Services Truck"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3177.948066947838!2d-2.587485723901652!3d36.82341467224098!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd7aa6e6e6e6e6e6%3A0x5f5f5f5f5f5f5f5f!2sPaseo%20del%20Limonar%2C%203%2C%2004720%20Aguadulce%2C%20Almer%C3%ADa!5e0!3m2!1ses!2ses!4v1710000000000"
                width="100%"
                height="100%"
                style={{ border: 0, borderRadius: '12px' }}
                allowFullScreen=""
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container-content">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="footer-logo">
                <Truck size={28} className="logo-icon" />
                <span className="logo-text">Services Truck</span>
              </div>
              <p className="footer-text">
                Especialistas en motores de maquinaria pesada
              </p>
            </div>
            <div className="footer-links">
              <h4 className="footer-heading">Enlaces</h4>
              <a href="#inicio" className="footer-link">Inicio</a>
              <a href="#servicios" className="footer-link">Servicios</a>
              <a href="#sobre-nosotros" className="footer-link">Nosotros</a>
              <a href="#contacto" className="footer-link">Contacto</a>
            </div>
            <div className="footer-contact">
              <h4 className="footer-heading">Contacto</h4>
              <p className="footer-text">634 91 92 57</p>
              <p className="footer-text">Aguadulce, Almería</p>
            </div>
          </div>
          <div className="footer-bottom">
            <p className="footer-copyright">
              © 2024 Services Truck. Todos los derechos reservados.
            </p>
          </div>
        </div>
      </footer>

      {/* WhatsApp Floating Button */}
      <a
        href={`https://wa.me/${whatsappNumber}`}
        target="_blank"
        rel="noopener noreferrer"
        className="whatsapp-float"
        aria-label="Contactar por WhatsApp"
      >
        <MessageCircle size={28} />
      </a>
    </div>
  );
};

export default Home;
