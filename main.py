from encryption_module import modified_encryption, modified_decryption
from utils.image_utils import load_images, save_images
from utils.performance_metrics import evaluate_performance
import pandas as pd
import numpy as np

if __name__ == "__main__":
    password = "vamshi123"
    
    print("🔹 Loading images...")
    images = load_images("input_images")
    print(f"Loaded {len(images)} images.")
    
    # --- ENCRYPTION ---
    print("\n🚀 Starting Encryption...")
    encrypted_images, keys = modified_encryption(images, password)
    save_images(encrypted_images, "output_encrypted", "encrypted")
    print("✅ Encryption completed. Files saved in 'output_encrypted/'.")
    
    # --- DECRYPTION ---
    print("\n🔓 Starting Decryption...")
    decrypted_images = modified_decryption(encrypted_images, keys)
    save_images(decrypted_images, "output_decrypted", "decrypted")
    print("✅ Decryption completed. Files saved in 'output_decrypted/'.")
    
    # --- PERFORMANCE EVALUATION ---
    print("\n📊 Evaluating Encryption Performance...")
    results = []
    for i in range(len(images)):
        original = np.array(images[i])
        encrypted = np.array(encrypted_images[i])
        metrics = evaluate_performance(original, encrypted)
        metrics["Image"] = f"img{i+1}"
        results.append(metrics)

    df = pd.DataFrame(results)
    print(df)
    df.to_csv("encryption_results.csv", index=False)
    print("✅ Metrics saved to 'encryption_results.csv'")
