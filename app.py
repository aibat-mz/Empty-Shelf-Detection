import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import cv2

st.set_page_config(
    page_title="Empty Shelf Detection",
    layout="centered"
)

st.title("Empty Shelf Detection System")
st.write("Upload a retail shelf image to detect empty shelf regions.")

@st.cache_resource
def load_model():
    model = YOLO("best.pt")
    return model

model = load_model()

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

# Confidence slider
confidence = st.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.25,
    step=0.05
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        image.save(tmp_file.name)
        temp_path = tmp_file.name

    with st.spinner("Running detection..."):
        results = model.predict(
            source=temp_path,
            conf=confidence,
            save=False
        )

    # Convert BGR → RGB so colors stay correct
    result_image = cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB)

    # Better side-by-side layout
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    with col2:
        st.image(
            result_image,
            caption="Detection Result",
            use_container_width=True
        )