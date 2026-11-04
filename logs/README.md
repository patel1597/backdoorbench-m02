# Rahil Patel (rnp83): Defense pipeline (FT, NC) on BadNets 10%

## Configuration
- BackdoorBench commit `f02e3534645f0ee63d6848653062cd6c0d6c400d`, plus three patches for PyTorch 2.11:
  - `utils/save_load_attack.py`: `torch.load(..., weights_only=False)`
  - `defense/nc.py`: `--num_workers` type float to int
  - `defense/ft.py`: `--num_workers` type float to int
- Dataset CIFAR-10, attack BadNets (3x3 white square, target label 0), poisoning ratio 10%, seed 0
- Model: `vgg19_bn` (VGG19 with batch norm). The proposal says VGG19, and the BackdoorBench paper describes its VGG-19 as without batch norm. We used `vgg19_bn`, the variant we had working for the midpoint, and will switch to plain `vgg19` if the instructor prefers. These runs would then be kept as a cross-check.
- Attack: 30 epochs, trained by Rahil on Colab (free T4). Ahmed's separate run used PreAct-ResNet18 (see `BadNets_GitHub/`).
- FT: 30 epochs (default is 100), `ratio` 0.05. NC: default config.
- Environment: Colab free T4, PyTorch 2.11, Python 3.13.

## Results (single seed, single poisoning ratio: baseline only)
| Stage | Clean accuracy | ASR |
|---|---|---|
| Undefended attack | 0.8629 | 0.9286 |
| After NC | 0.8824 | 0.0098 |
| After FT | 0.8749 | 0.1424 |

NC detection: flagged label 0 (mask norm 8.01; median 74.9, MAD 30.4, anomaly index 2.199, just above the usual threshold of 2).

## Folders
- `test_badnet_0_1/`: 2-epoch smoke test. The backdoor never formed (ASR 7-8%), so it checks the pipeline only. This is why we retrained.
- `rahil_badnet_0_1_local/`: 30-epoch baseline with `defense/nc/` and `defense/ft/`.

## Sanity check and fallback trace
- Check: after 2 epochs ASR was 7-8% (no backdoor). After 30 epochs ASR was 0.93, and NC flagged label 0, the true target.
- Failures found and fixed: `weights_only` load error, and `--num_workers` float error in NC and FT.
- **Fallback trace:** `logs/rahil_badnet_0_1_local/`

## Not yet verified
- The ASR denominator. Check in the BackdoorBench code whether it excludes target-class test images, then state it here.
