"""
PyTorch Model Architectures for NFL AI Coach
All 5 models: Offensive, Defensive, 4th Down, Win Prob, Personnel
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class OffensivePlayCallerModel(nn.Module):
    """
    Multi-class classification model for offensive play-calling
    Predicts: pass, run, play_action, screen, draw
    """

    def __init__(self, input_dim, num_classes=5, hidden_dims=[128, 64, 32]):
        super(OffensivePlayCallerModel, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.bn1 = nn.BatchNorm1d(hidden_dims[0])
        self.dropout1 = nn.Dropout(0.3)

        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.bn2 = nn.BatchNorm1d(hidden_dims[1])
        self.dropout2 = nn.Dropout(0.2)

        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.bn3 = nn.BatchNorm1d(hidden_dims[2])

        self.fc4 = nn.Linear(hidden_dims[2], num_classes)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)

        x = F.relu(self.bn3(self.fc3(x)))

        x = self.fc4(x)
        return x

    def predict_proba(self, x):
        """Get probabilities for each class"""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits, dim=1)
        return probs


class DefensiveCoordinatorModel(nn.Module):
    """
    Binary classification model for defensive play prediction
    Predicts: pass (1) or run (0)
    """

    def __init__(self, input_dim, hidden_dims=[96, 48, 24]):
        super(DefensiveCoordinatorModel, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.bn1 = nn.BatchNorm1d(hidden_dims[0])
        self.dropout1 = nn.Dropout(0.25)

        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.bn2 = nn.BatchNorm1d(hidden_dims[1])
        self.dropout2 = nn.Dropout(0.15)

        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.bn3 = nn.BatchNorm1d(hidden_dims[2])

        self.fc4 = nn.Linear(hidden_dims[2], 1)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)

        x = F.relu(self.bn3(self.fc3(x)))

        x = self.fc4(x)
        return x

    def predict_proba(self, x):
        """Get probability of pass"""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = torch.sigmoid(logits)
        return probs


class FourthDownDecisionModel(nn.Module):
    """
    Multi-output regression model for 4th down decisions
    Outputs: conversion_prob, fg_success_prob, expected_epa
    """

    def __init__(self, input_dim, hidden_dims=[64, 32, 16]):
        super(FourthDownDecisionModel, self).__init__()

        # Shared layers
        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.bn1 = nn.BatchNorm1d(hidden_dims[0])
        self.dropout1 = nn.Dropout(0.2)

        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.bn2 = nn.BatchNorm1d(hidden_dims[1])

        # Specialized output heads
        self.conversion_head = nn.Linear(hidden_dims[1], 1)  # Probability of conversion
        self.fg_head = nn.Linear(hidden_dims[1], 1)  # Probability of FG success
        self.epa_head = nn.Linear(hidden_dims[1], 1)  # Expected points added

    def forward(self, x):
        # Shared features
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))

        # Multiple outputs
        conversion_prob = torch.sigmoid(self.conversion_head(x))
        fg_prob = torch.sigmoid(self.fg_head(x))
        epa = self.epa_head(x)

        return conversion_prob, fg_prob, epa

    def predict(self, x):
        """Get all predictions"""
        self.eval()
        with torch.no_grad():
            conversion_prob, fg_prob, epa = self.forward(x)
        return {
            'conversion_prob': conversion_prob,
            'fg_success_prob': fg_prob,
            'expected_epa': epa
        }


class WinProbabilityModel(nn.Module):
    """
    Binary classification model for win probability
    Predicts: probability that possession team wins
    """

    def __init__(self, input_dim, hidden_dims=[128, 64, 32, 16]):
        super(WinProbabilityModel, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.bn1 = nn.BatchNorm1d(hidden_dims[0])
        self.dropout1 = nn.Dropout(0.3)

        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.bn2 = nn.BatchNorm1d(hidden_dims[1])
        self.dropout2 = nn.Dropout(0.2)

        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.bn3 = nn.BatchNorm1d(hidden_dims[2])
        self.dropout3 = nn.Dropout(0.1)

        self.fc4 = nn.Linear(hidden_dims[2], hidden_dims[3])
        self.bn4 = nn.BatchNorm1d(hidden_dims[3])

        self.fc5 = nn.Linear(hidden_dims[3], 1)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)

        x = F.relu(self.bn3(self.fc3(x)))
        x = self.dropout3(x)

        x = F.relu(self.bn4(self.fc4(x)))

        x = self.fc5(x)
        return x

    def predict_proba(self, x):
        """Get win probability"""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = torch.sigmoid(logits)
        return probs


class PersonnelOptimizerModel(nn.Module):
    """
    Multi-class classification model for personnel grouping
    Predicts optimal personnel package: 11, 12, 21, 13, 22, etc.
    """

    def __init__(self, input_dim, num_personnel_groups=6, hidden_dims=[96, 48, 24]):
        super(PersonnelOptimizerModel, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.bn1 = nn.BatchNorm1d(hidden_dims[0])
        self.dropout1 = nn.Dropout(0.25)

        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.bn2 = nn.BatchNorm1d(hidden_dims[1])
        self.dropout2 = nn.Dropout(0.15)

        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.bn3 = nn.BatchNorm1d(hidden_dims[2])

        self.fc4 = nn.Linear(hidden_dims[2], num_personnel_groups)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)

        x = F.relu(self.bn3(self.fc3(x)))

        x = self.fc4(x)
        return x

    def predict_proba(self, x):
        """Get probabilities for each personnel group"""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits, dim=1)
        return probs


# Model factory for easy instantiation
def create_model(model_type, input_dim, **kwargs):
    """
    Factory function to create models

    Args:
        model_type: One of ['offensive', 'defensive', 'fourth_down', 'win_prob', 'personnel']
        input_dim: Number of input features
        **kwargs: Additional model-specific parameters

    Returns:
        PyTorch model instance
    """
    models = {
        'offensive': OffensivePlayCallerModel,
        'defensive': DefensiveCoordinatorModel,
        'fourth_down': FourthDownDecisionModel,
        'win_prob': WinProbabilityModel,
        'personnel': PersonnelOptimizerModel
    }

    if model_type not in models:
        raise ValueError(f"Unknown model type: {model_type}. Choose from {list(models.keys())}")

    return models[model_type](input_dim, **kwargs)


if __name__ == "__main__":
    # Test model creation
    print("Testing model architectures...")

    # Test offensive model
    off_model = create_model('offensive', input_dim=12, num_classes=5)
    test_input = torch.randn(32, 12)  # Batch of 32
    output = off_model(test_input)
    print(f"Offensive model output shape: {output.shape}")  # Should be [32, 5]

    # Test defensive model
    def_model = create_model('defensive', input_dim=11)
    output = def_model(test_input[:, :11])
    print(f"Defensive model output shape: {output.shape}")  # Should be [32, 1]

    # Test 4th down model
    fourth_model = create_model('fourth_down', input_dim=6)
    conv_prob, fg_prob, epa = fourth_model(test_input[:, :6])
    print(f"4th down model outputs: {conv_prob.shape}, {fg_prob.shape}, {epa.shape}")

    # Test win prob model
    wp_model = create_model('win_prob', input_dim=8)
    output = wp_model(test_input[:, :8])
    print(f"Win prob model output shape: {output.shape}")  # Should be [32, 1]

    # Test personnel model
    pers_model = create_model('personnel', input_dim=6, num_personnel_groups=6)
    output = pers_model(test_input[:, :6])
    print(f"Personnel model output shape: {output.shape}")  # Should be [32, 6]

    print("\nAll models created successfully!")
