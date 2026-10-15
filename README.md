# PRODIGY_CS_02

# 🔐 Pixel Manipulation for Image Encryption

A Python-based image encryption and decryption tool that uses **pixel manipulation techniques** to transform image data. The application supports five different methods, including XOR operations, modular arithmetic, color channel swapping, adjacent pixel swapping, and a combination of techniques.

The project demonstrates fundamental concepts of image processing, data transformation, and introductory cryptography through an interactive command-line interface (CLI).

## ✨ Features

- 🔒 **Image Encryption:** Transform image pixel values using different manipulation methods.
- 🔓 **Image Decryption:** Reverse supported transformations to restore the original image.
- 🔢 **XOR Operation:** Apply bitwise XOR using a numeric secret key.
- ➕ **Modular Arithmetic:** Encrypt and decrypt pixel values using modular addition and subtraction.
- 🎨 **Color Channel Swap:** Swap red and blue color channels.
- 🔄 **Adjacent Pixel Swap:** Exchange neighboring pixels.
- ⚡ **Combined Method:** Combine color channel swapping with XOR manipulation.
- 🖼️ **Image Processing:** Process RGB, RGBA, and grayscale images.
- 💻 **Dual Usage:** Use an interactive menu or command-line arguments.
- ⏱️ **Processing Information:** Display image resolution, operation status, and elapsed time.
- 💾 **Lossless Output:** Save processed images as PNG to avoid lossy compression artifacts.

## 🛠️ Technologies Used

- **Language:** Python 3
- **Image Processing:** Pillow
- **Core Concepts:** Pixel manipulation, bitwise operations, modular arithmetic
- **Interface:** Command-Line Interface (CLI)

## 📂 Project Structure

```text
pixel-manipulation-image-encryption/
├── image_encryption.py
└── README.md
```

> **Note:** Replace `image_encryption.py` with the actual filename of your Python script if it is different.

## ⚙️ Installation

### 1. Install Python

Make sure Python 3 is installed.

Check your version:

```bash
python3 --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/pixel-manipulation-image-encryption.git
```

Navigate to the project folder:

```bash
cd pixel-manipulation-image-encryption
```

### 3. Install Dependencies

Install Pillow, the Python imaging library:

```bash
python3 -m pip install Pillow
```

Alternatively, create and activate a virtual environment.

**Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install Pillow
```

## ▶️ How to Run

### Interactive Mode

Start the program without command-line arguments:

```bash
python3 image_encryption.py
```

The application displays a menu:

```text
============================================================
       PIXEL MANIPULATION IMAGE ENCRYPTION TOOL
============================================================

Choose an option:
  [1] ENCRYPT an image
  [2] DECRYPT an image
  [3] EXIT
```

Choose an operation, provide the image path, select a manipulation method, and enter a numeric key when required.

### Available Manipulation Methods

| Option | Method | Description |
|---|---|---|
| 1 | XOR | Applies bitwise XOR to pixel color values using a key. |
| 2 | Modulo | Uses modular addition for encryption and subtraction for decryption. |
| 3 | Channel Swap | Swaps red and blue color values. |
| 4 | Pixel Swap | Swaps neighboring pixel pairs. |
| 5 | Combined | Performs channel swapping and XOR manipulation. |

## 💻 Command-Line Usage

The program also supports direct execution with command-line arguments.

### Command Syntax

```bash
python3 image_encryption.py \
  --mode encrypt \
  --input input.png \
  --output encrypted_image.png \
  --method xor \
  --key 42
```

### Available Arguments

| Argument | Description | Default |
|---|---|---|
| `-m`, `--mode` | Operation: `encrypt` or `decrypt` | Interactive mode if omitted |
| `-i`, `--input` | Input image path | None |
| `-o`, `--output` | Output image path | Generated automatically |
| `--method` | Pixel manipulation method | `xor` |
| `-k`, `--key` | Numeric key | `42` |

### Supported Methods

```text
xor
modulo
channel_swap
pixel_swap
combined
```

## 🔒 Example: Encrypt an Image

```bash
python3 image_encryption.py \
  --mode encrypt \
  --input photo.png \
  --output encrypted_photo.png \
  --method xor \
  --key 42
```

Example output:

```text
[+] Successfully encrypted image!
    Output: encrypted_photo.png (1920x1080, 0.350s)
```

*The resolution and processing time shown above are illustrative examples.*

## 🔓 Example: Decrypt an Image

Use the same method and key used for encryption:

```bash
python3 image_encryption.py \
  --mode decrypt \
  --input encrypted_photo.png \
  --output decrypted_photo.png \
  --method xor \
  --key 42
```

For reversible transformations, the decrypted image should reproduce the original pixel values, provided the image was not altered and the correct method and key are used.

## 🧠 How It Works

### 1. XOR Manipulation

Each selected pixel channel is XORed with a key reduced to a byte value.

```text
Encrypted = Original XOR Key
Decrypted = Encrypted XOR Key
```

XOR is self-inverting, so applying the same operation with the same key restores the original channel value.

### 2. Modular Arithmetic

Pixel values range from 0 to 255.

Encryption:

```text
Encrypted = (Original + Key) mod 256
```

Decryption:

```text
Original = (Encrypted - Key) mod 256
```

### 3. Color Channel Swap

The red and blue channel values are exchanged for each pixel.

This transformation is reversible by swapping the same channels again.

### 4. Adjacent Pixel Swap

Neighboring pixel data blocks are exchanged. Applying the same pairwise swap again restores their original order.

### 5. Combined Method

The combined method performs the following operations:

**Encryption:**
1. Swap the red and blue channels.
2. Apply XOR using the numeric key.

**Decryption:**
1. Apply XOR using the same key.
2. Swap the red and blue channels back.

## 🖼️ Supported Image Formats

The program uses Pillow to open images and supports image modes such as:

- RGB
- RGBA
- Grayscale (L)

Images in other modes are converted to RGB before processing.

The output is saved as PNG. If the specified output filename does not end in `.png` or `.bmp`, the program changes the extension to `.png`.

For best results, use PNG input images and retain the original file for comparison.

## 🔐 Security Considerations

**Important:** This project is intended for educational purposes and is not a secure modern image-encryption system.

- XOR with a single-byte key does not provide strong cryptographic protection.
- Modular arithmetic and channel swapping are reversible transformations, not secure encryption on their own.
- Combining simple transformations does not make them equivalent to modern authenticated encryption.
- The numeric key is not a cryptographically secure key-management system.
- The tool does not provide authentication or tamper detection.

For real-world protection of sensitive images, use a vetted cryptographic library and authenticated encryption such as AES-GCM, with secure key generation and nonce management.

## 🎯 Learning Objectives

This project demonstrates:

- Basic image processing with Pillow.
- RGB and RGBA pixel representations.
- Byte-level data manipulation.
- Bitwise XOR operations.
- Modular arithmetic.
- Reversible transformations.
- Python functions, loops, and exception handling.
- Command-line argument parsing with `argparse`.
- File handling and error management.

## 🚀 Future Improvements

- [ ] Add a graphical user interface.
- [ ] Implement secure encryption using AES-GCM.
- [ ] Add automated unit tests.
- [ ] Support batch processing of multiple images.
- [ ] Add before-and-after image previews.
- [ ] Improve key management and validation.
- [ ] Generate image integrity checksums.
- [ ] Add progress reporting for large images.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork this repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request.
⭐ If you find this project useful, consider giving the repository a star!
