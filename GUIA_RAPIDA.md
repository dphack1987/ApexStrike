# ApexStrike - Guía Rápida de Uso

## 🚀 Inicio Rápido

### Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Dar permisos de ejecución
chmod +x pentest_cli.py
```

## 📚 Comandos Básicos

### 1. Escaneo de Puertos
```bash
# Escaneo básico
./pentest_cli.py -t ejemplo.com portscan

# Escaneo avanzado
./pentest_cli.py -t ejemplo.com portscan --port-start 1 --port-end 65535 --threads 200
```

### 2. Análisis Web
```bash
# Escaneo de vulnerabilidades web
./pentest_cli.py -t http://ejemplo.com webscan --deep

# Pruebas de API
./pentest_cli.py -t http://api.ejemplo.com webscan --mode api
```

### 3. Pruebas IoT
```bash
# Escanear red en busca de dispositivos IoT
./pentest_cli.py -t 192.168.1.0/24 iotscan --network

# Probar dispositivo específico
./pentest_cli.py -t 192.168.1.100 iotscan --protocol mqtt
```

### 4. Análisis de Vulnerabilidades
```bash
# Análisis básico de seguridad
./pentest_cli.py -t ejemplo.com exploit

# Análisis profundo con todas las pruebas
./pentest_cli.py -t ejemplo.com exploit --deep

# Análisis sin pruebas invasivas
./pentest_cli.py -t ejemplo.com exploit --no-dos
```

### 5. Pruebas DoS (Solo Educativo)
```bash
# Prueba SYN flood
./pentest_cli.py -t ejemplo.com dos --method syn --duration 10

# Prueba Slowloris
./pentest_cli.py -t ejemplo.com dos --method slowloris --port 80
```

## 📊 Generación de Reportes

```bash
# Generar reporte en JSON
./pentest_cli.py -t ejemplo.com portscan -o reporte.json
```

## 🔍 Opciones Comunes

### Opciones Generales
- `-t, --target`: IP/dominio objetivo
- `-o, --output`: Archivo de salida para el reporte
- `--deep`: Realizar escaneo profundo
- `-q, --quiet`: Modo silencioso

### Opciones de Escaneo
- `--threads`: Número de hilos para escaneo
- `--port-start`: Puerto inicial
- `--port-end`: Puerto final
- `--timeout`: Tiempo de espera por conexión

### Opciones de Análisis
- `--no-dos`: Excluir pruebas que puedan afectar servicios
- `--protocol`: Protocolo a probar (mqtt, coap, telnet)
- `--mode`: Modo de escaneo (web, api)

### Opciones de Pruebas
- `--duration`: Duración de la prueba
- `--method`: Método de ataque (syn, udp, http, slowloris)

## ⚠️ Advertencias

1. **Uso Legal**: Solo usar en sistemas con autorización explícita.
2. **Privilegios**: Algunas funciones requieren permisos de administrador.
3. **Rendimiento**: El escaneo profundo puede llevar tiempo considerable.
4. **Recursos**: Monitorear el uso de recursos del sistema.
5. **Impacto**: Las pruebas de exploit pueden afectar servicios en producción.
6. **Seguridad**: Mantener los resultados confidenciales y seguros.

## 🆘 Solución de Problemas

### Errores Comunes

1. **Permission Denied**
   ```bash
   sudo ./pentest_cli.py [comandos]
   ```

2. **Puerto en Uso**
   ```bash
   # Verificar puertos en uso
   netstat -tulpn
   ```

3. **Dependencias Faltantes**
   ```bash
   pip install -r requirements.txt
   ```

4. **SSL/TLS Errors**
   ```bash
   # Usar --no-verify para ignorar errores de certificado
   ./pentest_cli.py -t ejemplo.com exploit --no-verify
   ```

5. **Timeouts en Análisis**
   ```bash
   # Aumentar timeout para redes lentas
   ./pentest_cli.py -t ejemplo.com exploit --timeout 30
   ```

### Códigos de Error Comunes

- `E001`: Error de conexión SSL
- `E002`: Timeout en escaneo
- `E003`: Servicio no disponible
- `E004`: Permisos insuficientes
- `E005`: Recurso bloqueado

### Mejores Prácticas

1. **Planificación y Autorización**
   - Obtener autorización por escrito antes de iniciar pruebas
   - Documentar el alcance y limitaciones del análisis
   - Establecer ventanas de tiempo para pruebas invasivas

2. **Metodología de Pruebas**
   - Comenzar con escaneos básicos no intrusivos
   - Incrementar gradualmente la intensidad de las pruebas
   - Usar --no-dos para pruebas en producción
   - Realizar pruebas completas en entornos de staging

3. **Gestión de Recursos**
   - Monitorear el uso de recursos del sistema
   - Limitar el número de hilos en escaneos
   - Establecer timeouts apropiados
   - Pausar entre pruebas intensivas

4. **Documentación y Reportes**
   - Guardar siempre los reportes con -o
   - Documentar hallazgos y pasos de reproducción
   - Mantener registros de todas las pruebas realizadas
   - Incluir evidencias de vulnerabilidades

5. **Seguridad y Confidencialidad**
   - Cifrar los reportes de vulnerabilidades
   - No compartir resultados sin autorización
   - Eliminar datos sensibles después del análisis
   - Reportar vulnerabilidades críticas inmediatamente

## 📋 Ejemplos de Uso Real

### Auditoría de Seguridad Completa
```bash
# 1. Escaneo inicial de puertos
./pentest_cli.py -t objetivo.com portscan --top-ports -o puertos.json

# 2. Análisis de vulnerabilidades web
./pentest_cli.py -t http://objetivo.com webscan --deep -o web.json

# 3. Análisis profundo de vulnerabilidades
./pentest_cli.py -t objetivo.com exploit --deep -o vulns.json

# 4. Pruebas específicas de API
./pentest_cli.py -t http://api.objetivo.com webscan --mode api -o api.json
```

### Análisis IoT Avanzado
```bash
# 1. Descubrir dispositivos
./pentest_cli.py -t 192.168.1.0/24 iotscan --network -o devices.json

# 2. Análisis de vulnerabilidades por dispositivo
./pentest_cli.py -t 192.168.1.100 exploit --deep --no-dos -o iot_vulns.json

# 3. Pruebas específicas de protocolos
./pentest_cli.py -t 192.168.1.100 iotscan --protocol mqtt -o mqtt.json
```

### Análisis de Seguridad SSL/API
```bash
# 1. Verificación SSL/TLS
./pentest_cli.py -t objetivo.com exploit --deep --no-dos -o ssl_report.json

# 2. Pruebas de endpoints API
./pentest_cli.py -t api.objetivo.com webscan --mode api --deep -o api_full.json

# 3. Búsqueda de vulnerabilidades específicas
./pentest_cli.py -t objetivo.com exploit --deep -o security_audit.json
```

## 📊 Interpretación de Resultados

### Niveles de Severidad

- **CRÍTICO** (9.0-10.0)
  - Vulnerabilidades que permiten ejecución remota de código
  - Acceso no autorizado con privilegios elevados
  - Exposición directa de datos sensibles

- **ALTO** (7.0-8.9)
  - Inyecciones SQL sin mitigación
  - Vulnerabilidades de autenticación
  - Configuraciones SSL/TLS inseguras

- **MEDIO** (4.0-6.9)
  - XSS reflejado
  - Headers de seguridad faltantes
  - Exposición de información sensible

- **BAJO** (0.1-3.9)
  - Información de versiones expuesta
  - Cookies sin flags de seguridad
  - Métodos HTTP peligrosos habilitados

### Formato de Reportes

Los reportes JSON incluyen:
```json
{
  "scan_info": {
    "target": "ejemplo.com",
    "timestamp": "2024-01-20T10:00:00Z",
    "modules": ["exploit", "webscan"]
  },
  "vulnerabilities": [
    {
      "type": "SQL_INJECTION",
      "severity": "HIGH",
      "description": "Posible inyección SQL en parámetro 'id'",
      "proof": "Payload: ' OR '1'='1",
      "mitigation": "Implementar prepared statements"
    }
  ],
  "statistics": {
    "total_vulns": 5,
    "by_severity": {
      "CRITICAL": 1,
      "HIGH": 2,
      "MEDIUM": 1,
      "LOW": 1
    }
  }
}
```

## 🔄 Actualizaciones

Para mantener ApexStrike actualizado:

```bash
git pull origin main
pip install -r requirements.txt
```

## 🛡️ Mitigaciones Comunes

1. **SQL Injection**
   - Usar prepared statements
   - Implementar ORM
   - Validar y escapar inputs

2. **XSS**
   - Implementar CSP
   - Sanitizar inputs
   - Usar frameworks seguros

3. **SSL/TLS**
   - Actualizar a TLS 1.3
   - Configurar cipher suites seguros
   - Implementar HSTS

4. **API Security**
   - Implementar rate limiting
   - Usar autenticación fuerte
   - Validar todos los inputs

## 🤖 Automatización y CI/CD

### Escaneo Automatizado

```bash
# Script de escaneo diario
#!/bin/bash
DATE=$(date +%Y%m%d)
TARGETS="targets.txt"
OUTPUT_DIR="reports/$DATE"

mkdir -p $OUTPUT_DIR

while IFS= read -r target; do
    # Escaneo básico de seguridad
    ./pentest_cli.py -t $target exploit --no-dos -o "$OUTPUT_DIR/${target}_basic.json"
    
    # Análisis web si es aplicable
    if [[ $target == *"http"* ]]; then
        ./pentest_cli.py -t $target webscan --deep -o "$OUTPUT_DIR/${target}_web.json"
    fi
done < "$TARGETS"
```

### Integración con CI/CD

```yaml
# Ejemplo de GitHub Actions
name: Security Scan
on:
  schedule:
    - cron: '0 0 * * *'  # Diario
  push:
    branches: [ main ]

jobs:
  security_scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install ApexStrike
        run: |
          pip install -r requirements.txt
      - name: Run Security Scan
        run: |
          ./pentest_cli.py -t ${{ secrets.TARGET }} exploit --no-dos -o scan_results.json
      - name: Check Results
        run: |
          CRITICAL=$(jq '.statistics.by_severity.CRITICAL' scan_results.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "⚠️ Found $CRITICAL critical vulnerabilities!"
            exit 1
          fi
```

### Monitoreo Continuo

1. **Escaneo Programado**
   - Ejecutar escaneos básicos diariamente
   - Análisis profundo semanal
   - Pruebas de API cada 6 horas

2. **Alertas y Notificaciones**
   - Configurar alertas para vulnerabilidades críticas
   - Notificar cambios en la superficie de ataque
   - Reportar nuevos endpoints expuestos

3. **Gestión de Falsos Positivos**
   - Mantener lista de exclusiones
   - Validar hallazgos manualmente
   - Actualizar reglas de detección

## 📞 Soporte

- Reportar bugs: GitHub Issues
- Preguntas: GitHub Discussions
- Documentación: Wiki del proyecto
- Canal Discord: [ApexStrike Community]

---

⚠️ **Recuerda**: Esta herramienta es para uso ético y autorizado únicamente.
