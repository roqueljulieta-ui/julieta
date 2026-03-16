# Services Truck - Product Requirements Document

## 📋 Original Problem Statement
Crear una página web elegante, moderna y muy profesional para un taller especializado en mecánica pesada llamado Services Truck. El diseño debe ser dark-theme con colores negro dominante y naranja para CTAs, transmitiendo potencia, profesionalidad y confianza industrial.

## 🏢 Company Information
- **Nombre**: Services Truck
- **Ubicación**: P.º del Limonar, 3, Edificio Neptuno, piso 11D, 04720 Aguadulce, Almería, España
- **Teléfono**: 634 91 92 57
- **WhatsApp**: 634 91 92 57
- **Valoración**: 5.0 estrellas

## 🎯 User Personas
1. **Propietarios de flotas de camiones**: Necesitan mantenimiento regular y reparaciones confiables
2. **Empresas de construcción**: Requieren servicio para excavadoras, grúas y maquinaria pesada
3. **Operadores industriales**: Buscan expertos en motores industriales y algunos motores marinos
4. **Clientes individuales**: Propietarios de camiones que necesitan servicio profesional

## 🎨 Design System
- **Colors**: 
  - Primary: Negro (#000000) - Dominante
  - Accent: Naranja (#FF6B00) - Solo para CTAs
  - Brand: Cyan-Green (#00FFD1) - Detalles y iconos
- **Typography**: Inter font family
- **Buttons**: Sharp corners (border-radius: 0)
- **Theme**: Dark industrial premium

## ✅ Implemented (2024-03-16)

### Frontend Structure
- [x] Fixed dark-theme header with logo, navigation, and CTA button
- [x] Hero section with background image, main title, subtitle, CTAs, and 5-star rating
- [x] About section with company description and key features
- [x] Services section with 4 service cards:
  - Reparación de Motores de Camiones
  - Maquinaria Pesada
  - Diagnóstico y Mantenimiento
  - Motores Industriales y Marinos
- [x] Reviews section displaying 5.0 star rating with customer testimonial
- [x] Contact section with:
  - Contact information (address, phone, WhatsApp)
  - Contact form (nombre, email, teléfono, mensaje)
  - Google Maps integration
- [x] Footer with brand info, navigation links, and contact details
- [x] Floating WhatsApp button
- [x] Smooth scroll navigation
- [x] Fully responsive design (desktop, tablet, mobile)

### Components Created
- `/app/frontend/src/pages/Home.jsx` - Main landing page
- `/app/frontend/src/styles/Home.css` - Complete styling with dark theme

### Design Features
- Dark theme with black background (#000000)
- Orange CTAs for conversion (#FF6B00)
- Sharp-cornered buttons (border-radius: 0)
- High contrast text for readability
- Hover effects and smooth transitions
- Professional industrial look
- Temporary professional images from Unsplash

## 📦 Current Stack
- **Frontend**: React 19, Lucide React icons
- **Styling**: Custom CSS with dark industrial theme
- **Images**: Unsplash temporary placeholders
- **Maps**: Google Maps embedded iframe

## 🔄 Next Action Items

### P0 - Critical (Immediate)
- [ ] User to replace temporary images with actual workshop photos
- [ ] Test all links and buttons functionality
- [ ] Verify Google Maps location accuracy
- [ ] Mobile responsiveness testing on actual devices

### P1 - High Priority
- [ ] Add backend for contact form submission
- [ ] Email notification system for form submissions
- [ ] Add more animations and micro-interactions
- [ ] SEO optimization (meta tags, descriptions)
- [ ] Add mobile hamburger menu for better navigation

### P2 - Nice to Have
- [ ] Gallery section with before/after images
- [ ] Testimonials carousel with multiple reviews
- [ ] Service booking system
- [ ] Multi-language support (Spanish/English)
- [ ] Blog section for maintenance tips
- [ ] Live chat integration

## 🚀 Future Enhancements
- Integration with CRM for lead management
- Online appointment booking system
- Customer portal for service history
- WhatsApp Business API integration
- Analytics and tracking setup

---
**Last Updated**: March 16, 2024
**Status**: Frontend MVP Complete - Ready for content update
