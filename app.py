import gradio as gr
import numpy as np
import cv2
from tensorflow.keras.models import load_model

# ----------------------
# Load trained model
# ----------------------
model = load_model("cnn_model.h5")

# Example class labels (update according to your dataset)
class_labels = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']

# ----------------------
# Preprocessing + Prediction
# ----------------------
def predict_image(img):
    # Convert to numpy array (Gradio gives PIL Image)
    img = np.array(img)

    # If grayscale → convert to RGB
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Resize to model input
    img = cv2.resize(img, (150,150))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    prediction = model.predict(img)
    class_idx = np.argmax(prediction)
    confidence = np.max(prediction)

    return f"Predicted: {class_labels[class_idx]} (Confidence: {confidence:.2f})"

# ----------------------
# Gradio App
# ----------------------
demo = gr.Interface(
    fn=predict_image,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="CNN Image Classifier",
    description="Upload an image (color or grayscale) and the CNN will predict its class."
)

demo.launch(share=True)
