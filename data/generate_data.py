"""Genera un dataset de ventas sintético y reproducible (seed fija)."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
N_ROWS = 500
PRODUCTOS = {101: 10.0, 102: 25.5, 103: 7.75, 104: 120.0, 105: 3.2}


def generate(path: Path, n_rows: int = N_ROWS, seed: int = SEED) -> None:
    rnd = random.Random(seed)
    start = date(2023, 1, 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "producto_id", "cantidad", "precio_unitario"])
        for _ in range(n_rows):
            pid = rnd.choice(list(PRODUCTOS))
            w.writerow(
                [
                    (start + timedelta(days=rnd.randint(0, 29))).isoformat(),
                    pid,
                    rnd.randint(1, 20),
                    PRODUCTOS[pid],
                ]
            )


if __name__ == "__main__":
    out = Path(__file__).parent / "ventas.csv"
    generate(out)
    print(f"Dataset generado: {out} ({N_ROWS} filas)")
