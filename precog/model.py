# precog/model.py
"""
Módulo 'precog' - función predecir_riesgo para integración con dashboard.

Función principal:
    predecir_riesgo(velocidad_media, intensidad_lluvia, humedad, top3_intensities=None)

Retorna:
    float - riesgo en porcentaje (0.0 - 100.0)
"""

import numpy as np

def _normalizar(vel, lluvia, hum):
    # Normaliza a 0-1 según rangos esperados (ajustables)
    return np.clip(vel / 150.0, 0.0, 1.0), np.clip(lluvia / 200.0, 0.0, 1.0), np.clip(hum / 100.0, 0.0, 1.0)

def predecir_riesgo(velocidad_media, intensidad_lluvia, humedad, top3_intensities=None):
    """
    Calcula un porcentaje de riesgo (0-100).

    Parámetros:
    - velocidad_media: float (km/h) esperada 0-150
    - intensidad_lluvia: float (mm/h) esperada 0-200
    - humedad: float (%) 0-100
    - top3_intensities: lista/iterable con 3 valores [0..1] representando intensidad de los 3 clusters críticos.
                        Si es None, se considera 0.

    Lógica:
    - Normaliza entradas.
    - Combina factores con pesos (configurables).
    - Aplica influencia de top3 (si existen).
    - Clips y devuelve float.
    """
    # Validación básica
    try:
        vel = float(velocidad_media)
        lluvia = float(intensidad_lluvia)
        hum = float(humedad)
    except Exception:
        raise ValueError("Entradas velocidad, lluvia y humedad deben ser numéricas.")

    v_n, r_n, h_n = _normalizar(vel, lluvia, hum)

    # Pesos (puedes ajustar)
    w_vel = 0.35
    w_lluvia = 0.45
    w_hum = 0.20

    linear_score = w_vel * v_n + w_lluvia * r_n + w_hum * h_n  # rango 0..1

    # Influencia de los clusters top3
    if top3_intensities is None:
        cluster_factor = 0.0
    else:
        try:
            arr = np.array(list(top3_intensities), dtype=float)
            if arr.size == 0:
                cluster_factor = 0.0
            else:
                # esperar valores en 0..1; si vienen en otro rango se normalizan por su max
                arr = np.clip(arr, 0.0, 1.0)
                cluster_factor = float(np.mean(arr))
        except Exception:
            cluster_factor = 0.0

    # Ajuste por cluster (máx +50% riesgo)
    adjusted_score = linear_score * (1.0 + 0.5 * cluster_factor)

    # Aplicar una suave no-linealidad para penalizar valores medios/altos
    # (ej. función logística escalada)
    k = 6.0
    x = adjusted_score
    logistic = 1.0 / (1.0 + np.exp(-k * (x - 0.5)))
    # mezclar lineal y logístico para estabilidad
    final_score = 0.6 * adjusted_score + 0.4 * logistic

    percent = float(np.clip(final_score * 100.0, 0.0, 100.0))
    return percent
