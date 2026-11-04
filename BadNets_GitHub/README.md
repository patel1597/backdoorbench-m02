# BadNets Attack Results

## Experiment Overview

This experiment implements the BadNets backdoor attack using
the BackdoorBench framework.

## Configuration

- Dataset: CIFAR-10
- Model: PreAct-ResNet18
- Attack: BadNets
- Target class: 0 (Airplane)
- Label transformation: All-to-one
- Poisoning ratio: 10%
- Poisoned training samples: 5,000
- Trigger: White square
- Training epochs: 10
- Batch size: 32

## Results

| Metric | Result |
|---|---:|
| Clean Accuracy (CA) | 85.02% |
| Attack Success Rate (ASR) | 96.26% |

## Folder Contents

- model/: Trained model checkpoint
- config/: Experiment configuration files
- logs/: Training logs
- metrics/: CSV metric results
- plots/: Training accuracy and loss plots
- metadata/: Experiment metadata and poisoned sample indices

