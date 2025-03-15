import os
from os import environ
import pinecone
import openai
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = 'character-index'
# Connect to the Pinecone index
index = pc.Index(index_name)
print("✅ Pinecone index is ready!")

# ✅ Corrected function for generating OpenAI embeddings
def get_embedding(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Create OpenAI client
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding  # Return the embedding vector

# ✅ Load CSV file (Modify file path if needed)
csv_file = "Spells.csv"
df = pd.read_csv(csv_file, encoding="ISO-8859-1")  # Adjust encoding if needed

# ✅ Convert each row into a string (since your CSV has no "text" column)
df_strings = df.astype(str)  # Convert all values to string
df_strings["combined_text"] = df_strings.apply(lambda row: " | ".join(row.values), axis=1)  # Join all columns

# ✅ Store data in Pinecone
for i, row in tqdm(df_strings.iterrows(), total=len(df_strings)):
    text = row["combined_text"]  # Use the combined row text
    vector = get_embedding(text)  # Generate embedding
    
    # Store in Pinecone (metadata contains original row data)
    index.upsert([(str(i), vector, {"row_data": text})])