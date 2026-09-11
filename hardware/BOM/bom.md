# Bill of Materials (BOM)

Complete parts list to build one HumanaOpen. Quantities are per robot.

> Work in progress — sections are filled in as the build is completed.

## Cost summary

The control board is optional. Fasteners are yet to be added.

| Section | Subtotal (RMB) |
|---------|----------------|
| Mechanical / structure | 290 |
| 3D printed parts | 300 |
| Motion / actuation | 4,110 |
| Electronics (excl. control board) | 953 |
| Cables / misc | 65 |
| **Total (excl. control board, excl. fasteners)** | **≈ 5,718** |

## Mechanical / structure

### Differential base

| Part / description | Spec / size | Qty | Unit price | Total | Source |
|--------------------|-------------|-----|------------|-------|--------|
| Caster wheel (differential-drive base) | 5 inch (12.7 cm) | 2 | 33 RMB | 66 RMB | [link](https://e.tb.cn/h.8KjMwtvPCctqYIB?tk=8CsCTTQGr5Y) |
| Swivel caster wheel | Ø25 mm, wheel width 13 mm, base 39 × 33 mm, mounting hole pitch 30 × 24 mm, mounting height 37.5 mm | 2 | 3 RMB | 6 RMB | [link](https://e.tb.cn/h.8KvHhYsMbquYeNy?tk=0FWcTTwToO5) |
| Ball bearing | 6706RS, 30 × 37 × 4 mm | 2 | 11 RMB | 22 RMB | [link](https://e.tb.cn/h.8ppes1EsjZbPZ7G?tk=j67IT6WceLJ) |

### Lift structure

| Part / description | Spec / size | Qty | Unit price | Total | Source |
|--------------------|-------------|-----|------------|-------|--------|
| Graphite self-lubricating bronze bushing | 8 × 15 × 24 mm | 2 | 6 RMB | 12 RMB | [link](https://e.tb.cn/h.8LyLe0PfJWP7vzO?tk=2RPvT6qeK39) |
| T-leadscrew with brass nut | T8 × 300 mm | 1 | 12 RMB | 12 RMB | [link](https://e.tb.cn/h.8MsdKG0YofaR0MA?tk=FcbUTTjETcR) |
| Bearing (bearing 608-2Z, iron shield) — Japan VBI | 8 × 22 × 7 mm | 1 | 1 RMB | 1 RMB | [link](https://e.tb.cn/h.8KWfffzVtRIZkMB?tk=IkvxT6Jfnwz) |
| Aluminium rigid coupling | Ø20 × 25 mm, bores Ø8 / Ø6 | 1 | 4 RMB | 4 RMB | [link](https://e.tb.cn/h.8K8vuIaWV6FE6xU?tk=vCWeTTQZ5ji) |
| Bus-servo flat-shaft flange (A servo horn) | A-style servo horn | 1 | 12 RMB | 12 RMB | [link](https://e.tb.cn/h.8LBtAQFkrs6S6lb?tk=qVBvTTQV6sU) |
| Hardened precision shaft | Ø8 × 310 mm, hardened | 2 | 3.5 RMB | 7 RMB | — |
| Aluminium extrusion (M6 tapped holes at both ends) | 2040 EU-spec silver, 300 mm | 1 | 10 RMB | 10 RMB | [link](https://e.tb.cn/h.8oH8sbI8ngX3S5c?tk=VQAlTTQObBL) |

### Leader arm

| Part / description | Spec / size | Qty | Unit price | Total | Source |
|--------------------|-------------|-----|------------|-------|--------|
| Aluminium extrusion | 3060 EU-spec silver | 1 | 30 RMB | 30 RMB | — |
| Aluminium plate | 200 × 300 mm, M6 holes — 116 mm hole spacing along the 200 mm side, 30 mm along the 300 mm side | 1 | 100 RMB | 100 RMB | — |
| Aluminium extrusion corner bracket | 3060, 90° double-slot | 2 | 4 RMB | 8 RMB | [link](https://qr.1688.com/s/aVNYKMW5) |

## 3D printed parts

Filament: Bambu Lab PLA Basic / Anycubic PLA. A large-build-volume printer
(e.g. Anycubic Kobra 3 MAX) is required for the large printed parts.

| Part / description | STL file | Qty | Total cost | Notes |
|--------------------|----------|-----|------------|-------|
| _see `stl/`_        |          | 6   | ≈ 300 RMB | Requires a large-format printer (Anycubic Kobra 3 MAX) |

## Fasteners

| Part / description | Spec | Qty | Source / link |
|--------------------|------|-----|---------------|
|                   |      |     |               |

## Motion / actuation

| Part / description | Model | Qty | Unit price | Total | Source |
|--------------------|-------|-----|------------|-------|--------|
| Follower arm servos (left + right, 8 each) | FEETECH ST3215 C018 | 16 | 110 RMB | 1,760 RMB | [link](https://e.tb.cn/h.8KS047iJugyLfv9?tk=DSDWTTSxLeS) |
| Head servos (pan + tilt) | FEETECH ST3215 C018 | 2 | 110 RMB | 220 RMB | [link](https://e.tb.cn/h.8KS047iJugyLfv9?tk=DSDWTTSxLeS) |
| Lift motor | FEETECH ST3250 | 1 | 310 RMB | 310 RMB | [link](https://e.tb.cn/h.8LwGPtampPRo6fc?tk=uCJATT7aXjl) |
| Base wheel motors (left + right) | FEETECH ST3215 C018 | 2 | 110 RMB | 220 RMB | [link](https://e.tb.cn/h.8KS047iJugyLfv9?tk=DSDWTTSxLeS) |
| Leader arm servos (left + right, 8 each) | FEETECH ST3215 C046 | 16 | 100 RMB | 1,600 RMB | [link](https://e.tb.cn/h.8KS047iJugyLfv9?tk=DSDWTTSxLeS) |

## Electronics

| Part / description | Model / spec | Qty | Unit price | Total | Source |
|--------------------|--------------|-----|------------|-------|--------|
| Main control board (Host) — optional | Raspberry Pi 5 4GB | 1 | 1,200 RMB | 1,200 RMB | — |
| Main control board (Host) — optional | Jetson Orin Nano Super 8GB | 1 | 3,800 RMB | 3,800 RMB | — |
| Camera (head/left_wrist/right_wrist/chest) | 720P 90° distortion-free USB | 4 | 70 RMB | 280 RMB | [link](https://e.tb.cn/h.8KRXD6pf6IHHQNu?tk=Liq1TT8421C) |
| Follower (from) power supply | 12V 4A | 1 | 20 RMB | 20 RMB | — |
| Leader (master) power supply | 7.3V 3A | 2 | 20 RMB | 40 RMB | — |
| Bus servo driver board | Waveshare (微雪) bus servo driver | 2 | 27 RMB | 54 RMB | [link](https://e.tb.cn/h.8Lya2xQuOF0N34m?tk=HTlUTT8TJLG) |
| Battery | 20000mAh 140W dual Type-C + USB-A | 1 | 399 RMB | 399 RMB | [link](https://e.tb.cn/h.8oI8XjbzbNgEeyh?tk=o73uTT8juXp) |
| Display (optional) | 7" touch with case, 1024×600 | 1 | 160 RMB | 160 RMB | [link](https://e.tb.cn/h.8JQRkOZKPsCPwZ7?tk=60rcT7YLj2W) |

## Cables / misc

| Part / description | Spec | Qty | Unit price | Total | Source |
|--------------------|------|-----|------------|-------|--------|
| USB-to-Type-C cable | USB 3.2, 10 Gbps | 2 | 8.5 RMB | 17 RMB | [link](https://e.tb.cn/h.8KRq9s1kJBHLtdN?tk=yS9XTT8GzSZ) |
| Y-split Type-C to DC 5521 cable | 0.5 m | 1 | 20 RMB | 20 RMB | [link](https://e.tb.cn/h.8KRHy0GP3Zk8Rw8?tk=UkoSTT8Dq9k) |
| USB to DC 5521 cable (optional, Raspberry Pi) | 0.5 m | 1 | 7 RMB | 7 RMB | [link](https://e.tb.cn/h.8J9K33ZS7bNSVQz?tk=PukJT71DTRR) |
| Type-C to DC 5521 cable (optional, Jetson) | 0.5 m | 1 | 9 RMB | 9 RMB | [link](https://e.tb.cn/h.8qUeZkgpcKBiZ6R?tk=239sT7cfg4G) |
| Terminal wire | 3P 5264 reverse terminal wire, 1000 mm | 1 | 3 RMB | 3 RMB | [link](https://e.tb.cn/h.8oTllunUw9ECpZp?tk=PRvNT60hcKX) |
| Terminal wire | 3P 5264 reverse terminal wire, 500 mm | 1 | 3 RMB | 3 RMB | [link](https://e.tb.cn/h.8oTllunUw9ECpZp?tk=PRvNT60hcKX) |
| Terminal wire | 3P 5264 reverse terminal wire, 200 mm | 2 | 3 RMB | 6 RMB | [link](https://e.tb.cn/h.8oTllunUw9ECpZp?tk=PRvNT60hcKX) |
| Chest camera cable (optional) | 100 mm | 1 | included with camera | — | — |
| Head camera cable | 300 mm | 1 | included with camera | — | — |
| Wrist camera cable | 900 mm | 2 | included with camera | — | — |
