# Rahil Patel (rnp83): defense runs (FT and NC) on BadNets

Setup, reproduction commands, patches and the full failure log are in the [root README](../README.md). This file only describes what is in each folder here. All runs are BackdoorBench commit `f02e3534645f0ee63d6848653062cd6c0d6c400d`, CIFAR-10, BadNets (3x3 white square, target label 0), seed 0, Colab free T4, single run each. All defenses (NC, FT) were run by Rahil.

## Folder naming
`0_1` in a folder name means poisoning ratio 0.1 (10%), not 1%.

## Folders

| Folder | Model | Poisoning | Role |
|---|---|---|---|
| `rahil_vgg19_cifar_0_1/` | `vgg19_bn_cifar` (Ahmed's modified VGG19-BN), 30 epochs, batch 32 | 10% | **Main:** attack (Rahil's Colab re-run of Ahmed's config), NC, FT |
| `rahil_badnet_5pct/` | `vgg19_bn_cifar` | 5% | Attack trained by Ahmed; NC, FT |
| `rahil_badnet_1pct/` | `vgg19_bn_cifar` | 1% | Attack trained by Ahmed; NC, FT |
| `rahil_badnet_0_1_local/` | stock `vgg19_bn`, 30 epochs | 10% | Cross-check and **fallback trace**: attack, NC, FT |
| `test_badnet_0_1/` | stock `vgg19_bn`, 2 epochs | 10% | Smoke test only: the backdoor did not form (ASR about 8%), so no defense result from it counts |

Each run folder holds the attack log, `attack_df.csv`, `attack_df_summary.csv`, the metric plots, and `defense/nc/` and `defense/ft/`. Model files and poisoned images are not stored here because they are too large.

## Results

| Run | Stage | Clean accuracy | ASR |
|---|---|---|---|
| `rahil_vgg19_cifar_0_1` (10%) | Undefended | 0.8762 | 0.9671 |
| | After NC | 0.9061 | 0.0108 |
| | After FT (30 epochs) | 0.9041 | 0.9169 |
| `rahil_badnet_5pct` (5%) | Undefended | 0.8818 | 0.9481 |
| | After NC | 0.9124 | 0.0110 |
| | After FT (30 epochs) | 0.9069 | 0.8897 |
| `rahil_badnet_1pct` (1%) | Undefended | 0.8759 | 0.8299 |
| | After NC | 0.9118 | 0.0112 |
| | After FT (30 epochs) | 0.9067 | 0.6936 |
| `rahil_badnet_0_1_local` (10%, stock `vgg19_bn`) | Undefended | 0.8629 | 0.9286 |
| | After NC | 0.8824 | 0.0098 |
| | After FT (30 epochs) | 0.8749 | 0.1424 |

**NC detection**

| Run | Flagged label | Its mask norm | Median | MAD | Anomaly index |
|---|---|---|---|---|---|
| `rahil_vgg19_cifar_0_1` (10%) | 0 | 5.09 | 73.68 | 26.11 | 2.627 |
| `rahil_badnet_5pct` (5%) | 0 | 2.92 | 65.90 | 11.95 | 5.268 |
| `rahil_badnet_1pct` (1%) | 0 | 5.24 | 75.87 | 15.61 | 4.524 |
| `rahil_badnet_0_1_local` (10%, stock) | 0 | 8.01 | 74.95 | 30.44 | 2.199 |

Label 0 is the true target. An anomaly index above about 2 counts as flagged.

## Notes

- NC flagged the true target label at every ratio and reduced ASR to about 1%. Its anomaly index does not change monotonically with the poisoning ratio (2.63, 5.27, 4.52 for 10%, 5%, 1%). With one seed per ratio we make no claim about a trend or its cause.
- FT left most of the backdoor in place on `vgg19_bn_cifar` at every ratio (residual ASR 0.69 to 0.92). Its drop was largest at 1%, but that attack also started from a weaker backdoor (0.83).
- On stock `vgg19_bn` at 10%, FT removed most of the backdoor (0.93 to 0.14). We do not know why the two architectures differ and have not tested an explanation.
- Clean accuracy rises after NC partly because its unlearning stage trains for 100 epochs, more than the 30-epoch attack models received.
- FT was run for 30 epochs instead of the default 100, with `ratio` 0.05.
- Results from the two architectures are not combined into one comparison.
- The ASR denominator is not yet confirmed. The backdoor test set has 9,000 images, which is consistent with excluding the 1,000 images whose true label is already the target. This still needs to be checked in the code.

## Fallback trace

`logs/rahil_badnet_0_1_local/`
