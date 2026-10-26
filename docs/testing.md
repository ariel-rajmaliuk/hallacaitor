# Validación y plan de ensayo

[Inicio](../README.md) · [Diseño](design.md) · [Resultados digitales](validation)

## Estado honesto

| Nivel | Estado | Evidencia |
|---|---|---|
| CAD exportable | Comprobado para parámetros por defecto | [Informe de geometría](validation/geometry.json) |
| Mallas | Comprobación automática por pieza | Un componente, volumen positivo, bordes cerrados/orientados, sin triángulos degenerados |
| Cama | Comprobada por envolvente de cada STL orientado | 220 × 220 × 250 mm, sin contar brim ni área de purga |
| Movimiento plástico-plástico | Muestreado digitalmente | [Intersecciones CGAL](validation/motion.json) |
| Pasos de aguja | Comprobación geométrica sin cuerda ni hoja | Misma fuente CAD, agujeros y huecos de bisagra |
| Ajuste y giro reales | **Pendiente** | Cupón, luego impresión de ejes |
| Resistencia y estabilidad | **Pendiente** | No hay FEA ni prueba de carga |
| Cierre con hoja / barreras | **Pendiente** | Necesita hojas reales y comprobación de roturas |
| Comportamiento durante cocción | **Pendiente** | Prueba del paquete, sin piezas impresas en la olla |
| Velocidad y ergonomía | **Pendiente** | Comparación con armado habitual |
| Aptitud alimentaria / comercial | **No validada** | El proyecto no constituye certificación |

## Qué hace el control digital

`validate.py` lee STL binario o ASCII, une vértices a 0,0001 mm y verifica aristas, orientación, componentes, volumen, envolvente y altura inicial. Guarda hashes SHA-256 del CAD, manifiesto y piezas. La revisión de enlaces comprueba destinos locales Markdown, no la disponibilidad de cada página externa.

`check_motion.py` calcula la intersección del sólido de la base con un ala a **0,10,30,50,70,90,100°**, y también entre las dos alas a esos ángulos. La configuración es simétrica; los dos ángulos se muestrean iguales. No es una demostración de todo el espacio de movimientos independientes ni de la trayectoria continua. Además comprueba la aguja en las seis posiciones, con alas a 0°, y los aros del rodillo contra su cuerpo. En los aros se espera una pequeña intersección por la interferencia diametral intencional de 0,2 mm: se mide y limita su volumen, no se declara libre de contacto. La deformación de montaje del aro abierto sigue sin simularse. No simula deformación, hoja, pabilo ni fuerza humana.

`tests/test_design.py` verifica combinaciones de dosis/espesor, cálculo de cuerda, canales dentro del paquete y en huecos de bisagra, manifiesto e inputs inválidos. Un control automático pasado no significa que una persona pueda usar la máquina con éxito.

## Extensión Familiar 0.3

Las muestras nuevas comprueban base/alas a 0/30/70/100°, copa/soportes y copa/eje a 0/45/90/135°, acople de camisas, solape de eje, adaptadores y abrazaderas. La aguja del Familiar y el apilado tienen comprobaciones propias. Las caras de apoyo con espesor y volumen exactamente nulos se registran como contacto plano intencional, no como choque. Consultar los pares y ángulos exactos en el JSON; no confundir esta lista con cobertura de todas las combinaciones.

El constructor del sitio verifica los destinos locales de todas las páginas y que cada pieza tenga ficha, imagen y STL. La revisión de interfaz cubre búsqueda, filtro, calculadora, lectura de una ficha y lista de lectura. No demuestra compatibilidad con todos los navegadores o impresoras.

## Protocolo de banco

| Etapa | Muestra | Aceptación inicial propuesta |
|---|---|---|
| A - Encaje | Cupones y un segmento de eje por diámetro | Entra sin golpe, gira sin atasco y no requiere flexionar la pieza receptora |
| B - Movimiento | 20 ciclos sin hoja ni carga | Sin choque, grieta, roce creciente ni salida de chaveta; pasadores entran libres |
| C - Atado simulado | 10 paquetes de papel de 160×90×35 mm | Seis vueltas, salida por arriba de canales y nudo que no se deshace al manipular |
| D - Hoja | 10 envoltorios sin comida | Cierre con margen, sin roturas causadas por la herramienta |
| E - Masa | 10 porciones con barrera íntegra | Registrar peso, diámetro y espesor; objetivo exploratorio Familiar 2,5±0,5 mm |
| F - Hallaca | 10 paquetes completos, luego cocción externa | Registrar pérdidas, roturas y estado del nudo; no consumir si falló el procedimiento alimentario |
| G - Tiempo | 10 armados usuales y 10 asistidos, misma persona | Registrar tiempos por etapa y mediana; no exigir ventaja antes de medir |

No se establece una carga segura en newtons ni un ritmo de producción. Si el método habitual es más rápido, registrar qué módulo entorpece y usar solo los módulos que ayuden. Un resultado negativo también mejora el diseño.

## Registrar una prueba

Copiar [bench_log.csv](../examples/bench_log.csv), completar impresora, material, perfil, versión y ajustes. **La planilla está vacía a propósito:** el repositorio no contiene datos de ensayos físicos inventados. Agregar fotos con escala y abrir una incidencia mediante [Contribuir](../CONTRIBUTING.md).

Después de modificar bisagras, índices, aguja o canales, repetir comprobaciones y etapas A–D. Después de cambiar material o barrera, repetir desde los cupones correspondientes y las pruebas alimentarias necesarias.

## Ensayos específicos pendientes de 0.3

- Medir flexión del eje partido y escalón de camisas con cargas crecientes, registrando fuerza/desplazamiento; definir límite solo después de medir.
- Volcador: vacío, simulante ligero y porción real; verificar vuelco, desplazamiento del pie, pérdida de chaveta y desprendimiento de forro/pinzas.
- Dock: asentamiento y levantamiento accidental durante cada tarea. La unión actual es por gravedad.
- Guardado: dos niveles, cuatro postes, módulos descargados y alas retiradas; comprobar interferencias y estabilidad. No es prueba de torre operativa.
- Equipo: comparar transferencias de hoja cargada frente a mesa única y contabilizar roturas, retrabajos y limpieza además del tiempo.
