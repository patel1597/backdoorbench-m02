# BadNets Modified VGG19-BN CIFAR-10: 1% Poisoning

## Overview
This experiment evaluates a BadNets backdoor attack on CIFAR-10 using a modified VGG19-BN architecture.

## Experiment Settings
- Dataset: CIFAR-10
- Model: vgg19_bn_cifar
- Attack: BadNets
- Poisoning rate: 1%
- Poisoned training images: 500
- Target class: 0 (Airplane)
- Trigger: 3x3 white square in the bottom-right corner
- Poisoning strategy: all-to-one
- Epochs: 30
- Batch size: 32
- Learning rate: 0.01
- Random seed: 0

## Final Results
Metrics from the final training epoch (epoch 29):

- Clean Accuracy (CA): 87.59%
- Attack Success Rate (ASR): 82.99%
- Robust Accuracy (RA): 15.49%
- Final training loss: 0.27635

The maximum clean accuracy reported was 88.19%, and the maximum ASR reported was 87.87%. These are separate maximum values.

## Model Architecture
The standard VGG19-BN classifier was adapted for CIFAR-10 using adaptive average pooling and a single linear classification layer.

The custom model definition is included in the full package under:
`utils/aggregate_block/model_trainer_generate.py`

## Folder Contents
- `config/`: Training configuration, BadNets configuration, trigger image, and experiment metadata.
- `logs/`: Training log.
- `metrics/`: Per-epoch metrics and summary CSV files.
- `plots/`: Accuracy and loss plots.

## Reproducibility
This lightweight package contains the experiment configurations and results but does not include the model checkpoint or dataset files.

To reproduce or evaluate the experiment, use a compatible BackdoorBench checkout, the included custom model definition, and the CIFAR-10 dataset.

The full package contains the checkpoint and poisoned datasets.
