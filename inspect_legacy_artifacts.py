import torch
import joblib
import os
import sys

MODELS_DIR = "resources/nfl/models"
DATA_DIR = "resources/data"

def inspect_pytorch_model(path):
    print(f"\n--- Inspecting {os.path.basename(path)} ---")
    try:
        # Load state dict
        state_dict = torch.load(path, map_location=torch.device('cpu'))
        
        # Check if it's a full model or just state_dict
        if isinstance(state_dict, dict):
            print("Type: State Dictionary")
            # Infer input size from the first weight matrix
            first_layer = list(state_dict.keys())[0]
            if 'weight' in first_layer:
                shape = state_dict[first_layer].shape
                print(f"Input Dimension (Inferred): {shape[1]}")
                print(f"First Layer Size: {shape[0]}")
            
            # Infer output from last weight/bias
            last_layer = list(state_dict.keys())[-2] # weight of last layer
            if 'weight' in last_layer:
                shape = state_dict[last_layer].shape
                print(f"Output Dimension: {shape[0]}")
        else:
            print("Type: Full Model Object")
            print(state_dict)

    except Exception as e:
        print(f"Error loading model: {e}")

def inspect_pickle(path):
    print(f"\n--- Inspecting {os.path.basename(path)} ---")
    try:
        data = joblib.load(path)
        if hasattr(data, 'classes_'):
            print(f"Type: LabelEncoder")
            print(f"Classes ({len(data.classes_)}): {data.classes_}")
        elif isinstance(data, dict):
            print(f"Type: Dictionary (Scalers/Encoders)")
            print(f"Keys: {list(data.keys())}")
        else:
            print(f"Type: {type(data)}")
    except Exception as e:
        print(f"Error loading pickle: {e}")

if __name__ == "__main__":
    # Inspect Models
    for f in os.listdir(MODELS_DIR):
        if f.endswith(".pt"):
            inspect_pytorch_model(os.path.join(MODELS_DIR, f))
        elif f.endswith(".pkl"):
            inspect_pickle(os.path.join(MODELS_DIR, f))
            
    # Inspect Data Artifacts if they exist
    if os.path.exists(DATA_DIR):
        for f in os.listdir(DATA_DIR):
            if f.endswith(".pkl"):
                inspect_pickle(os.path.join(DATA_DIR, f))
