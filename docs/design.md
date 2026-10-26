# Diseño Familiar 0.3

[Investigación y correcciones](research.md) · [Configuraciones](configurations.md) · [Geometría Compact heredada](compact-design.md)

## Dos configuraciones, una interfaz

Mesa única: 800 × 400 mm, ocho Dock200, cuatro tapas lisas, dos bandejas de ingredientes y un plegador que también permite atar. El octavo puesto queda para hojas y útiles sin adaptador. Equipo: nueve bases, cuatro de ellas juntas para hoja/masa y cinco repartidas para guiso, banco de adornos, volcador, plegado y atado. Ninguna promete movimiento automático ni ausencia de traslados.

## Cotas de interfaz

| Par | Macho | Hembra | Condición |
|---|---:|---:|---|
| Tetón / Dock | Ø8 × 4,4 | Ø8,6 × 5 | 0,6 mm diametral, gravedad |
| Poste / alojamiento | Ø12 × 4 | Ø12,6 × 4,5 inferior o 5 superior | almacenamiento descargado |
| Acople de camisas | Ø29,4, plano x=11 | Ø30, plano x=11,6 | entrada 24 mm |
| Eje / tambor | Ø12 | Ø12,5 | giro con holgura |
| Solape del eje partido | 24 mm | planos separados 0,3 mm | pasador Ø4 en Ø4,4 |
| Aro / asiento | Ø39,2 interior | Ø39,4 de asiento | interferencia 0,2 mm intencional |

Dock: placa 200 × 200 × 8 sobre patas de 8. Adaptador: placa de 4 con cuatro tetones sobre cuadrícula de 100. No hay retención contra levantamiento. Llaves de borde 7,8 mm en placa de 8. No compatible declarado con estándares de terceros.

Poste: 104 mm total = 4 + 96 + 4. Apoya entre cara superior inferior y patas superiores, por lo que el espacio libre es 96 mm y dos baldosas equivalentes se desplazan 112 mm (96 + 16). Usar solo dos niveles; sacar alas, rodillo, volcador y piezas que invadan postes o techo. No hay validación de vuelco.

Familiar: base central 190 × 100, eje de alas y=±64. Se reutilizan alas y ejes Compact, en nueva separación. Paquete supuesto 160 × 90 × 35, sujeto a receta. La envolvente de la base con orejas es mayor que el apoyo central; consultar informe del STL. Las alas abiertas sobresalen de un Dock; dejar perímetro libre.

Rodillo: cuerpo 280, 266 útiles entre límites de ranuras, dos mitades de 140 con acople D. Eje completo 344 mediante solape de 24 entre dos tramos de 184. El pasador del solape se encierra bajo el cuerpo. Es una hipótesis mecánica pendiente de medir flexión y escalón bajo carga, no un eje validado.

Volcador: una porción precargada. Pivote y=-8, z=104 sobre referencia del adaptador. La copa queda por delante y el eje detrás de la cavidad alimentaria; dos soportes con pies y abrazaderas. No tiene tolva, conteo, temporización ni resorte. Muestreo de giro no simula comida ni estabilidad.

La cabeza de H04 mide 3,2 × 6 mm: su ancho axial reducido deja 0,7 mm respecto de la arandela final en ambos rodillos. Se conserva el vástago y su encastre; la retención real se debe ensayar.

## Cálculos

Disco ideal: `D = sqrt(4000 V / (pi t))`; 80/100 ml a 2,5 mm → 202/226 mm. No hay equivalencia universal ml/g. Con forro arrugado o masa no uniforme cambia el resultado.

Pabilo: `L = n*2*(l+h) + n*2*(w+h) + reserva`. Supuesto 160 × 90 × 35, n=3, reserva=300 → 2.220 mm. Probar 2,4 m y medir sobrante. La reserva no modela todas las diagonales ni cruces.

## Lo que la simulación no demuestra

Se comprueban mallas, envolventes, muestras de intersección y enlaces del sitio. El contacto plano de apoyo puede exportar una superficie de espesor cero: se registra como contacto, no como volumen de colisión. La pequeña interferencia de aros se trata por separado. No se prueba elasticidad, desgaste, carga admisible, limpieza, estanqueidad, rendimiento ni facilidad de uso. Ver [ensayos](testing.md).
