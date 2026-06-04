"""
Script de migración para agregar columnas faltantes a la tabla estudiantes.
Ejecutar: python scripts/migrate_add_student_fields.py
"""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "dropout.db"

COLUMNS = ["correo", "nombres", "apellidos"]


def get_existing_columns(cursor):
    cursor.execute("PRAGMA table_info(estudiantes)")
    return {row[1] for row in cursor.fetchall()}


def migrate():
    if not DB_PATH.exists():
        print(f"⚠️ Base de datos no encontrada: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    existing = get_existing_columns(cursor)
    added = []

    for col in COLUMNS:
        if col not in existing:
            try:
                cursor.execute(f"ALTER TABLE estudiantes ADD COLUMN {col} TEXT")
                added.append(col)
                print(f"  ✓ Agregada columna: {col}")
            except Exception as e:
                print(f"  ✗ Error con {col}: {e}")

    conn.commit()
    conn.close()

    if added:
        print(f"\n✅ Migración completada. Columnas agregadas: {added}")
    else:
        print("\nℹ️  No se requieren migraciones. Todas las columnas ya existen.")


if __name__ == "__main__":
    print("🔄 Iniciando migración...")
    migrate()