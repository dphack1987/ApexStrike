# 🤝 Contribuir a ApexStrike

¡Gracias por tu interés en contribuir a ApexStrike! Este documento proporciona las pautas y mejores prácticas para contribuir al proyecto.

## 📋 Índice

1. [Código de Conducta](#código-de-conducta)
2. [Proceso de Desarrollo](#proceso-de-desarrollo)
3. [Reportar Bugs](#reportar-bugs)
4. [Sugerir Mejoras](#sugerir-mejoras)
5. [Guía de Estilo](#guía-de-estilo)
6. [Proceso de Pull Request](#proceso-de-pull-request)

## 📜 Código de Conducta

Este proyecto se adhiere a un Código de Conducta que esperamos que todos los participantes respeten. Por favor, lee [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) antes de contribuir.

## 🔄 Proceso de Desarrollo

1. Fork el repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Implementa tus cambios
4. Ejecuta las pruebas
5. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
6. Push a la rama (`git push origin feature/AmazingFeature`)
7. Abre un Pull Request

## 🐛 Reportar Bugs

### Antes de Reportar

- Verifica que el bug no haya sido reportado ya
- Asegúrate de estar usando la última versión
- Comprueba la documentación

### Información a Incluir

```markdown
**Descripción del Bug**
Una descripción clara y concisa del bug.

**Para Reproducir**
Pasos para reproducir el comportamiento:
1. Ejecutar comando '...'
2. Usar parámetro '....'
3. Ver error

**Comportamiento Esperado**
Una descripción clara de lo que esperabas que sucediera.

**Capturas de Pantalla**
Si aplica, añade capturas de pantalla.

**Entorno:**
 - OS: [ej. Ubuntu 20.04]
 - Python Version: [ej. 3.8.5]
 - ApexStrike Version: [ej. 1.0.0]

**Contexto Adicional**
Cualquier otro contexto sobre el problema.
```

## 💡 Sugerir Mejoras

### Formato de Propuesta

```markdown
**Descripción de la Mejora**
Una descripción clara y concisa de la mejora.

**Problema que Resuelve**
Explica qué problema resuelve esta mejora.

**Alternativas Consideradas**
Describe las alternativas que has considerado.

**Recursos Adicionales**
Enlaces, ejemplos o recursos relacionados.
```

## 📝 Guía de Estilo

### Python

- Sigue PEP 8
- Usa type hints
- Documenta todas las funciones y clases
- Mantén las líneas a menos de 100 caracteres
- Usa nombres descriptivos en inglés

### Ejemplo de Código

```python
from typing import List, Optional

def analyze_target(target: str, ports: List[int], timeout: Optional[float] = None) -> dict:
    """
    Analyze a target for vulnerabilities.

    Args:
        target: The target IP or hostname
        ports: List of ports to scan
        timeout: Optional timeout in seconds

    Returns:
        dict: Analysis results
    """
    results = {}
    # Implementation
    return results
```

## 🔄 Proceso de Pull Request

1. **Título Descriptivo**
   - Use formato: `[Tipo]: Descripción corta`
   - Tipos: `Add`, `Fix`, `Update`, `Refactor`, `Docs`

2. **Descripción Detallada**
   ```markdown
   ## Descripción
   Descripción clara de los cambios

   ## Tipo de Cambio
   - [ ] Bug fix
   - [ ] Nueva característica
   - [ ] Breaking change
   - [ ] Documentación

   ## ¿Cómo se ha Probado?
   Describe las pruebas realizadas

   ## Checklist
   - [ ] Pruebas añadidas/actualizadas
   - [ ] Documentación actualizada
   - [ ] Sigue la guía de estilo
   ```

3. **Review Process**
   - Al menos una aprobación requerida
   - Todos los tests deben pasar
   - La documentación debe estar actualizada

## 🧪 Testing

### Ejecutar Tests

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
python -m pytest tests/

# Verificar cobertura
python -m pytest --cov=apexstrike tests/
```

### Escribir Tests

```python
def test_port_scanner():
    """Test port scanner functionality."""
    scanner = PortScanner("localhost")
    results = scanner.scan_ports([80, 443])
    assert isinstance(results, dict)
    assert all(isinstance(port, int) for port in results.keys())
```

## 📚 Recursos Adicionales

- [Documentación de Python](https://docs.python.org/)
- [Guía de Git](https://git-scm.com/book/en/v2)
- [Escribir Buenos Commits](https://chris.beams.io/posts/git-commit/)
- [Semantic Versioning](https://semver.org/)

## ❓ ¿Preguntas?

Si tienes preguntas o necesitas ayuda:
1. Revisa la [documentación](docs/)
2. Abre un issue con la etiqueta "pregunta"
3. Únete a nuestro canal de Discord

---

¡Gracias por contribuir a ApexStrike! 🚀
