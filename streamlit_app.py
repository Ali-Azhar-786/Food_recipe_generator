import streamlit as st
import requests
import time

# In your requests.post calls, instead of hardcoding localhost:8000
# Use this (you can even make it configurable later)

BASE_URL = "http://127.0.0.1:8000"

# At the very top of streamlit_app.py
with st.spinner("Starting backend services... please wait 5-10 seconds"):
    import time
    time.sleep(5)  # rough delay - you can make it smarter later

st.set_page_config(
    page_title="Food Recipe & Dish Ideas",
    page_icon="🍳",
    layout="wide"
)

st.title("🍴 Food Recipe & Dish Suggestion Generator")
st.markdown("Upload a photo and let AI tell you what to cook!")

# Mode selection
mode = st.radio(
    "What would you like to do?",
    ["Generate recipe for one dish", "Get dish ideas from ingredients"],
    horizontal=True
)

# File upload
uploaded_file = st.file_uploader(
    "Upload food/ingredients photo",
    type=["jpg", "jpeg", "png"],
    help="Clear, well-lit photo works best"
)

if uploaded_file:
    # Show preview
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(uploaded_file, caption="Uploaded image", use_column_width=True)
    
    if st.button("✨ Process Image", type="primary"):
        with st.spinner("Analyzing image and generating ideas..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                if mode == "Generate recipe for one dish":
                    endpoint = "/api/v1/generate-recipe"
                else:
                    endpoint = "/api/v1/suggest-dishes"
                
                response = requests.post(f"{BASE_URL}{endpoint}", files=files, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("Done!")
                        
                        if mode == "Generate recipe for one dish":
                            st.subheader(f"🍲 {data['detected_food']}")
                            st.markdown(data["recipe"])
                        else:
                            st.subheader("Detected ingredients")
                            st.write(", ".join(data["detected_ingredients"]) or "— nothing detected —")
                            
                            st.subheader("Here are some delicious ideas:")
                            st.markdown(data["suggestions"])
                    else:
                        st.error("Processing completed but result format is invalid")
                else:
                    error_msg = response.json().get("detail", "Unknown error")
                    st.error(f"Server error ({response.status_code}): {error_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend.\n\nPlease make sure FastAPI server is running (`uvicorn main:app --reload`)")
            except requests.exceptions.Timeout:
                st.error("Processing took too long. The model might be busy or the image is complex.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")