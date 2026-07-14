import streamlit as st
import ollama
from PIL import Image
from pypdf import PdfReader
import io

# App Configurations
st.set_page_config(page_title="Local AI Medical Assistant", layout="wide")
st.title("🩺 Local AI Medical Assistant (Offline & Private)")
st.caption("Powered by Streamlit & Ollama — your data stays strictly on this machine.")

# Disclaimer Block
st.warning(
    "⚠️ **Disclaimer:** This tool is for **informational and educational purposes only**. "
    "It is running a local AI model and does not constitute professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider regarding any medical condition."
)

# Configuration Sidebar
with st.sidebar:
    st.header("Settings")
    # You can change this to any vision model you have pulled in Ollama
    model_choice = st.selectbox(
        "Select Local Model",
        ["llama3.2-vision", "moondream", "gemma3"]
    )
    st.info("Make sure you run `ollama pull <model-name>` in your terminal first!")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your medical report (PDF, PNG, or JPG)", 
    type=["pdf", "png", "jpg", "jpeg"]
)

# Extract text from PDFs
def extract_text_from_pdf(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

if uploaded_file is not None:
    st.success("📄 File uploaded successfully!")
    
    file_type = uploaded_file.type
    
    # Define the system instructions for the report analysis
    medical_prompt = (
        "You are an empathetic, highly accurate, and helpful medical communication assistant. "
        "Your task is to review the provided medical document "
        "and explain it clearly to a patient without medical training. "
        "Adhere to the following structural output format:\n\n"
        "### 1. Simple Summary\n"
        "Provide a high-level 2-3 sentence overview of what this test/report was evaluating and the main takeaway.\n\n"
        "### 2. Key Terms Explained\n"
        "List 3 to 5 complex medical terms found in the report and define them in everyday, simple language.\n\n"
        "### 3. Understanding the Findings\n"
        "Break down the values, numbers, or observations. Let the user know if things appear within standard reference ranges. "
        "Avoid diagnosing; frame observations carefully.\n\n"
        "### 4. Questions to Ask Your Doctor\n"
        "Provide a list of 3 actionable, specific questions the patient should bring to their follow-up appointment."
    )

    images_payload = []
    text_content = ""

    # Process PDF vs Image
    if "pdf" in file_type:
        with st.spinner("Extracting text from PDF..."):
            text_content = extract_text_from_pdf(uploaded_file)
            with st.expander("Show Extracted Raw Text Preview"):
                st.text(text_content[:1000] + "..." if len(text_content) > 1000 else text_content)
    else:
        # It's an image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Report Image Preview", width=400)
        
        # Convert image to bytes for the Ollama API
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format if image.format else 'PNG')
        images_payload = [img_byte_arr.getvalue()]

    if st.button("Generate Easy-to-Understand Summary", type="primary"):
        with st.spinner(f"Analyzing locally with {model_choice}..."):
            try:
                # Prepare message structure for Ollama
                message = {
                    'role': 'user',
                    'content': f"{medical_prompt}\n\n[Medical Document Text]:\n{text_content}" if text_content else medical_prompt
                }
                
                # Attach images if it's an image file
                if images_payload:
                    message['images'] = images_payload

                # Run local inference
                response = ollama.chat(
                    model=model_choice,
                    messages=[message]
                )
                
                st.markdown("---")
                st.subheader("📋 Patient-Friendly Report Breakdown (Fully Local)")
                st.write(response['message']['content'])
                
            except Exception as e:
                st.error(f"Failed to communicate with local Ollama. Is Ollama running? Error: {e}")