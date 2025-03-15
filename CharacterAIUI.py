import streamlit as st
import openai
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from VoiceGenerator import text_to_speech

# Load API keys from .env
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "character-index"

# Connect to the existing index
index = pc.Index(index_name)

# Character styles
CHARACTER_STYLES = {
    "Hermione": "Respond in an intelligent and bookish manner, using formal and detailed explanations.",
    "Harry Potter": "Speak like Harry Potter, be courageous, friendly, and straightforward.",
    "Dumbledore": "Respond with wisdom, using metaphorical and deep philosophical advice.",
    "Snape": "Speak in a cold, sarcastic, and strict tone, with precise and sharp language.",
    "Hagrid": "Use a warm, friendly, and rustic tone with occasional slang."
}

# Set up Streamlit UI
st.title("🔮 Chat with a Fictional Character")

character = st.selectbox("Choose a character:", list(CHARACTER_STYLES.keys()))
query = st.text_input("Ask a question:")

client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ Initialize OpenAI client

if st.button("Get Response"):
    if query:
        # Query Pinecone for relevant context
        query_embedding = client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        ).data[0].embedding

        results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

        # Extract context from Pinecone results
        context = "\n".join([match["metadata"].get("row_data", "No relevant text found.") for match in results["matches"]])

        # Define OpenAI prompt
        prompt = f"""
        You are {character} from Harry Potter. {CHARACTER_STYLES[character]}
        Answer the user's question in the style of {character}, using the following context from the books:
        {context}
        User's Question: {query}
        """

        # Get GPT response
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )

        # Display response
        st.markdown(f"**{character} says:** {response.choices[0].message.content}")

        # Extract generated response text
        response_text = response.choices[0].message.content

        # Convert response to speech
        text_to_speech(response_text, character)