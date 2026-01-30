import google.generativeai as genai
import os

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyA4oWqRuC_VL_R_niTYYeJ5Xmi1Y19SAWw")
genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for model in genai.list_models():
        print(f"Model name: {model.name}")
        print(f"  - Supported operations: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"Error listing models: {e}")

print("\nTrying to create a model instance with different names...")

# Try common model names
common_names = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-pro-vision",
    "text-embedding-004",
    "embedding-001"
]

for name in common_names:
    try:
        model = genai.GenerativeModel(name)
        print(f"✓ Successfully created model: {name}")
    except Exception as e:
        print(f"✗ Failed to create model {name}: {e}")