# Services Truck - Guía de Instalación en Hostinger

## 📋 Requisitos Previos

1. **Plan de Hostinger**: Necesitas un plan que soporte Node.js y Python
   - VPS Hosting (RECOMENDADO)
   - Cloud Hosting
   - Business Hosting con Node.js

2. **MongoDB**: Base de datos gratuita
   - Crear cuenta en: https://www.mongodb.com/cloud/atlas
   - Plan gratuito (M0) es suficiente

---

## 🚀 Paso 1: Preparar MongoDB (5 minutos)

1. Ve a https://www.mongodb.com/cloud/atlas
2. Crea una cuenta gratuita
3. Crea un nuevo cluster (elige región cercana a España - Europa)
4. Espera 3-5 minutos a que se cree
5. Click en "Connect" → "Connect your application"
6. Copia la URL de conexión (se ve así):
   ```
   mongodb+srv://usuario:<password>@cluster0.xxxxx.mongodb.net/
   ```
7. Reemplaza `<password>` con tu contraseña real
8. Guarda esta URL, la necesitarás después

---

## 🚀 Paso 2: Subir Archivos a Hostinger

### Opción A: Usando File Manager (Más fácil)

1. **Accede a tu panel de Hostinger**
   - Ve a hpanel.hostinger.com
   - Login con tu cuenta

2. **Abre File Manager**
   - En el panel, busca "File Manager"
   - Click para abrir

3. **Sube el archivo ZIP**
   - Click en "Upload" (arriba a la derecha)
   - Selecciona el archivo `services-truck.zip`
   - Espera a que suba (puede tardar 2-5 minutos)

4. **Extrae el ZIP**
   - Click derecho en `services-truck.zip`
   - Selecciona "Extract"
   - Confirma la extracción

### Opción B: Usando FTP (Alternativa)

1. **Descarga FileZilla**: https://filezilla-project.org/
2. **Conéctate vía FTP**:
   - Host: Tu dominio o IP de Hostinger
   - Usuario: Tu usuario FTP (lo ves en hPanel)
   - Contraseña: Tu contraseña FTP
   - Puerto: 21

3. **Sube todos los archivos**:
   - Arrastra las carpetas `frontend` y `backend` al servidor

---

## 🚀 Paso 3: Configurar Variables de Entorno

1. **Busca el archivo** `backend/.env` en File Manager

2. **Edita el archivo** y cambia estas líneas:
   ```env
   MONGO_URL=mongodb+srv://tu-usuario:tu-password@cluster0.xxxxx.mongodb.net/services_truck
   DB_NAME=services_truck
   ```
   - Reemplaza con tu URL de MongoDB del Paso 1

3. **Guarda el archivo**

---

## 🚀 Paso 4: Instalar Dependencias

### Backend (Python)

1. **Abre Terminal SSH en Hostinger**:
   - En hPanel → "Advanced" → "SSH Access"
   - O usa PuTTY en Windows

2. **Navega a la carpeta backend**:
   ```bash
   cd ~/services-truck/backend
   ```

3. **Instala dependencias Python**:
   ```bash
   pip3 install -r requirements.txt
   ```

### Frontend (Node.js)

1. **Navega a la carpeta frontend**:
   ```bash
   cd ~/services-truck/frontend
   ```

2. **Instala dependencias**:
   ```bash
   npm install
   # o si tienes yarn:
   yarn install
   ```

3. **Compila el frontend para producción**:
   ```bash
   npm run build
   # o
   yarn build
   ```

---

## 🚀 Paso 5: Configurar el Dominio

1. **En hPanel de Hostinger**:
   - Ve a "Websites"
   - Selecciona tu dominio

2. **Configura Node.js Application**:
   - Busca "Node.js" en el panel
   - Click en "Create Application"
   - Configuración:
     - Application root: `/services-truck/frontend`
     - Application URL: Tu dominio (ej: servicestrucks.com)
     - Application startup file: `server.js` o `index.js`

3. **Para el Backend (API)**:
   - Crea otra aplicación Node.js/Python
   - Application root: `/services-truck/backend`
   - Application startup: `uvicorn server:app --host 0.0.0.0 --port 8001`

---

## 🚀 Paso 6: Iniciar los Servicios

### Opción 1: Usando PM2 (Recomendado)

```bash
# Instala PM2
npm install -g pm2

# Inicia el backend
cd ~/services-truck/backend
pm2 start "uvicorn server:app --host 0.0.0.0 --port 8001" --name backend

# Sirve el frontend compilado
cd ~/services-truck/frontend
pm2 serve build 3000 --name frontend

# Guarda la configuración
pm2 save
pm2 startup
```

### Opción 2: Usando Screen (Alternativa)

```bash
# Backend
screen -S backend
cd ~/services-truck/backend
uvicorn server:app --host 0.0.0.0 --port 8001
# Presiona Ctrl+A, luego D para salir

# Frontend
screen -S frontend
cd ~/services-truck/frontend/build
python3 -m http.server 3000
# Presiona Ctrl+A, luego D para salir
```

---

## 🚀 Paso 7: Configurar Nginx (Importante)

Necesitas configurar Nginx para que redirija correctamente:

1. **Crea archivo de configuración**:
   ```bash
   sudo nano /etc/nginx/sites-available/servicestrucks
   ```

2. **Agrega esta configuración**:
   ```nginx
   server {
       listen 80;
       server_name tudominio.com www.tudominio.com;

       # Frontend
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }

       # Backend API
       location /api {
           proxy_pass http://localhost:8001;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. **Activa el sitio**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/servicestrucks /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## 🚀 Paso 8: Configurar SSL (HTTPS)

```bash
# Instala Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Genera certificado SSL gratis
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Sigue las instrucciones
```

---

## ✅ Verificación Final

1. **Verifica que todo funcione**:
   - Ve a tu dominio: https://tudominio.com
   - Prueba el botón "Solicitar Presupuesto"
   - Envía un formulario de contacto
   - Verifica WhatsApp

2. **Verifica el backend**:
   - Ve a: https://tudominio.com/api/
   - Deberías ver: `{"message":"Services Truck API - Running","status":"ok"}`

---

## 🆘 Solución de Problemas

### Error: "Cannot connect to MongoDB"
- Verifica que la URL de MongoDB en `.env` sea correcta
- Asegúrate de haber reemplazado `<password>` con tu contraseña real
- Verifica que tu IP esté en la whitelist de MongoDB Atlas

### Error: "502 Bad Gateway"
- Verifica que los servicios estén corriendo: `pm2 list`
- Reinicia los servicios: `pm2 restart all`

### Los formularios no envían datos
- Verifica que el backend esté corriendo en el puerto 8001
- Verifica la configuración de Nginx
- Revisa los logs: `pm2 logs backend`

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `pm2 logs`
2. Verifica el estado: `pm2 status`
3. Contacta soporte de Hostinger si es problema del servidor

---

## 🎉 ¡Listo!

Tu web está online en: **https://tudominio.com**

Todas las funcionalidades están activas:
- ✅ Formulario de contacto
- ✅ Sistema de presupuestos
- ✅ WhatsApp con mensajes pre-escritos
- ✅ Base de datos MongoDB
- ✅ Emails a info@servicestrucks.com
