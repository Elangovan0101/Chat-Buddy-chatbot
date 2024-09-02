import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from dotenv import load_dotenv
from PIL import Image
import os
import io

# Load environment variables from .env file
load_dotenv()

# Convert image to byte array
def image_to_byte_array(image: Image) -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

# Set API key from environment variables
API_KEY = os.environ.get("AIzaSyCtpOxrG0XBTl7YwxNKE9p-c0UBZQMmU1w")
genai.configure(api_key="AIzaSyCtpOxrG0XBTl7YwxNKE9p-c0UBZQMmU1w")

# Display logo image
st.image(r"C:\Users\VJ_Mahesh\OneDrive\Desktop\Chat Buddy\GeminiProUnleased\logo.png", width=900)
st.write("")

# Define tabs for different functionalities
gemini_pro, gemini_vision = st.tabs(["Gemini Pro", "Gemini Pro Vision"])

def main():
    with gemini_pro:
        st.header("Interact with Chat buddy")
        st.write("")

        prompt = st.text_input("prompt please...", placeholder="Prompt", label_visibility="visible")
        
        # Updated model to gemini-1.5-flash
        model = genai.GenerativeModel("gemini-1.5-flash")

        if st.button("SEND", use_container_width=True):
            response = model.generate_content(prompt)

            # Check if response contains candidates
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]  # Get the first candidate
                
                # Extract text from the first part if available
                if candidate.content and candidate.content.parts:
                    response_text = candidate.content.parts[0].text
                    st.write("")
                    st.header(":blue[Response]")
                    st.write("")
                    st.markdown(response_text)
                else:
                    st.write(":red[No valid text content found in the response.]")
                    st.write("Debug info: Response parts missing or empty.")
            else:
                st.write(":red[No valid response generated or the response was blocked by safety filters.]")
                st.write("Debug info: Candidates present?", response.candidates)

    with gemini_vision:
        st.header("Interact with Gemini Pro Vision")
        st.write("")

        image_prompt = st.text_input("Interact with the Image", placeholder="Prompt", label_visibility="visible")
        uploaded_file = st.file_uploader("Choose an Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)

        if st.button("GET RESPONSE", use_container_width=True):
            # Use the updated model for vision tasks
            model = genai.GenerativeModel("gemini-1.5-flash")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts=[
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    # Check if response contains candidates
                    if response.candidates and len(response.candidates) > 0:
                        candidate = response.candidates[0]  # Get the first candidate
                        
                        # Extract text from the first part if available
                        if candidate.content and candidate.content.parts:
                            response_text = candidate.content.parts[0].text
                            st.write("")
                            st.write(":blue[Response]")
                            st.write("")
                            st.markdown(response_text)
                        else:
                            st.write(":red[No valid text content found in the response.]")
                            st.write("Debug info: Response parts missing or empty.")
                    else:
                        st.write(":red[No valid response generated or the response was blocked by safety filters.]")
                        st.write("Debug info: Candidates present?", response.candidates)

                else:
                    st.write(":red[Please Provide a prompt]")

            else:
                st.write(":red[Please Provide an image]")

if __name__ == "__main__":
    main()
