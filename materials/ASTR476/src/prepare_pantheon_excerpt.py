"""Extract a compact Pantheon+ plotting/analysis subset and matching covariance."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np


COURSE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = COURSE_ROOT / "data"
RELEASE_ROOT = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
    "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/"
)
DATA_URL = RELEASE_ROOT + "Pantheon%2BSH0ES.dat"
COVARIANCE_URL = RELEASE_ROOT + "Pantheon%2BSH0ES_STAT%2BSYS.cov"
TARGET_REDSHIFTS = np.array(
    [0.025, 0.03, 0.04, 0.05, 0.07, 0.10, 0.15, 0.20, 0.30,
     0.40, 0.60, 0.80, 1.00, 1.25, 1.50, 1.80, 2.00, 2.20]
)


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "ASTR476-course-materials/1.0"})
    with urlopen(request, timeout=60) as response:
        if response.status != 200:
            raise RuntimeError(f"Download failed with HTTP {response.status}: {url}")
        return response.read()


def parse_release_table(payload: bytes) -> tuple[list[str], list[dict[str, str]]]:
    lines = payload.decode("utf-8").splitlines()
    header = lines[0].split()
    required = {"CID", "zHD", "MU_SH0ES", "MU_SH0ES_ERR_DIAG", "IS_CALIBRATOR"}
    if not required.issubset(header):
        raise ValueError(f"Pantheon+ table lacks required columns: {sorted(required - set(header))}")
    records: list[dict[str, str]] = []
    for line_number, line in enumerate(lines[1:], start=2):
        fields = line.split()
        if not fields:
            continue
        if len(fields) != len(header):
            raise ValueError(f"Unexpected column count on Pantheon+ row {line_number}")
        records.append(dict(zip(header, fields, strict=True)))
    return header, records


def select_rows(records: list[dict[str, str]]) -> list[tuple[int, dict[str, str]]]:
    candidates = []
    seen_cids: set[str] = set()
    for source_index, record in enumerate(records):
        redshift = float(record["zHD"])
        if int(float(record["IS_CALIBRATOR"])) != 0 or redshift < 0.023:
            continue
        cid = record["CID"]
        if cid in seen_cids:
            continue
        seen_cids.add(cid)
        candidates.append((source_index, record))

    chosen: list[tuple[int, dict[str, str]]] = []
    used_indices: set[int] = set()
    for target in TARGET_REDSHIFTS:
        available = [item for item in candidates if item[0] not in used_indices]
        if not available:
            break
        selected = min(available, key=lambda item: abs(float(item[1]["zHD"]) - target))
        chosen.append(selected)
        used_indices.add(selected[0])
    if len(chosen) != len(TARGET_REDSHIFTS):
        raise ValueError("Could not find one distinct non-calibrator SN row per target redshift")
    return sorted(chosen, key=lambda item: float(item[1]["zHD"]))


def parse_covariance(payload: bytes, expected_size: int) -> np.ndarray:
    values = np.fromstring(payload.decode("ascii"), sep=" ", dtype=float)
    if values.size != expected_size * expected_size + 1:
        raise ValueError(
            f"Covariance has {values.size} values; expected {expected_size * expected_size + 1}"
        )
    declared_size = int(values[0])
    if declared_size != expected_size:
        raise ValueError(f"Covariance declares {declared_size} rows, expected {expected_size}")
    matrix = values[1:].reshape((expected_size, expected_size))
    asymmetry = float(np.max(np.abs(matrix - matrix.T)))
    if asymmetry > 5e-8:
        raise ValueError("Published covariance is not symmetric")
    return 0.5 * (matrix + matrix.T)


def prepare(output_dir: Path = DATA_DIR) -> dict[str, object]:
    data_payload = fetch_bytes(DATA_URL)
    covariance_payload = fetch_bytes(COVARIANCE_URL)
    _, records = parse_release_table(data_payload)
    if len(records) != 1701:
        raise ValueError(f"Pantheon+ release table contains {len(records)} rows, expected 1701")
    full_covariance = parse_covariance(covariance_payload, len(records))
    selected = select_rows(records)
    selected_indices = np.array([index for index, _ in selected], dtype=int)
    selected_covariance = full_covariance[np.ix_(selected_indices, selected_indices)]
    if np.min(np.linalg.eigvalsh(selected_covariance)) <= 0:
        raise ValueError("Selected Pantheon+ covariance submatrix is not positive definite")

    output_dir.mkdir(parents=True, exist_ok=True)
    table_path = output_dir / "pantheonplus-subset.csv"
    covariance_path = output_dir / "pantheonplus-subset-covariance.csv"
    table_fields = ["CID", "IDSURVEY", "zHD", "MU_SH0ES", "MU_SH0ES_ERR_DIAG",
                    "IS_CALIBRATOR", "USED_IN_SH0ES_HF"]
    with table_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=table_fields)
        writer.writeheader()
        for _, record in selected:
            writer.writerow({key: record.get(key, "") for key in table_fields})
    np.savetxt(covariance_path, selected_covariance, delimiter=",", fmt="%.12g")

    provenance = {
        "dataset": "Pantheon+SH0ES public distance and covariance release",
        "provenanceLevel": 1,
        "accessDate": "2026-09-25",
        "sourceDataUrl": DATA_URL,
        "sourceCovarianceUrl": COVARIANCE_URL,
        "sourceDataSha256": hashlib.sha256(data_payload).hexdigest(),
        "sourceCovarianceSha256": hashlib.sha256(covariance_payload).hexdigest(),
        "sourceRows": len(records),
        "sourceCovarianceShape": [len(records), len(records)],
        "excerptRows": len(selected),
        "excerptSelection": (
            "For each fixed target redshift 0.025, 0.03, 0.04, 0.05, 0.07, 0.10, "
            "0.15, 0.20, 0.30, 0.40, 0.60, 0.80, 1.00, 1.25, 1.50, 1.80, "
            "2.00, and 2.20, choose the nearest unused unique CID with IS_CALIBRATOR=0 "
            "and zHD>=0.023. Preserve original source row order for covariance indexing."
        ),
        "excerptFiles": [table_path.name, covariance_path.name],
        "covarianceRounding": (
            "The source covariance is printed to 8 decimal places and has maximum "
            "paired-entry difference 3e-8; paired entries were averaged after "
            "requiring absolute asymmetry <=5e-8."
        ),
        "limitations": (
            "This redshift-stratified excerpt is suitable for plotting and a small "
            "covariance-aware demonstration only. It is not a representative random "
            "sample and must not be reported as a Pantheon+ cosmology constraint. "
            "MU_SH0ES_ERR_DIAG is included for plotting only; inference must use the "
            "matching covariance submatrix. The full 1701x1701 covariance is not bundled."
        ),
    }
    (output_dir / "pantheonplus-subset-provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    return provenance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DATA_DIR)
    args = parser.parse_args()
    result = prepare(args.output_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()