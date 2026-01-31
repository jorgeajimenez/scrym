"""
Test Script for All 5 NFL AI Coach Models
Validates that models load correctly and make predictions
"""

import torch
import numpy as np
import joblib
from pathlib import Path
from models import create_model

# Paths
MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

def test_model_exists(model_name):
    """Check if model file exists"""
    model_path = MODEL_DIR / f"{model_name}.pt"
    exists = model_path.exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {model_name}.pt {'exists' if exists else 'MISSING'}")
    return exists

def test_model_load_and_predict(model_type, model_name, input_dim, **kwargs):
    """Test model loading and prediction"""
    try:
        # Create model architecture
        model = create_model(model_type, input_dim=input_dim, **kwargs)

        # Load weights
        model_path = MODEL_DIR / f"{model_name}.pt"
        model.load_state_dict(torch.load(model_path, map_location='cpu', weights_only=True))
        model.eval()

        # Test prediction with dummy data
        dummy_input = torch.randn(1, input_dim)
        with torch.no_grad():
            output = model(dummy_input)

        print(f"  ✓ {model_name} loaded and tested successfully")
        print(f"    Input shape: {dummy_input.shape}, Output shape: {output.shape if isinstance(output, torch.Tensor) else [o.shape for o in output]}")
        return True

    except Exception as e:
        print(f"  ✗ {model_name} FAILED: {str(e)}")
        return False

def test_scalers_and_encoders():
    """Test that scalers and encoders exist"""
    print("\nTesting Scalers and Encoders:")

    scalers_path = DATA_DIR / "scalers.pkl"
    encoders_path = DATA_DIR / "encoders.pkl"

    if scalers_path.exists():
        scalers = joblib.load(scalers_path)
        print(f"  ✓ Scalers loaded: {list(scalers.keys())}")
    else:
        print(f"  ✗ Scalers MISSING")
        return False

    if encoders_path.exists():
        encoders = joblib.load(encoders_path)
        print(f"  ✓ Encoders loaded: {list(encoders.keys())}")
    else:
        print(f"  ✗ Encoders MISSING")
        return False

    # Test label encoders
    off_encoder_path = MODEL_DIR / "offensive_label_encoder.pkl"
    pers_encoder_path = MODEL_DIR / "personnel_label_encoder.pkl"

    if off_encoder_path.exists():
        off_encoder = joblib.load(off_encoder_path)
        print(f"  ✓ Offensive label encoder: {off_encoder.classes_}")
    else:
        print(f"  ✗ Offensive label encoder MISSING")

    if pers_encoder_path.exists():
        pers_encoder = joblib.load(pers_encoder_path)
        print(f"  ✓ Personnel label encoder: {pers_encoder.classes_}")
    else:
        print(f"  ✗ Personnel label encoder MISSING")

    return True

def test_data_files():
    """Test that data files exist"""
    print("\nTesting Data Files:")

    data_files = [
        "pbp_2018_2024.parquet",
        "ftn_2022_2024.parquet",
        "rosters_2022_2024.parquet"
    ]

    all_exist = True
    for filename in data_files:
        filepath = DATA_DIR / filename
        exists = filepath.exists()
        status = "✓" if exists else "✗"

        if exists:
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"  {status} {filename} ({size_mb:.1f} MB)")
        else:
            print(f"  {status} {filename} MISSING")
            all_exist = False

    return all_exist

def main():
    """Run all tests"""
    print("=" * 70)
    print("NFL AI COACH - MODEL TESTING SUITE")
    print("=" * 70)

    # Test 1: Check model files exist
    print("\n1. Checking Model Files:")
    models_exist = [
        test_model_exists("offensive_model"),
        test_model_exists("defensive_model"),
        test_model_exists("fourth_down_model"),
        test_model_exists("win_prob_model"),
        test_model_exists("personnel_model")
    ]

    # Test 2: Load and test each model
    print("\n2. Testing Model Loading and Inference:")

    tests_passed = []

    # Load label encoders to get actual class counts
    off_encoder_path = MODEL_DIR / "offensive_label_encoder.pkl"
    pers_encoder_path = MODEL_DIR / "personnel_label_encoder.pkl"

    offensive_num_classes = 5  # default
    personnel_num_groups = 6   # default

    if off_encoder_path.exists():
        off_encoder = joblib.load(off_encoder_path)
        offensive_num_classes = len(off_encoder.classes_)

    if pers_encoder_path.exists():
        pers_encoder = joblib.load(pers_encoder_path)
        personnel_num_groups = len(pers_encoder.classes_)

    # Offensive Model (12 features, dynamic classes)
    tests_passed.append(
        test_model_load_and_predict('offensive', 'offensive_model',
                                     input_dim=12, num_classes=offensive_num_classes)
    )

    # Defensive Model (11 features, binary)
    tests_passed.append(
        test_model_load_and_predict('defensive', 'defensive_model',
                                     input_dim=11)
    )

    # 4th Down Model (6 features, multi-output)
    tests_passed.append(
        test_model_load_and_predict('fourth_down', 'fourth_down_model',
                                     input_dim=6)
    )

    # Win Probability Model (8 features, binary)
    tests_passed.append(
        test_model_load_and_predict('win_prob', 'win_prob_model',
                                     input_dim=8)
    )

    # Personnel Model (6 features, dynamic personnel groups)
    tests_passed.append(
        test_model_load_and_predict('personnel', 'personnel_model',
                                     input_dim=6, num_personnel_groups=personnel_num_groups)
    )

    # Test 3: Check data files
    data_exists = test_data_files()

    # Test 4: Check scalers and encoders
    scalers_exist = test_scalers_and_encoders()

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Model files exist: {sum(models_exist)}/5")
    print(f"Models load correctly: {sum(tests_passed)}/5")
    print(f"Data files exist: {'✓' if data_exists else '✗'}")
    print(f"Scalers/Encoders exist: {'✓' if scalers_exist else '✗'}")

    all_passed = (sum(models_exist) == 5 and sum(tests_passed) == 5
                  and data_exists and scalers_exist)

    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Models are ready for inference.")
    else:
        print("\n⚠️  SOME TESTS FAILED. Review errors above.")
        print("\nTo fix:")
        print("  - Run 'python train.py' to train models")
        print("  - Run 'python data_loader.py' to download data")

    print("=" * 70)

if __name__ == "__main__":
    main()
