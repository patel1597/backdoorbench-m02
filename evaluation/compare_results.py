import csv
from pathlib import Path

# Locate the repository's root directory
ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"
OUTPUT = Path(__file__).resolve().parent / "results_summary.csv"

# Existing completed BadNets experiments at 10% poisoning
EXPERIMENTS = {
    "Stock VGG19-BN": "rahil_badnet_0_1_local",
    "Modified VGG19-BN": "rahil_vgg19_cifar_0_1",
}


def read_metrics(csv_path):
    """Read final test metrics from a BackdoorBench summary CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing results: {csv_path}")

    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row.get("", "").strip() == "last":
                return {
                    "clean_accuracy": float(row["test_acc"]),
                    "asr": float(row["test_asr"]),
                }

    raise ValueError(f"No 'last' row found in {csv_path}")


def evaluate_experiment(model_name, folder_name):
    """Compare undefended attack against FT and NC."""
    folder = LOGS / folder_name

    attack = read_metrics(folder / "attack_df_summary.csv")

    paths = {
        "FT": folder / "defense" / "ft" / "ft_df_summary.csv",
        "NC": folder / "defense" / "nc" / "nc_df_summary.csv",
    }

    results = []

    for defense, path in paths.items():
        defended = read_metrics(path)

        results.append({
            "model": model_name,
            "attack": "BadNets",
            "poisoning_ratio": "10%",
            "defense": defense,
            "baseline_clean_accuracy": round(
                attack["clean_accuracy"] * 100, 2
            ),
            "baseline_asr": round(attack["asr"] * 100, 2),
            "defended_clean_accuracy": round(
                defended["clean_accuracy"] * 100, 2
            ),
            "defended_asr": round(defended["asr"] * 100, 2),
            "asr_reduction_pp": round(
                (attack["asr"] - defended["asr"]) * 100, 2
            ),
            "clean_accuracy_change_pp": round(
                (defended["clean_accuracy"]
                 - attack["clean_accuracy"]) * 100, 2
            ),
        })

    return results


def main():
    all_results = []

    for model_name, folder_name in EXPERIMENTS.items():
        all_results.extend(
            evaluate_experiment(model_name, folder_name)
        )

    fieldnames = list(all_results[0].keys())

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print("\nBadNets Defense Evaluation (10% Poisoning)")
    print("-" * 85)

    for row in all_results:
        print(f"\nModel: {row['model']}")
        print(f"Defense: {row['defense']}")
        print(f"Baseline ASR: {row['baseline_asr']:.2f}%")
        print(f"Defended ASR: {row['defended_asr']:.2f}%")
        print(
            f"ASR reduction: {row['asr_reduction_pp']:.2f} "
            "percentage points"
        )
        print(
            f"Clean accuracy change: "
            f"{row['clean_accuracy_change_pp']:+.2f} "
            "percentage points"
        )

    print(f"\nResults saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
