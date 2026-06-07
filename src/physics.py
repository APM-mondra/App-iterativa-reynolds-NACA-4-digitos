"""Funciones fisicas puras para el diseno iterativo de palas."""

import numpy as np

RHO_AIR = 1.225
MU_AIR = 1.789e-5
AXIAL_INDUCTION = 1.0 / 3.0
MIN_SIN_PHI = 1e-6


def rpm_to_omega(rpm: float) -> float:
    return rpm * np.pi / 30.0


def calc_lambda(erradioak: np.ndarray, rpm: float, v_wind: float) -> np.ndarray:
    omega = rpm_to_omega(rpm)
    return (omega * erradioak) / v_wind


def calc_phi_rad(lambda_r: float) -> float:
    return (2.0 / 3.0) * np.arctan(1.0 / lambda_r)


def calc_relative_velocity(v_wind: float, phi_rad: float) -> float:
    sin_phi = max(abs(np.sin(phi_rad)), MIN_SIN_PHI)
    return v_wind * (1.0 - AXIAL_INDUCTION) / sin_phi


def calc_reynolds(erradioa: float, korda: float, rpm: float, v_wind: float) -> float:
    if korda <= 0 or v_wind <= 0:
        return 0.0

    omega = rpm_to_omega(rpm)
    lambda_r = (omega * erradioa) / v_wind
    phi_rad = calc_phi_rad(lambda_r)
    u_rel = calc_relative_velocity(v_wind, phi_rad)
    reynolds = korda * u_rel * RHO_AIR / MU_AIR
    return float(reynolds) if np.isfinite(reynolds) else 0.0


def calc_reynolds_array(
    erradioak: np.ndarray, kordak: np.ndarray, rpm: float, v_wind: float
) -> np.ndarray:
    n = min(len(erradioak), len(kordak))
    if n == 0:
        return np.array([], dtype=float)

    return np.array(
        [calc_reynolds(erradioak[i], kordak[i], rpm, v_wind) for i in range(n)],
        dtype=float,
    )


def calc_station_metrics(
    erradioa: float, korda: float, rpm: float, v_wind: float
) -> dict[str, float]:
    omega = rpm_to_omega(rpm)
    lambda_r = (omega * erradioa) / v_wind if v_wind > 0 else 0.0
    phi_rad = calc_phi_rad(lambda_r) if lambda_r > 0 else 0.0
    u_rel = calc_relative_velocity(v_wind, phi_rad) if v_wind > 0 else 0.0
    reynolds = calc_reynolds(erradioa, korda, rpm, v_wind)
    return {
        "lambda": float(lambda_r),
        "phi_deg": float(np.degrees(phi_rad)),
        "u_rel": float(u_rel) if np.isfinite(u_rel) else 0.0,
        "reynolds": reynolds,
    }
