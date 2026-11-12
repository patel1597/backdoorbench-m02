# BadNets CIFAR-10 - 5% Poisoning

## Experiment Configuration
- Dataset: CIFAR-10
- Model: Modified VGG19-BN (vgg19_bn_cifar)
- Attack: BadNets, all-to-one
- Target class: 0 (Airplane)
- Poisoning rate: 5% (2,500 of 50,000 training images)
- Trigger: 3x3 white square in the bottom-right corner
- Epochs: 30
- Batch size: 32
- Learning rate: 0.01
- Random seed: 0

## Final Results
- Clean test accuracy: 88.18%
- Attack success rate: 94.81%
- Robust accuracy: 4.72%
- Final training loss: 0.32986

## Best Recorded Results
- Best clean test accuracy: 88.53%
- Best attack success rate: 96.06%

## Included Files
- config/: Experiment configuration and trigger
- logs/: Training log
- metrics/: Epoch metrics and summary
- plots/: Accuracy and loss plots

## Notes
This lightweight folder does not include the trained checkpoint or
poisoned datasets. Use the corresponding Full folder for those files.
