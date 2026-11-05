# BadNets Attack Results: Modified VGG19-BN

## 1. Experiment Overview

This experiment evaluates the BadNets backdoor attack using the BackdoorBench framework and CIFAR-10 dataset.

The original VGG19-BN architecture struggled to learn CIFAR-10 under the selected training setup. We investigated the issue using clean-only training tests and modified the classifier to better suit the 32x32 CIFAR-10 images.

## 2. Experiment Configuration

- Dataset: CIFAR-10
- Model: Modified VGG19-BN
- Attack: BadNets
- Target class: 0 (Airplane)
- Label transformation: All-to-one
- Poisoning ratio: 10%
- Poisoned training samples: 5,000
- Trigger: 3x3 white square in the bottom-right corner
- Training epochs: 30
- Batch size: 32
- Learning rate: 0.01
- Optimizer: SGD
- Momentum: 0.9
- Weight decay: 0.0005
- Random seed: 0
- Learning rate scheduler: CosineAnnealingLR

## 3. Model Modification

The original VGG19-BN classifier contained approximately 119.6 million parameters and was designed for ImageNet-sized images.

We retained the convolutional feature extractor and made two changes:

1. Replaced the original pooling layer with AdaptiveAvgPool2d((1, 1)).
2. Replaced the original fully connected classifier with a single linear layer (512 inputs, 10 outputs).

The modified classifier contains 5,130 parameters.

This reduced the classifier size while preserving the VGG19-BN convolutional architecture.

## 4. Final Results

| Metric | Result |
|---|---:|
| Clean Accuracy (CA) | 87.37% |
| Attack Success Rate (ASR) | 95.10% |
| Robust Accuracy (RA) | 4.40% |
| Final Training Loss | 0.38235 |

### Best Individual Metrics

- Highest clean accuracy: 87.44% at epoch 24.
- Highest ASR: 97.08% at epoch 21.
- Lowest robust accuracy: 2.72% at epoch 21.

These individual best values occurred at different epochs. The final results above are all from epoch 29.

## 5. Original Model Issue

The original VGG19-BN experiment produced approximately 10% clean accuracy and 100% ASR.

Further investigation showed that the model predicted class 0 for all 10,000 clean test images. This indicated model collapse rather than successful normal classification.

Clean-only tests showed that the original VGG19-BN struggled to learn CIFAR-10, while the modified classifier allowed
reach 83.12% clean test accuracy after 8 epochs.

The modified architecture was then used for the full BadNets experiment.

## 6. Results Interpretation

The modified VGG19-BN achieved 87.37% clean accuracy and 95.10% attack success rate.

This indicates that the model learned normal CIFAR-10 classification while also learning the backdoor trigger association.

The low robust accuracy of 4.40% shows that triggered images were rarely classified according to their original labels.

## 7. Files and Reproducibility

- `config/training_config.yaml`: Training configuration.
- `config/badnet_default.yaml`: BadNets attack settings.
- `config/trigger_image.png`: Trigger image.
- `config/info.pickle`: Experiment metadata.
- `logs/`: Training log.
- `metrics/attack_df.csv`: Epoch-by-epoch metrics.
- `metrics/attack_df_summary.csv`: Summary metrics.
- `plots/`: Training accuracy and loss plots.

The trained model checkpoint and generated poisoned datasets are excluded to keep the repository small.

### Training Command

```bash
python ./attack/badnet.py \
  --yaml_path ./config/attack/prototype/cifar10_vgg19_cifar.yaml \
  --bd_yaml_path ./config/attack/badnet/default.yaml \
  --patch_mask_path ./resource/badnet/trigger_image.png \
  --model vgg19_bn_cifar \
  --pratio 0.1 \
  --epochs 30 \
  --random_seed 0 \
  --save_folder_name badnet_vgg19_cifar_0_1
```
