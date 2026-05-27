import argparse

from src.etl import run_etl
from src.train import run_training


def main():
    parser = argparse.ArgumentParser(description="Student Dropout Prediction")
    parser.add_argument(
        "--train",
        action="store_true",
        help="Ejecutar ETL + entrenamiento del modelo",
    )
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Omitir optimización de hiperparámetros",
    )

    args = parser.parse_args()

    df = run_etl()

    if args.train:
        run_training(optimizar=not args.no_optimize)


if __name__ == "__main__":
    main()
