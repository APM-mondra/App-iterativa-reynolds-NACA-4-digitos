"""Utilidades para perfiles NACA."""

import aerosandbox as asb

ESPESORES = [8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]


def nacas_fase1() -> list[str]:
    return ["0012"] + [f"{m}412" for m in range(1, 10)]


def nacas_fase2(m_hautatua: str) -> list[str]:
    return [f"{m_hautatua}{p}12" for p in range(1, 10)]


def nacas_fase3(m_hautatua: str, p_hautatua: str) -> list[str]:
    return [f"{m_hautatua}{p_hautatua}{t:02d}" for t in ESPESORES]


def is_valid_naca_digit_pair(naca: str) -> bool:
    m, p = int(naca[0]), int(naca[1])
    return not ((m > 0 and p == 0) or (m == 0 and p > 0))


def sortu_naca_txt(naca: str) -> str:
    m = int(naca[0]) * 1.0
    p = int(naca[1]) * 10.0
    t = int(naca[2:]) * 1.0
    goiburua = f"NACA {naca} Airfoil M={m}% P={p}% T={t}%"

    perfila = asb.Airfoil(f"naca{naca}")
    koordenatuak = perfila.coordinates

    lerroak = [goiburua]
    for x, y in koordenatuak:
        lerroak.append(f" {x:9.6f}  {y:9.6f}")

    return "\n".join(lerroak)


def get_airfoil_coordinates(naca: str) -> tuple[list[float], list[float]]:
    perfila = asb.Airfoil(f"naca{naca}")
    xs = [coord[0] for coord in perfila.coordinates]
    ys = [coord[1] for coord in perfila.coordinates]
    return xs, ys
