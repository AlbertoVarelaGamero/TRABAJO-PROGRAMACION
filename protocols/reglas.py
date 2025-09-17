# protocols/reglas.py
"""
Reglas oficiales (simuladas) para K-Lang.
Función principal:
    decidir_protocolo(viento_kmh, inundacion_cm, temperatura_c=None, extra=None)
Devuelve un dict con:
    {
      "protocol": "VÍSPERA" | "CÓDIGO ROJO" | "RENACIMIENTO",
      "tag": "VERDE"|"AMARILLO"|"ROJO",
      "reason": "explicación breve",
      "actions": [...lista de acciones...]
    }
"""

PROTOCOLS = {
    "VÍSPERA": {
        "trigger": "Prealerta: viento > 60 km/h o inundación moderada",
        "actions": ["Notificar equipo", "Preparar recursos", "Revisar rutas críticas"]
    },
    "CÓDIGO ROJO": {
        "trigger": "Evento severo: viento > 90 km/h o inundación > 50 cm",
        "actions": ["Activar respuesta de emergencia", "Aislar activos críticos", "Comunicar a stakeholders"]
    },
    "RENACIMIENTO": {
        "trigger": "Fase de recuperación y restauración",
        "actions": ["Evaluar daños", "Iniciar reparaciones", "Revisión estratégica"]
    }
}

# Umbrales (configurables)
TH_VIGILANCIA_VIENTO = 60
TH_ALERTA_VIENTO = 90
TH_VIGILANCIA_INUND = 20
TH_ALERTA_INUND = 50

def decidir_protocolo(viento_kmh, inundacion_cm, temperatura_c=None, extra=None):
    """
    Decide qué protocolo debe activarse según entradas de sensores.
    Retorna un dict con protocolo, tag, reason y acciones.
    """
    try:
        v = float(viento_kmh)
        i = float(inundacion_cm)
    except Exception:
        raise ValueError("Viento e inundación deben ser numéricos.")

    # Prioridad: CÓDIGO ROJO > VÍSPERA > RENACIMIENTO
    if v >= TH_ALERTA_VIENTO or i >= TH_ALERTA_INUND:
        proto = "CÓDIGO ROJO"
        tag = "ROJO"
        reason = f"Viento {v:.0f} km/h >= {TH_ALERTA_VIENTO} o Inundación {i:.0f} cm >= {TH_ALERTA_INUND}"
    elif v >= TH_VIGILANCIA_VIENTO or i >= TH_VIGILANCIA_INUND:
        proto = "VÍSPERA"
        tag = "AMARILLO"
        reason = f"Viento {v:.0f} km/h >= {TH_VIGILANCIA_VIENTO} o Inundación {i:.0f} cm >= {TH_VIGILANCIA_INUND}"
    elif v < 20 and i < 5:
        proto = "RENACIMIENTO"
        tag = "VERDE"
        reason = "Condiciones calmadas (recuperación)"
    else:
        proto = "VÍSPERA"
        tag = "VERDE"
        reason = "Condiciones dentro de parámetros normales"

    actions = PROTOCOLS.get(proto, {}).get("actions", [])
    return {"protocol": proto, "tag": tag, "reason": reason, "actions": actions}
