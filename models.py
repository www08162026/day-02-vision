"""Models for real concrete crack image classification."""

from __future__ import annotations

import torch
from torch import nn


class SmallCNN(nn.Module):
    """A small two-class network for 3 by 64 by 64 image tensors."""

    def __init__(self) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(3, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(16 * 16 * 16, 2),
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        return self.network(images)
