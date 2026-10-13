#!/usr/bin/env python3
"""
Simple Image Encryption Tool Using Pixel Manipulation
Supports:
  1. XOR Operation (Bitwise math with secret key)
  2. Modulo Addition/Subtraction (Mathematical shift with secret key)
  3. Color Channel Swap (Red <-> Blue channel swap)
  4. Adjacent Pixel Swap (Swapping neighboring pixels)
  5. Combined Operation (Color Channel Swap + XOR Math with secret key)
"""

import os
import sys
import time
import argparse

try:
    from PIL import Image
except ImportError:
    print("\n[!] Error: 'Pillow' is required for image processing.")
    print("    Install it via:  pip install pillow")
    print("    Or if using a virtual environment, activate it first.\n")
    sys.exit(1)


METHODS = {
    "1": ("XOR Math (Bitwise XOR with secret key)", "xor"),
    "2": ("Modular Math (Addition / Subtraction with key)", "modulo"),
    "3": ("Channel Swap (Swap Red & Blue values)", "channel_swap"),
    "4": ("Adjacent Pixel Swap (Swap neighboring pixels)", "pixel_swap"),
    "5": ("Combined (Channel Swap + XOR Key)", "combined")
}


def get_channel_count(mode: str) -> int:
    """Returns number of channels for common image modes."""
    mode_channels = {
        "RGB": 3,
        "RGBA": 4,
        "L": 1,
        "CMYK": 4
    }
    return mode_channels.get(mode, 3)


def manipulate_pixels(raw_bytes: bytearray, mode: str, method: str, key: int, channels: int) -> bytearray:
    """
    Applies pixel manipulation to raw image bytes according to the specified method.

    Parameters:
        raw_bytes (bytearray): Raw image pixel bytes.
        mode (str): 'encrypt' or 'decrypt'.
        method (str): 'xor', 'modulo', 'channel_swap', 'pixel_swap', or 'combined'.
        key (int): Secret key integer.
        channels (int): Number of color channels per pixel (3 for RGB, 4 for RGBA, 1 for L).

    Returns:
        bytearray: Transformed pixel bytes.
    """
    data = bytearray(raw_bytes)
    k = key % 256
    active_channels = min(channels, 3)  # Don't scramble Alpha channel in RGBA

    if method == "xor":
        # XOR is self-inverting: (A ^ K) ^ K = A
        for i in range(0, len(data), channels):
            for c in range(active_channels):
                data[i + c] ^= k

    elif method == "modulo":
        # Modular math: (A + K) % 256 for encrypt, (A - K) % 256 for decrypt
        if mode == "encrypt":
            for i in range(0, len(data), channels):
                for c in range(active_channels):
                    data[i + c] = (data[i + c] + k) % 256
        else:
            for i in range(0, len(data), channels):
                for c in range(active_channels):
                    data[i + c] = (data[i + c] - k) % 256

    elif method == "channel_swap":
        # Swap Red (channel 0) and Blue (channel 2). Self-inverting.
        if channels >= 3:
            for i in range(0, len(data), channels):
                data[i], data[i + 2] = data[i + 2], data[i]

    elif method == "pixel_swap":
        # Swap adjacent pixel pairs. Self-inverting.
        step = channels
        for i in range(0, len(data) - step, step * 2):
            data[i:i + step], data[i + step:i + step * 2] = (
                data[i + step:i + step * 2],
                data[i:i + step],
            )

    elif method == "combined":
        # Encrypt: Channel Swap -> XOR with Key
        # Decrypt: XOR with Key -> Channel Swap
        if mode == "encrypt":
            for i in range(0, len(data), channels):
                if channels >= 3:
                    data[i], data[i + 2] = data[i + 2], data[i]
                for c in range(active_channels):
                    data[i + c] ^= k
        else:
            for i in range(0, len(data), channels):
                for c in range(active_channels):
                    data[i + c] ^= k
                if channels >= 3:
                    data[i], data[i + 2] = data[i + 2], data[i]

    else:
        raise ValueError(f"Unknown manipulation method: {method}")

    return data


def process_image(input_path: str, output_path: str, mode: str, method: str, key: int = 42) -> str:
    """
    Encrypts or decrypts an image using pixel manipulation.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    start_time = time.time()

    # Open image
    with Image.open(input_path) as img:
        img_mode = img.mode
        img_size = img.size

        # Convert palette/binary images to RGB for manipulation
        if img_mode not in ("RGB", "RGBA", "L"):
            img = img.convert("RGB")
            img_mode = "RGB"

        channels = get_channel_count(img_mode)
        raw_bytes = bytearray(img.tobytes())

    # Perform pixel manipulation
    processed_bytes = manipulate_pixels(raw_bytes, mode, method, key, channels)

    # Reconstruct image from modified bytes
    result_img = Image.frombytes(img_mode, img_size, bytes(processed_bytes))

    # Ensure lossless saving: If user didn't specify PNG/BMP, save as PNG to avoid compression artifacts
    base, ext = os.path.splitext(output_path)
    if ext.lower() not in (".png", ".bmp"):
        output_path = f"{base}.png"

    result_img.save(output_path, format="PNG")
    elapsed = time.time() - start_time

    return output_path, img_size, elapsed


def prompt_valid_key() -> int:
    """Prompts the user until a valid integer key is provided."""
    while True:
        try:
            val = input("Enter secret key integer (e.g. 1-255) [default 42]: ").strip()
            if not val:
                return 42
            return int(val)
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def prompt_method() -> str:
    """Prompts the user to select the pixel manipulation method."""
    print("\nSelect Pixel Manipulation Method:")
    for num, (desc, _) in METHODS.items():
        print(f"  [{num}] {desc}")

    while True:
        choice = input("Enter method choice (1-5) [default 1]: ").strip()
        if not choice:
            return "xor"
        if choice in METHODS:
            return METHODS[choice][1]
        print("Invalid choice. Please enter a number between 1 and 5.")


def interactive_menu():
    print("=" * 60)
    print("       PIXEL MANIPULATION IMAGE ENCRYPTION TOOL")
    print("=" * 60)

    while True:
        print("\nChoose an option:")
        print("  [1] ENCRYPT an image")
        print("  [2] DECRYPT an image")
        print("  [3] EXIT")
        choice = input("Enter your choice (1/2/3): ").strip().lower()

        if choice in ["1", "encrypt", "e"]:
            op_mode = "encrypt"
        elif choice in ["2", "decrypt", "d"]:
            op_mode = "decrypt"
        elif choice in ["3", "exit", "q", "quit"]:
            print("\nExiting tool. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please choose 1, 2, or 3.")
            continue

        # Get input image path
        while True:
            img_path = input(f"\nEnter path to image to {op_mode.upper()}: ").strip()
            # Strip quotes if copied from terminal
            img_path = img_path.strip("\"'")
            if os.path.isfile(img_path):
                break
            print(f"[!] File not found: '{img_path}'. Please check the path.")

        # Suggest default output path
        dirname, filename = os.path.split(img_path)
        base, _ = os.path.splitext(filename)
        default_out = os.path.join(dirname, f"{op_mode}ed_{base}.png")

        out_path = input(f"Enter output path [default: {default_out}]: ").strip().strip("\"'")
        if not out_path:
            out_path = default_out

        # Select method and key
        method = prompt_method()
        if method in ("xor", "modulo", "combined"):
            key = prompt_valid_key()
        else:
            key = 0

        print(f"\nProcessing image ({op_mode.upper()} using {method})...")
        try:
            saved_file, size, elapsed = process_image(img_path, out_path, op_mode, method, key)
            print("-" * 60)
            print(f"  Status        : SUCCESS")
            print(f"  Operation     : {op_mode.upper()}")
            print(f"  Method        : {method}")
            print(f"  Resolution    : {size[0]} x {size[1]} pixels")
            print(f"  Time Taken    : {elapsed:.3f} seconds")
            print(f"  Saved Image   : {saved_file}")
            print("-" * 60)
        except Exception as e:
            print(f"\n[!] Error processing image: {e}")

        again = input("\nPerform another operation? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\nExiting tool. Goodbye!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt and decrypt images using pixel manipulation (XOR, Modulo, Swapping)."
    )
    parser.add_argument("-m", "--mode", choices=["encrypt", "decrypt"], help="Operation mode")
    parser.add_argument("-i", "--input", help="Path to input image")
    parser.add_argument("-o", "--output", help="Path to output image")
    parser.add_argument(
        "--method",
        choices=["xor", "modulo", "channel_swap", "pixel_swap", "combined"],
        default="xor",
        help="Manipulation technique (default: xor)"
    )
    parser.add_argument("-k", "--key", type=int, default=42, help="Secret numeric key (default: 42)")

    args = parser.parse_args()

    # If CLI arguments are provided, run directly without interactive menu
    if args.mode and args.input:
        output = args.output
        if not output:
            dirname, filename = os.path.split(args.input)
            base, _ = os.path.splitext(filename)
            output = os.path.join(dirname, f"{args.mode}ed_{base}.png")

        try:
            saved_file, size, elapsed = process_image(args.input, output, args.mode, args.method, args.key)
            print(f"[+] Successfully {args.mode}ed image!")
            print(f"    Output: {saved_file} ({size[0]}x{size[1]}, {elapsed:.3f}s)")
        except Exception as e:
            print(f"[!] Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Otherwise run interactive menu
        interactive_menu()


if __name__ == "__main__":
    main()
