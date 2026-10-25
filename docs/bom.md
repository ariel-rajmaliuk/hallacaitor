# Lista de piezas y kits

[Inicio](../README.md) · [Montaje](assembly.md) · [CSV](bom.csv)

Todas las cotas son envolventes del STL en su orientación suministrada, en mm. No son medidas de encaje. El laminador debe centrar cada pieza; algunas llevan traslación de CAD.

- **Mínimo: 14 piezas.** Plegado, atado simulado, pala y cupones; incluye una chaveta de repuesto.
- **Estándar: 45 piezas.** Agrega tabla, rodillo con aros de 4 mm, dosis de 80 ml, medida de guiso de 60 ml y organizador.
- **Completo: 62 piezas.** Suma otros espesores/dosis, tapas, bandeja y accesorios; cinco chavetas en total (tres instaladas y dos repuestos).

| SKU | Archivo STL | Mín. | Est. | Comp. | X × Y × Z (mm) |
|---|---|---:|---:|---:|---|
| H01 | [fold_base](../stl/fold_base.stl) | 1 | 1 | 1 | 200 × 164 × 37.6658 |
| H02N | [fold_wing_north](../stl/fold_wing_north.stl) | 1 | 1 | 1 | 194.7 × 137 × 20 |
| H02S | [fold_wing_south](../stl/fold_wing_south.stl) | 1 | 1 | 1 | 194.7 × 137 × 20 |
| H03 | [hinge_axle](../stl/hinge_axle.stl) | 2 | 2 | 2 | 212 × 12 × 9.2 |
| H04 | [lock_key](../stl/lock_key.stl) | 3 | 3 | 5 | 6 × 6 × 14 |
| H05 | [index_pin](../stl/index_pin.stl) | 2 | 2 | 2 | 7 × 7 × 15 |
| R01 | [roller_body](../stl/roller_body.stl) | 0 | 1 | 1 | 40 × 40 × 200 |
| R02 | [roller_axle](../stl/roller_axle.stl) | 0 | 1 | 1 | 197.99 × 197.99 × 15.2 |
| R03 | [roller_grip](../stl/roller_grip.stl) | 0 | 2 | 2 | 29 × 29 × 24 |
| R04 | [roller_washer](../stl/roller_washer.stl) | 0 | 1 | 1 | 21 × 21 × 2 |
| R05A | [ring_3mm](../stl/ring_3mm.stl) | 0 | 0 | 2 | 46 × 45.9017 × 5.6 |
| R05B | [ring_4mm](../stl/ring_4mm.stl) | 0 | 2 | 2 | 48 × 47.9017 × 5.6 |
| R05C | [ring_5mm](../stl/ring_5mm.stl) | 0 | 0 | 2 | 50 × 49.9017 × 5.6 |
| B01 | [board_tile](../stl/board_tile.stl) | 0 | 4 | 4 | 180 × 180 × 6 |
| B02 | [board_key](../stl/board_key.stl) | 0 | 8 | 8 | 24 × 14 × 5.8 |
| D01A | [dose_60ml](../stl/dose_60ml.stl) | 0 | 0 | 1 | 88 × 68 × 21.2207 |
| D01B | [dose_80ml](../stl/dose_80ml.stl) | 0 | 1 | 1 | 88 × 68 × 28.2942 |
| D01C | [dose_100ml](../stl/dose_100ml.stl) | 0 | 0 | 1 | 88 × 68 × 35.3678 |
| D02 | [dose_plunger](../stl/dose_plunger.stl) | 0 | 1 | 1 | 59 × 59 × 42 |
| G01A | [guiso_40ml](../stl/guiso_40ml.stl) | 0 | 0 | 1 | 95 × 58 × 23.3718 |
| G01B | [guiso_60ml](../stl/guiso_60ml.stl) | 0 | 1 | 1 | 95 × 58 × 33.5577 |
| O01 | [ingredient_caddy](../stl/ingredient_caddy.stl) | 0 | 1 | 1 | 194 × 128 × 8 |
| O02 | [ingredient_cup](../stl/ingredient_cup.stl) | 0 | 6 | 6 | 56 × 56 × 44 |
| O03 | [ingredient_lid](../stl/ingredient_lid.stl) | 0 | 0 | 6 | 60 × 60 × 5 |
| M01 | [knead_tray](../stl/knead_tray.stl) | 0 | 0 | 1 | 194 × 174 × 50 |
| T01 | [thread_needle](../stl/thread_needle.stl) | 1 | 1 | 1 | 212 × 6 × 2.4 |
| T02 | [cord_gauge](../stl/cord_gauge.stl) | 0 | 1 | 1 | 200 × 36 × 30 |
| T03 | [end_paddle](../stl/end_paddle.stl) | 1 | 1 | 1 | 100 × 130 × 5 |
| T04 | [cord_cleat](../stl/cord_cleat.stl) | 0 | 0 | 1 | 50 × 30 × 12 |
| C01 | [fit_coupon](../stl/fit_coupon.stl) | 1 | 1 | 1 | 118 × 78 × 7 |
| C02 | [key_coupon](../stl/key_coupon.stl) | 1 | 1 | 1 | 64 × 36 × 7 |
| C03 | [rule](../stl/rule.stl) | 0 | 1 | 1 | 200 × 24 × 3.5 |

## Orientación y soportes

| Pieza | Orientación / observación |
|---|---|
| H01 | Plano inferior; soportes locales bajo orejas de índice |
| H02N | Cara amplia ya apoyada; revisar puentes de bisagra |
| H02S | Cara amplia ya apoyada; revisar puentes de bisagra |
| H03 | Plano D hacia cama; brim 2 mm |
| H04 | Vertical, base pequeña; brim 3 mm |
| H05 | Cabeza a cama |
| R01 | Vertical; brim 5 mm |
| R02 | Diagonal en cama ya aplicada; brim 2 mm |
| R03 | Base circular |
| R04 | Plana |
| R05A | Plano |
| R05B | Plano |
| R05C | Plano |
| B01 | Cara plana a cama |
| B02 | Plana |
| D01A | Aro abierto; usar forro |
| D01B | Aro abierto; usar forro |
| D01C | Aro abierto; usar forro |
| D02 | Disco a cama; cubrir con barrera |
| G01A | Base a cama; usar forro |
| G01B | Base a cama; usar forro |
| O01 | Base a cama |
| O02 | Base a cama; usar forro |
| O03 | Cara cerrada a cama; invertir en laminador |
| M01 | Base a cama |
| T01 | Plana; brim 2 mm |
| T02 | Base a cama |
| T03 | Plana |
| T04 | Base a cama |
| C01 | Plano |
| C02 | Plano |
| C03 | Plana |

No se necesitan tornillos, metal ni adhesivo. Las barreras alimentarias, hojas, cuerda y comida son consumibles externos. La regla y medidor no cortan. Herramientas de preparación (tijera, balanza, cocción) no están incluidas.

No se publican gramos ni horas sin un laminado real. Los volúmenes del informe de geometría representan sólidos cerrados, no consumo con relleno.
