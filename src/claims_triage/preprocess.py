# UBICACION FINAL (ejercicio 1): src/claims_triage/preprocess.py
"""EJERCICIO 3: preprocesado.

El modelo solo entiende NUMEROS y en un ORDEN concreto. Esta funcion convierte
un siniestro ya validado (un ClaimRequest) en la lista de numeros que espera.

preprocess es una función que se le va a llamar desde un bucle. Recibe un claim request. 
El bucle estará en otra función de fuera.
preprocess prepara los datos (por ejemplo, orden del input) para el modelo
"""

from .contracts import ClaimRequest

# Orden exacto en el que se entreno el modelo. NO LO CAMBIEIS.
# El modelo no sabe como se llaman las columnas: solo mira la posicion.
FEATURE_NAMES = [
    "driver_age",
    "vehicle_age_years",
    "claim_amount_eur",
    "injuries",
    "police_report",
    "policy_code",
]

# Valor que usamos cuando no se conoce la edad del vehiculo.
DEFAULT_VEHICLE_AGE = 8.0


def preprocess(request: ClaimRequest):
    """Recibe un ClaimRequest y devuelve la lista de numeros para el modelo.

    Los datos del siniestro estan en sus atributos: request.driver_age,
    request.policy_type, etc.
    """
    # TODO 3.1 (LIMPIEZA): si la edad del vehiculo no esta informada, el modelo
    #   debe recibir DEFAULT_VEHICLE_AGE en su lugar.
    if request.vehicle_age_years is None:
        request.vehicle_age_years = DEFAULT_VEHICLE_AGE

    # TODO 3.2 (CATEGORIZACION): el modelo no entiende texto, asi que el tipo
    #   de poliza debe convertirse en un codigo numerico (policy_code):
    #       basico -> 0     terceros_ampliado -> 1     todo_riesgo -> 2
    if request.policy_type == "basico":
        policy_code = 0
    elif request.policy_type == "terceros_ampliado":
        policy_code = 1
    else: #ClaimRequest ya se encarga de que la otra única opción sea "todo_riesgo"
        policy_code = 2

    # request.policy_type = policy_code <---- esto no se puede hacer, 
    # porque policy_type está tipado como Literal["basico", "terceros_ampliado", "todo_riesgo"]
    # es decir, no acepta números. Por eso hay que crear otra columna.

    # TODO 3.3: devolver los valores del siniestro, ya limpios, en el orden
    #   exacto de FEATURE_NAMES. El identificador (claim_id) no es un dato para
    #   el modelo y no debe incluirse.

    # No estamos creando una nueva variable en el contrato, ni una nueva columna en el dataframe
    # EL modelo espera una "variable" numérica policy_code, 
    # así que se lo damos tal cual, según policy_type

    return [
        request.driver_age,
        request.vehicle_age_years,
        request.claim_amount_eur,
        request.injuries,
        request.police_report,
        policy_code # esto no es un atributo de request, así que lo tienes que devolver tal cual
    ]
