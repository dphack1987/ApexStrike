# 🛡️ ApexStrike

Framework avanzado de pruebas de penetración y análisis de seguridad.

## 🚀 Características

- **Escaneo de Puertos**: Detección avanzada de servicios y vulnerabilidades
- **Análisis Web**: Pruebas de seguridad web y API
- **Seguridad IoT**: Análisis de dispositivos y redes IoT
- **Motor de Exploits**: Detección y verificación de vulnerabilidades
- **Pruebas DoS**: Análisis de resistencia (solo educativo)
- **Automatización**: Integración con CI/CD y escaneo continuo

## 📋 Requisitos

- Python 3.8+
- pip
- Privilegios de administrador (para algunas funciones)

## 🔧 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/dphack1987/ApexStrike.git
cd ApexStrike

# Instalar dependencias
pip install -r requirements.txt

# Dar permisos de ejecución
chmod +x pentest_cli.py
```

## 💡 Uso Básico

```bash
# Escaneo de puertos
./pentest_cli.py -t ejemplo.com portscan

# Análisis web
./pentest_cli.py -t http://ejemplo.com webscan --deep

# Análisis de vulnerabilidades
./pentest_cli.py -t ejemplo.com exploit --deep

# Escaneo IoT
./pentest_cli.py -t 192.168.1.0/24 iotscan --network
```

## 📊 Módulos Disponibles

### 1. Escaneo de Puertos (portscan)
- Detección de servicios
- Fingerprinting de versiones
- Escaneo de puertos comunes
- Análisis de banners

### 2. Análisis Web (webscan)
- Detección de vulnerabilidades web
- Pruebas de API REST
- Análisis de headers de seguridad
- Identificación de tecnologías

### 3. Seguridad IoT (iotscan)
- Descubrimiento de dispositivos
- Análisis de protocolos IoT
- Pruebas de seguridad específicas
- Detección de configuraciones por defecto

### 4. Motor de Exploits (exploit)
- Análisis SSL/TLS
- Detección de inyecciones
- Pruebas de autenticación
- Verificación de configuraciones

### 5. Pruebas DoS (dos)
- Análisis de resistencia
- Pruebas de carga
- Simulación de ataques
- Medición de impacto

## 🔄 Flujo de Trabajo Recomendado

1. **Reconocimiento Inicial**
   ```bash
   ./pentest_cli.py -t objetivo.com portscan --top-ports
   ```

2. **Análisis de Servicios**
   ```bash
   ./pentest_cli.py -t objetivo.com webscan --deep
   ```

3. **Búsqueda de Vulnerabilidades**
   ```bash
   ./pentest_cli.py -t objetivo.com exploit --deep
   ```

4. **Generación de Reportes**
   ```bash
   ./pentest_cli.py -t objetivo.com exploit -o reporte_final.json
   ```

## 📚 Documentación

Para instrucciones detalladas, consulta:
- [Guía Rápida](GUIA_RAPIDA.md)
- [Contribuir](CONTRIBUTING.md)
- [Licencia](LICENSE.md)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE.md](LICENSE.md) para detalles.

## ⚠️ Aviso Legal

Esta herramienta está diseñada para pruebas de seguridad autorizadas y éticas. El uso indebido de esta herramienta puede resultar en acciones legales. Los autores no se hacen responsables del mal uso o daños causados por esta herramienta.

## 🌟 Créditos

Desarrollado por el equipo CyberHunters.

---

Made with ❤️ by Security Researchers for Security Researchers
