# 🔐 Hybrid MD5 + SHA256 Multiple Image Encryption — Summary

## 🧭 Overview
This repository presents a **modified multi-image encryption system** based on **MD5 + SHA-256 hybrid hashing** and **chaotic map scrambling**.  
It enhances security and randomness compared to biological (genetic dogma) models by integrating cryptographic diffusion and chaotic transformations.

Originally inspired by the paper  
> *“Multiple-image encryption algorithm based on genetic central dogma”*,  
this modified implementation replaces the biological model with **hybrid hash-based diffusion**, achieving improved security, performance, and reproducibility.

---

## ⚙️ Quick Setup
```bash
git clone https://github.com/<your-username>/Hybrid_image_encpy.git
cd Hybrid_image_encpy
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Run Commands
### Command-Line Mode
```bash
python main.py
```

### GUI Mode
```bash
python gui_app.py
```

Results are stored in:
```
output_encrypted/    → Encrypted images
output_decrypted/    → Decrypted images
encryption_results.csv
Encryption_Report.pdf
```

---

## 🔐 Encryption Pipeline
1️⃣ Hybrid Key Generation
Concatenate all image data + password
Generate two digests → MD5, SHA-256
Extract chaotic map parameters

2️⃣ 3D Bit-Plane Scrambling
Stack images → 3D cube
Generate sequences from Sine & LASM maps
Scramble cube along X, Y, Z planes

3️⃣ Multi-Layer Hash Diffusion
Layer 1: MD5-based XOR diffusion
Layer 2: SHA-256 additive diffusion
Layer 3: MD5 + SHA-256 hybrid chaining
Rebuild encrypted cube → separate encrypted images

4️⃣ Decryption (Reverse Order)
Reverse hybrid → SHA256 → MD5
Reverse plane scrambling
Recover original images 

---

## 📊 Metrics (Auto-Generated)
| Metric | Ideal Value | Description |
|---------|--------------|-------------|
| Entropy | ≈ 7.99 | Measures randomness |
| NPCR | > 99% | Pixel change rate |
| UACI | ≈ 33% | Average intensity change |
| Correlation | ≈ 0 | Adjacent pixel correlation |

---

## 🧠 Key Advantage
Hybrid cryptographic diffusion ensures **resistance to brute-force and differential attacks**, while maintaining **lossless reversibility**.

---

## 🧠 Research Contribution
  1. Replaces biological “genetic central dogma” model with MD5 + SHA-256 hybrid cryptographic approach
  2. Enhances randomness, entropy, and diffusion quality
  3. Resistant to differential, brute-force, and plaintext attacks
  4. Easily extendable for color images or video frames

---

## 🧩 Future Enhancements

  1. Add AES-256 layer for hybrid symmetric encryption
  2. Integrate GPU-based parallelization (CUDA/OpenCL)
  3. Expand GUI for batch operations and visual metric plots
  4. Implement real-time video encryption pipeline

---

## 📜 License

This project is released under the MIT License.
You are free to use, modify, and distribute with attribution.

---

## 🧩 Author
**Vamshi Krishna**  
💼 Data Engineer | ML & AI Enthusiast  
📧 [vallabudasvamshikrishna28@gmail.com]
📘 GitHub: (https://github.com/vamshikris28)

---
⭐ *Star this repository if you found it helpful!*
