"""Funciones fisicas puras para el diseno iterativo de palas."""

import numpy as np

RHO_AIR = 1.225
MU_AIR = 1.789e-5
AXIAL_INDUCTION = 1.0 / 3.0


def rpm_to_omega(rpm: float) -> float:
    return rpm * np.pi / 30.0


def calc_lambda(erradioak: np.ndarray, rpm: float, v_wind: float) -> np.ndarray:
    omega = rpm_to_omega(rpm)
    return (omega * erradioak) / v_wind


def calc_phi_rad(lambda_r: float) -> float:
    return (2.0 / 3.0) * np.arctan(1.0 / lambda_r)


def calc_relative_velocity(v_wind: float, phi_rad: float) -> float:
    return v_wind * (1.0 - AXIAL_INDUCTION) / np.sin(phi_rad)


def calc_reynolds(erradioa: float, korda: float, rpm: float, v_wind: float) -> float:
    omega = rpm_to_omega(rpm)
    lambda_r = (omega * erradioa) / v_wind
    phi_rad = calc_phi_rad(lambda_r)
    u_rel = calc_relative_velocity(v_wind, phi_rad)
    return korda * u_rel * RHO_AIR / MU_AIR


def calc_reynolds_array(
    erradioak: np.ndarray, kordak: np.ndarray, rpm: float, v_wind: float
) -> np.ndarray:
    return np.array(
        [calc_reynolds(r, c, rpm, v_wind) for r, c in zip(erradioak, kordak)],
        dtype=float,
    )


def calc_station_metrics(
    erradioa: float, korda: float, rpm: float, v_wind: float
) -> dict[str, float]:
    omega = rpm_to_omega(rpm)
    lambda_r = (omega * erradioa) / v_wind
    phi_rad = calc_phi_rad(lambda_r)
    u_rel = calc_relative_velocity(v_wind, phi_rad)
    reynolds = korda * u_rel * RHO_AIR / MU_AIR
    return {
        "lambda": lambda_r,
        "phi_deg": np.degrees(phi_rad),
        "u_rel": u_rel,
        "reynolds": reynolds,
    }
