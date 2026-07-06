# RESUMEN RÁPIDO - Hostinger

## ⚡ Pasos Rápidos (Para Expertos)

### 1. MongoDB Atlas
```
1. Crear cluster gratis en mongodb.com/cloud/atlas
2. Copiar URL de conexión
3. Pegar en backend/.env → MONGO_URL=tu-url-aqui
```

### 2. Hostinger
```bash
# Subir ZIP y extraer
# En SSH terminal:

cd ~/services-truck/backend
pip3 install -r requirements.txt

cd ~/services-truck/frontend
npm install && npm run build

# Instalar PM2
npm install -g pm2

# Iniciar servicios
cd ~/services-truck/backend
pm2 start "uvicorn server:app --host 0.0.0.0 --port 8001" --name backend

cd ~/services-truck/frontend
pm2 serve build 3000 --name frontend

pm2 save
pm2 startup
```

### 3. Nginx
```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8001;
    }
}
```

### 4. SSL
```bash
sudo certbot --nginx -d tudominio.com
```

## ✅ Verificar
- https://tudominio.com → Ver web
- https://tudominio.com/api/ → Ver {"status":"ok"}

## 🆘 Problemas?
```bash
pm2 logs        # Ver errores
pm2 restart all # Reiniciar todo
```

---

**Archivo completo:** Lee `INSTRUCCIONES_HOSTINGER.md` para guía detallada paso a paso.
