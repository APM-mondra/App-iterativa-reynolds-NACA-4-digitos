"""Calculos aerodinamicos cacheados con NeuralFoil."""

from __future__ import annotations

import numpy as np
import aerosandbox as asb
import neuralfoil as nf
import streamlit as st

from src.naca import is_valid_naca_digit_pair


@st.cache_data(show_spinner=False)
def get_aero_cached(
    naca: str,
    reynolds: float,
    alpha_min: float,
    alpha_max: float,
    alpha_steps: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
    if not is_valid_naca_digit_pair(naca):
        return None

    try:
        alphas = np.linspace(alpha_min, alpha_max, alpha_steps)
        aero = nf.get_aero_from_airfoil(
            asb.Airfoil(f"naca{naca}"), alphas, reynolds
        )
        return alphas, np.asarray(aero["CL"]), np.asarray(aero["CD"])
    except Exception:
        return None


def evaluate_naca_list(
    naca_list: list[str],
    reynolds: float,
    alpha_min: float,
    alpha_max: float,
    alpha_steps: int,
) -> list[dict]:
    results: list[dict] = []

    for naca in naca_list:
        cached = get_aero_cached(naca, reynolds, alpha_min, alpha_max, alpha_steps)
        if cached is None:
            continue

        alphas, cl, cd = cached
        cl_cds = np.divide(cl, cd, out=np.zeros_like(cl), where=(cd > 0))

        if np.max(cl_cds) <= 0:
            continue

        best_idx = int(np.argmax(cl_cds))
        results.append(
            {
                "naca": naca,
                "alphas": alphas,
                "cl": cl,
                "cd": cd,
                "cl_cd": cl_cds,
                "max_cl_cd": float(cl_cds[best_idx]),
                "alpha_opt": float(alphas[best_idx]),
                "cl_at_opt": float(cl[best_idx]),
                "cd_at_opt": float(cd[best_idx]),
            }
        )

    results.sort(key=lambda item: item["max_cl_cd"], reverse=True)
    return results


def get_phase_cache_key(estazioa: int, fase: str, reynolds: float) -> str:
    return f"{estazioa}_{fase}_{round(reynolds, 0)}"


def get_or_compute_phase_results(
    cache: dict,
    cache_key: str,
    naca_list: list[str],
    reynolds: float,
    alpha_min: float,
    alpha_max: float,
    alpha_steps: int,
) -> list[dict]:
    if cache_key in cache:
        return cache[cache_key]

    results = evaluate_naca_list(
        naca_list, reynolds, alpha_min, alpha_max, alpha_steps
    )
    cache[cache_key] = results
    return results
