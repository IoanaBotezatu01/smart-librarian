# Running the Project

1. **Clone the Repository**
    ```bash
    git clone [https://github.com/IoanaBotezatu01/smart-librarian](https://github.com/IoanaBotezatu01/smart-librarian)
    cd smart-librarian
    ```

2. **Install Dependencies**
   pip install -r requirements.txt


3. **Configure Environment Variables**
    - set .env with the OpenAI API Key
    CHAT_MODEL=gpt-4o-mini
    EMBED_MODEL=text-embedding-3-small

    ENABLE_TTS=true
    ENABLE_IMAGE=true

4. **Start the Application**
   streamlit run app_streamlit.py


5. **Access the Application**
    - Open your browser and go to `http://localhost:8501`

