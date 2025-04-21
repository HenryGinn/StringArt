import numpy as np
import matplotlib.pyplot as plt

# ----------- OKLab Conversion Functions (from Björn Ottosson's OKLab spec) -----------

def srgb_to_linear(rgb):
    rgb = np.asarray(rgb)
    linear = np.where(
        rgb <= 0.04045,
        rgb / 12.92,
        ((rgb + 0.055) / 1.055) ** 2.4)
    return linear

def linear_to_srgb(rgb):
    rgb = np.asarray(rgb)
    srgb = np.where(
        rgb <= 0.0031308,
        12.92 * rgb,
        1.055 * (rgb ** (1 / 2.4)) - 0.055)
    return srgb

def linear_srgb_to_oklab(rgb):
    # M1 matrix
    lms = np.cbrt(np.dot(
        np.array([
            [0.4122214708, 0.5363325363, 0.0514459929],
            [0.2119034982, 0.6806995451, 0.1073969566],
            [0.0883024619, 0.2817188376, 0.6299787005]
        ]), rgb))
    lms = np.dot(
        np.array([
            [0.2104542553, 0.7936177850, -0.0040720468],
            [1.9779984951, -2.4285922050, 0.4505937099],
            [0.0259040371, 0.7827717662, -0.8086757660]
        ]), lms)
    return lms

def oklab_to_linear_srgb(lab):
    l, a, b = lab
    lms = np.dot(
        np.array([
            [1.0000000, 0.3963378, 0.2158038],
            [1.0000000, -0.1055613, -0.0638542],
            [1.0000000, -0.0894842, -1.2914855]
        ]), [l, a, b])**3
    lms = np.dot(
        np.array([
            [4.0767417, -3.3077116, 0.2309699],
            [-1.2684380, 2.6097574, -0.3413194],
            [-0.0041961, -0.7034186, 1.7076147]
        ]), lms)
    return lms


# ----------- Thread Blending Function -----------

def blend_thread_with_canvas(width=200, thread_rgb=[0.8, 0.2, 0.1], sigma=15.0):
    canvas_rgb = np.ones(3)  # White canvas

    # Convert to linear RGB
    thread_lin = srgb_to_linear(thread_rgb)
    canvas_lin = srgb_to_linear(canvas_rgb)

    # Convert to OKLab
    thread_oklab = linear_srgb_to_oklab(thread_lin)
    canvas_oklab = linear_srgb_to_oklab(canvas_lin)

    # Create distance map (1D array simulating cross-section)
    x = np.linspace(-width // 2, width // 2, width)
    distance = np.abs(x)

    # Gaussian falloff
    intensity = np.exp(-(distance ** 2) / (2 * sigma ** 2))

    # Blend in OKLab
    blended_oklab = np.array([
        thread_oklab * i + canvas_oklab * (1 - i)
        for i in intensity
    ])

    # Convert back to linear RGB
    blended_lin_rgb = np.array([oklab_to_linear_srgb(lab) for lab in blended_oklab])
    
    # Convert to sRGB
    blended_srgb = linear_to_srgb(blended_lin_rgb)
    
    # Clip for display
    blended_srgb = np.clip(blended_srgb, 0, 1)

    return x, blended_srgb

# ----------- Visualization -----------

def show_thread_profile():
    x, colors = blend_thread_with_canvas()
    
    # Display as an image (1-pixel high strip)
    img = np.expand_dims(colors, axis=0)
    
    plt.figure(figsize=(10, 2))
    plt.imshow(img, aspect='auto')
    plt.axis('off')
    plt.title('Thread Intensity Profile Across Canvas')
    plt.show()

show_thread_profile()
