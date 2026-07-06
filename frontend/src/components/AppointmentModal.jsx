import React, { useState } from 'react';
import { Calendar, Clock, Wrench, X, CheckCircle } from 'lucide-react';
import '../styles/AppointmentModal.css';

const AppointmentModal = ({ isOpen, onClose, backendUrl }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    apellidos: '',
    email: '',
    telefono: '',
    fecha_preferida: '',
    hora_preferida: '',
    tipo_servicio: '',
    descripcion: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const servicios = [
    'Reparación de Motores de Camiones',
    'Mantenimiento de Excavadoras',
    'Reparación de Grúas',
    'Motores Industriales',
    'Motores Marinos',
    'Diagnóstico Electrónico',
    'Otro'
  ];

  const horarios = [
    '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch(`${backendUrl}/api/appointments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setSubmitSuccess(true);
        setTimeout(() => {
          onClose();
          setSubmitSuccess(false);
          setFormData({
            nombre: '',
            apellidos: '',
            email: '',
            telefono: '',
            fecha_preferida: '',
            hora_preferida: '',
            tipo_servicio: '',
            descripcion: ''
          });
        }, 3000);
      } else {
        alert('Error al enviar la solicitud. Por favor, inténtalo de nuevo.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error de conexión. Por favor, inténtalo de nuevo.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="appointment-modal-overlay" onClick={onClose}>
      <div className="appointment-modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          <X size={24} />
        </button>

        {submitSuccess ? (
          <div className="success-message">
            <CheckCircle size={64} className="success-icon" />
            <h2>¡Solicitud Enviada!</h2>
            <p>Te contactaremos pronto para confirmar tu cita.</p>
          </div>
        ) : (
          <>
            <div className="modal-header">
              <Calendar size={32} className="modal-icon" />
              <h2>Solicitar Presupuesto</h2>
              <p>Completa el formulario y te contactaremos para confirmar</p>
            </div>

            <form onSubmit={handleSubmit} className="appointment-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Nombre *</label>
                  <input
                    type="text"
                    name="nombre"
                    value={formData.nombre}
                    onChange={handleChange}
                    required
                    placeholder="Tu nombre"
                  />
                </div>
                <div className="form-group">
                  <label>Apellidos *</label>
                  <input
                    type="text"
                    name="apellidos"
                    value={formData.apellidos}
                    onChange={handleChange}
                    required
                    placeholder="Tus apellidos"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="tu@email.com"
                  />
                </div>
                <div className="form-group">
                  <label>Teléfono *</label>
                  <input
                    type="tel"
                    name="telefono"
                    value={formData.telefono}
                    onChange={handleChange}
                    required
                    placeholder="+34 600 00 00 00"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Fecha Preferida *</label>
                  <input
                    type="date"
                    name="fecha_preferida"
                    value={formData.fecha_preferida}
                    onChange={handleChange}
                    required
                    min={new Date().toISOString().split('T')[0]}
                  />
                </div>
                <div className="form-group">
                  <label>Hora Preferida *</label>
                  <select
                    name="hora_preferida"
                    value={formData.hora_preferida}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Seleccionar hora</option>
                    {horarios.map((hora) => (
                      <option key={hora} value={hora}>{hora}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Tipo de Servicio *</label>
                <select
                  name="tipo_servicio"
                  value={formData.tipo_servicio}
                  onChange={handleChange}
                  required
                >
                  <option value="">Seleccionar servicio</option>
                  {servicios.map((servicio) => (
                    <option key={servicio} value={servicio}>{servicio}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Descripción del Problema *</label>
                <textarea
                  name="descripcion"
                  value={formData.descripcion}
                  onChange={handleChange}
                  required
                  rows="4"
                  placeholder="Describe el problema o servicio que necesitas..."
                ></textarea>
              </div>

              <button
                type="submit"
                className="btn-submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Enviando...' : 'Enviar Solicitud'}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};

export default AppointmentModal;
