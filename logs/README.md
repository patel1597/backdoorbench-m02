# Rahil Patel (rnp83): defense runs (FT and NC) on BadNets 10%

Setup, reproduction commands, patches and the full failure log are in the [root README](../README.md). This file only describes what is in each folder here. All runs are BackdoorBench commit `f02e3534645f0ee63d6848653062cd6c0d6c400d`, CIFAR-10, BadNets (3x3 white square, target label 0), 10% poisoning, seed 0, Colab free T4, single run each.

## Folders

| Folder | Model | Role |
|---|---|---|
| `rahil_vgg19_cifar_0_1/` | `vgg19_bn_cifar` (Ahmed's modified VGG19-BN), 30 epochs, batch 32 | **Main runs:** attack, NC, FT |
| `rahil_badnet_0_1_local/` | stock `vgg19_bn`, 30 epochs | Cross-check and **fallback trace**: attack, NC, FT |
| `test_badnet_0_1/` | stock `vgg19_bn`, 2 epochs | Smoke test only: the backdoor did not form (ASR about 8%), so no defense result from it counts |

Each run folder holds the attack log, `attack_df.csv`, `attack_df_summary.csv`, the metric plots, and `defense/nc/` and `defense/ft/`. Model files and poisoned images are not stored here because they are too large.

## Results

| Run | Stage | Clean accuracy | ASR |
|---|---|---|---|
| `rahil_vgg19_cifar_0_1` | Undefended | 0.8762 | 0.9671 |
| | After NC | 0.9061 | 0.0108 |
| | After FT (30 epochs) | 0.9041 | 0.9169 |
| `rahil_badnet_0_1_local` | Undefended | 0.8629 | 0.9286 |
| | After NC | 0.8824 | 0.0098 |
| | After FT (30 epochs) | 0.8749 | 0.1424 |

**NC detection**

| Run | Flagged label | Its mask norm | Median | MAD | Anomaly index |
|---|---|---|---|---|---|
| `rahil_vgg19_cifar_0_1` | 0 | 5.09 | 73.68 | 26.11 | 2.627 |
| `rahil_badnet_0_1_local` | 0 | 8.01 | 74.95 | 30.44 | 2.199 |

Label 0 is the true target. An anomaly index above about 2 counts as flagged.

## Notes

- FT removed most of the backdoor on stock `vgg19_bn` (ASR 0.93 to 0.14) but little on `vgg19_bn_cifar` (0.97 to 0.92). We do not know why and have not tested an explanation.
- Clean accuracy rises after NC partly because its unlearning stage trains for 100 epochs, more than the 30-epoch attack models received.
- FT was run for 30 epochs instead of the default 100, with `ratio` 0.05.
- Results from the two architectures are not combined into one comparison.
- The ASR denominator is not yet confirmed. The backdoor test set has 9,000 images, which is consistent with excluding the 1,000 images whose true label is already the target. This still needs to be checked in the code.

## Fallback trace

`logs/rahil_badnet_0_1_local/`
