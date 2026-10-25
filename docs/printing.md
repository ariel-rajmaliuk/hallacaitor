# Impresión y calibración

[Inicio](../README.md) · [BOM y orientaciones](bom.md)

## Referencia inicial, no perfil validado

| Ajuste | Punto de partida |
|---|---|
| Impresora | Cama 220 × 220 mm, altura 250 mm |
| Material estructural | PETG; PLA solo para pruebas geométricas |
| Boquilla / capa | 0,4 / 0,2 mm |
| Perímetros | 4; revisar ejes y chavetas con el laminador |
| Tapas y bases | 5 capas |
| Relleno | 20–30%; ajustar según pieza |
| Aros abiertos | PETG tenaz; revisar la pequeña flexión de montaje |
| Soportes | Revisar en orejas de índice y agujeros horizontales |

Elegir temperaturas y ventilación del fabricante del filamento y del perfil de la impresora. No se suministra G-code: depende de máquina, boquilla, material y laminador. Usar PETG no habilita por sí solo el contacto con alimentos.

## Orden que evita imprimir todo de entrada

1. C01 y C02.
2. Kit mínimo del plegador; prueba sin alimentos.
3. Rodillo y dos aros de 4 mm; comprobar giro y retención.
4. Tabla, dosis de 80 ml y medida de guiso de 60 ml.
5. Organizador y accesorios opcionales.

El conjunto mínimo tiene 14 piezas contando cupones; la cantidad de cada modelo se publica en [parts.json](../config/parts.json). No hace falta imprimir los tres juegos de aros ni los tres dosificadores al principio.

## Orientaciones que importan

- **Alas:** el STL está invertido para apoyar la cara amplia en la cama. Limpiar puentes de los agujeros sin cambiar su posición. No reorientar verticalmente por ahorrar espacio.
- **Ejes largos:** tienen una cara plana para imprimirse tumbados. El eje del rodillo ya está girado 45° en la cama y entra por su proyección diagonal. Usar un brim pequeño de 2 mm y comprobar que la purga/prime line no invada la pieza.
- **Cuerpo de rodillo:** vertical, 200 mm de altura. Brim sugerido 5 mm. Comprobar estabilidad; no lanzar la impresión si el perfil no resuelve esa altura con seguridad.
- **Chavetas:** con cabeza arriba; base pequeña y brim. Limpiar el brim antes de probar. No engrosar para forzarlas dentro del eje.
- **Tapas opcionales:** invertir en el laminador con la cara cerrada sobre la cama. Así no necesitan puentear toda la abertura.
- **Tabla:** plana sobre la cama. Deformación o esquinas levantadas arruinan el espesor repetible del rodillo; medir sobre una mesa plana.

## Ajustes editables

`cad/hallacaitor.scad` expone `clearance` (diámetro), `key_clearance` (por lado), `angle` y `facets`. Los volúmenes y espesores se seleccionan por nombre de pieza. No hay garantía de compatibilidad con v0.1 ni con cualquier escalado global del STL.

```bash
python scripts/export.py --part fold_base --part fold_wing_north --part fold_wing_south --clearance 0.6
```

Reexportar **las dos piezas de un encaje** cuando cambies un parámetro. No escalar un eje para corregir su diámetro: también cambia su longitud y la posición de la chaveta. No escalar todo un dosificador para cambiar capacidad: cambia el encaje del empujador.

## Coste y material

Laminar el kit elegido y tomar los gramos/horas de ese trabajo. El informe de geometría contiene **volumen de sólido CAD**, no gramos de una impresión con relleno. No se publica un costo ni una duración inventada. Registrar filamento, boquilla, orientación y masa estimada en la planilla de ensayo.

## Piezas fuera de tolerancia

No martillar pasadores, doblar brazos para hacer coincidir agujeros ni usar una herramienta como palanca. Una impresión que solo encaja a la fuerza no pasa el criterio inicial. Eliminar rebabas pequeñas, medir y repetir el cupón. Si es necesario agrandar un agujero, documentar cuánto; no asumir que el resto de la máquina conserva su precisión.
