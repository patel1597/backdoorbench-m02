# Team M02: Backdoor defenses on BackdoorBench (ECE 424, Midpoint)

Team: Shruthi Shankar (ss4592), Rahil Patel (rnp83), Ahmed Abouelkhir (aa2899)
Topic: *BackdoorBench: A Comprehensive Benchmark of Backdoor Learning* (Wu et al., NeurIPS 2022).
Question: how well do FT and NC defend against BadNets and Blended attacks on CIFAR-10 as the poisoning ratio drops?

## Repo map
| Folder | Owner | Contents |
|---|---|---|
| `BadNets_GitHub/` | Ahmed (aa2899) | BadNets attack run (PreAct-ResNet18, 10 epochs, batch 32): configs, logs, metrics, plots. Has its own README. |
| `logs/` | Rahil (rnp83) | Defense runs (FT, NC) on a VGG19-BN BadNets 10% model. See `logs/README.md`. |
| `[shruthi_folder]/` | Shruthi (ss4592) | [Evaluation scripts and results. To be added.] |

## Item 1: Runnable baseline
Environment used: Google Colab free T4, PyTorch 2.11, Python 3.13. The repo's `install.sh` pins PyTorch 1.11 and was not used.

Setup:
    git clone https://github.com/SCLBD/BackdoorBench.git
    cd BackdoorBench
    git checkout f02e3534645f0ee63d6848653062cd6c0d6c400d
    sh ./sh/init_folders.sh
    pip install kornia pyyaml scikit-learn scikit-image tqdm matplotlib pandas pytorch-wavelets

Three one-line patches are applied on top of that commit for PyTorch 2.11:
1. `utils/save_load_attack.py`: `torch.load(save_path)` becomes `torch.load(save_path, weights_only=False)`
2. `defense/nc.py`: `"--num_workers", type=float` becomes `type=int`
3. `defense/ft.py`: `"--num_workers", type=float` becomes `type=int`

Commands (CIFAR-10 must be in `./data/cifar10`):
    python ./resource/badnet/generate_white_square.py --image_size 32 --square_size 3 --distance_to_right 0 --distance_to_bottom 0 --output_path ./resource/badnet/trigger_image.png
    python ./attack/badnet.py --yaml_path ./config/attack/prototype/cifar10.yaml --patch_mask_path ./resource/badnet/trigger_image.png --model vgg19_bn --pratio 0.1 --epochs 30 --random_seed 0 --num_workers 2 --save_folder_name badnet_0_1
    python ./defense/nc.py --result_file badnet_0_1 --yaml_path ./config/defense/nc/cifar10.yaml --dataset cifar10 --model vgg19_bn --num_workers 2
    python ./defense/ft.py --result_file badnet_0_1 --yaml_path ./config/defense/ft/cifar10.yaml --dataset cifar10 --model vgg19_bn --num_workers 2 --epochs 30

Expected: undefended clean accuracy about 0.86 and ASR about 0.93; after NC, ASR about 0.01; after FT, ASR about 0.14 (single seed).

## Item 2: Trace and sanity check
Details and numbers are in `logs/README.md`.
- Sanity check: a 2-epoch model had ASR of only 7-8%, so the backdoor had not formed. We retrained for 30 epochs (ASR 0.93), and NC flagged label 0, the true target.
- Failures found and fixed: a `weights_only` load error and a `--num_workers` float error in NC and FT.
- **Fallback trace:** `logs/rahil_badnet_0_1_local/`

## Item 3: Bounded-contribution plan
A failure analysis of how FT and NC degrade as the poisoning ratio falls (1%, 5%, 10%), with per-case results reported beside totals. The first data point is at 10%: NC removed the backdoor (ASR 0.93 to 0.01) and FT only partly (0.93 to 0.14). Planned per-case checks: whether NC still flags the target label and how its anomaly index changes (2.2 at 10%), and how FT's residual ASR changes.

## Item 4: Member evidence
| Member | Component | Evidence so far |
|---|---|---|
| Ahmed (aa2899) | Attack pipeline (BadNets, Blended) | `BadNets_GitHub/`: BadNets run, configs, logs. Commit confirmed as `f02e353` from his run log. Blended: [pending] |
| Rahil (rnp83) | Defense pipeline (FT, NC) | `logs/`: FT and NC on BadNets 10%, patches, smoke test |
| Shruthi (ss4592) | Evaluation | [pending] |

## Item 5: Updated protocol
- Matrix: 2 attacks (BadNets, Blended) x 2 defenses (FT, NC) x 3 poisoning ratios (1%, 5%, 10%). Done so far: BadNets 10% with both defenses.
- Seed 0. Metrics: clean accuracy over all test images and ASR before and after each defense.
- ASR denominator: [to be confirmed from the BackdoorBench code before the final report].
- Midpoint runs use the default defense settings, except FT at 30 epochs instead of 100. Defense hyperparameters will be tuned on a validation split for the final runs, followed by a single final test evaluation.

### Deviations from the proposal
- **Model:** the proposal says VGG19. The BackdoorBench paper describes its VGG-19 as without batch norm. We used `vgg19_bn` and will switch to plain `vgg19` if the instructor prefers. These runs would then be a cross-check.
- **Compute:** Colab free T4 instead of personal devices. [Instructor reply pending.]
- **Attack provenance:** the VGG19-BN attack used for the defense runs was trained by Rahil on Colab. Ahmed's BadNets run used PreAct-ResNet18 (10 epochs, batch 32, CA 85.02%, ASR 96.26%) and is kept as a supplementary attack. [Update when Ahmed's VGG19 run exists.]
- Three patches on top of commit `f02e353` (Item 1).
