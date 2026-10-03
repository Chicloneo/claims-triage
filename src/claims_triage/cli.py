# UBICACION FINAL (ejercicio 1): src/claims_triage/cli.py
"""Programa principal: CSV -> validacion -> preprocess -> modelo -> CSV de salida.

Se ejecuta asi (desde la raiz del proyecto):
    uv run python -m claims_triage.cli --input data/claims.csv --output .tmp/predicciones.csv

Pasos del programa:
  1. read_claims : lee el CSV y valida cada fila con ClaimRequest    (ejercicio 2)
  2. load_model  : carga el modelo                                    (ejercicio 4)
  3. predict     : predice cada siniestro                             (ejercicios 3 y 4)
  4. escribe el CSV de salida                                         (ejercicio 4)
"""

import argparse
import csv  # noqa: F401
import os  # noqa: F401
import sys  # noqa: F401

from pydantic import ValidationError  # noqa: F401

from claims_triage.contracts import ClaimRequest  # noqa: F401
from claims_triage.inference import load_model, predict  # noqa: F401

import pandas as pd
from pathlib import Path

# Columnas del CSV de salida, en este orden.
OUTPUT_COLUMNS = ["claim_id", "decision", "risk_probability", "model_version"]


def read_claims(path):
    """EJERCICIO 2: leer el CSV y devolver la lista de siniestros validados."""
    # TODO 2.8: leer el fichero CSV indicado, cuyas filas tienen las columnas
    #   de ClaimRequest.
    fichero = pd.read_csv(path, dtype=str, keep_default_na=False)
    #esto lo he puesto así para solucionar algunos errores
    # REVISARLO BIEN

    # TODO 2.9: validar cada fila con ClaimRequest. Si alguna fila no es valida,
    #   hay que parar con un ValueError cuyo mensaje diga en que LINEA del
    #   fichero esta el problema y cual es (la cabecera es la linea 1).
    siniestros_validados = [] # <---- los modelos reciben listas

    for index, row in fichero.iterrows():
        try:
            claim = ClaimRequest(**row.to_dict())
            #claim = ClaimRequest.model_validate(row.to_dict()) 
            # valen las dos formas. Creo que es así
            siniestros_validados.append(claim)
        except Exception as e:
            raise ValueError(f"El error está en la línea {index + 2} : {e}")

    # TODO 2.10: devolver la lista con todos los siniestros validados.
    return siniestros_validados


def main(argv=None):
    # Ya hecho: lee los argumentos --input, --output y --model.
    parser = argparse.ArgumentParser(description="Triaje de siniestros")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="models/claims_triage_model.joblib")
    args = parser.parse_args(argv)  # noqa: F841

    # TODO 4.12: leer y validar los siniestros y cargar el modelo. Si algo de
    #   eso falla (ValueError), mostrar el error por la salida de errores y
    #   terminar con codigo de salida 2, SIN escribir ningun fichero.
    try:
        claims = read_claims(args.input)
        model = load_model(args.model)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2

    # TODO 4.13: obtener la prediccion de cada siniestro.
    predictions = []
    for claim in claims:
        prediction = predict(model, claim)
        predictions.append(prediction.dict())

    # TODO 4.14: escribir el CSV de salida (con las columnas de OUTPUT_COLUMNS)
    #   en la ruta --output, creando la carpeta si no existe. Solo se escribe
    #   cuando todo lo anterior ha ido bien: si algo falla, no debe quedar un
    #   fichero a medias.
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df = pd.DataFrame(predictions)
    df.to_csv(args.output, index=False, columns=OUTPUT_COLUMNS)

    # TODO 4.15: mostrar cuantos siniestros se han predicho y terminar con
    #   codigo de salida 0.
    print(f"Se gan predicho {len(predictions)} siniestros")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
