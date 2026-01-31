"""
PyTorch Model Architectures for the 4th Down Bot
Multi-output 4th Down Engine and Deep Win Probability Calculator.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class FourthDownDecisionModel(nn.Module):
    """
    Multi-output regression/classification model.
    Outputs:
    - conversion_prob (sigmoid)
    - fg_success_prob (sigmoid)
    - expected_epa (linear)
    """
    def __init__(self, input_dim):
        super(FourthDownDecisionModel, self).__init__()
        
        # Shared Layers
        self.shared = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU()
        )
        
        # Output Heads
        self.conversion_head = nn.Linear(32, 1)
        self.fg_head = nn.Linear(32, 1)
        self.epa_head = nn.Linear(32, 1)

    def forward(self, x):
        features = self.shared(x)
        
        conv_prob = torch.sigmoid(self.conversion_head(features))
        fg_prob = torch.sigmoid(self.fg_head(features))
        epa = self.epa_head(features)
        
        return conv_prob, fg_prob, epa

class WinProbabilityModel(nn.Module):
    """
    Deep 5-layer classification network for real-time Win Probability.
    """
    def __init__(self, input_dim):
        super(WinProbabilityModel, self).__init__()
        
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.1),
            
            nn.Linear(32, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return torch.sigmoid(self.net(x))

class OffensivePlayCallerModel(nn.Module):
    """
    Multi-class classification for Offensive Play Calling.
    Predicts: Pass, Run, Play Action, Screen, Draw (5 classes)
    """
    def __init__(self, input_dim, num_classes=5):
        super(OffensivePlayCallerModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        return self.net(x) # Returns logits

class DefensiveCoordinatorModel(nn.Module):
    """
    Binary classification for Defensive Prediction.
    Predicts: Pass (1) or Run (0)
    """
    def __init__(self, input_dim):
        super(DefensiveCoordinatorModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 96),
            nn.BatchNorm1d(96),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(96, 48),
            nn.BatchNorm1d(48),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(48, 24),
            nn.BatchNorm1d(24),
            nn.ReLU(),
            nn.Linear(24, 1)
        )

    def forward(self, x):
        return torch.sigmoid(self.net(x))

class PersonnelOptimizerModel(nn.Module):
    """
    Multi-class classification for Personnel Grouping.
    Predicts: 11, 12, 21, 13, 22, etc. (mapped to indices)
    """
    def __init__(self, input_dim, num_classes):
        super(PersonnelOptimizerModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 96),
            nn.BatchNorm1d(96),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(96, 48),
            nn.BatchNorm1d(48),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(48, 24),
            nn.BatchNorm1d(24),
            nn.ReLU(),
            nn.Linear(24, num_classes)
        )

    def forward(self, x):
        return self.net(x) # Returns logits

def save_model(model, path):
    torch.save(model.state_dict(), path)
    print(f"Model saved to {path}")

def load_model(model, path):
    model.load_state_dict(torch.load(path))
    model.eval()
    return model
