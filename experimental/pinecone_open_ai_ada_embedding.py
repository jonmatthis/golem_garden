import os
import openai
from dotenv import load_dotenv
import pinecone
from pinecone import Index
from datasets import load_dataset
from tqdm.auto import tqdm

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Connect to Pinecone index
index_name = 'openai-youtube-transcriptions'
index = pinecone.Index(index_name)

def generate_chat_completions(prompt):
    # Call OpenAI API Chat endpoint
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI language model."},
            {"role": "user", "content": f"{prompt}"}
        ],
        temperature=0.8,
        max_tokens=150
    )

    return chat_response.choices[0].message['content']


def retrieve_and_generate_chat_response(query: str, index: Index, limit: int = 3750, embed_model: str = "text-embedding-ada-002"):
    # Retrieve relevant contexts from Pinecone
    embedding_create_response = openai.Embedding.create(
        input=[query],
        engine=embed_model
    )

    embedding_vector_of_the_query = embedding_create_response['data'][0]['embedding']
    embedded_query_response = index.query(embedding_vector_of_the_query, top_k=3, include_metadata=True)
    contexts = [
        x['metadata']['text'] for x in embedded_query_response['matches']
    ]

    # Build the prompt with the retrieved contexts included
    prompt = "Answer the question based on the context below.\n\nContext:\n "
    for i in range(len(contexts)):
        prompt += f"{contexts[i]}\n---\n"

    prompt += f"Question: {query}"

    # Generate chat completion with the retrieved context
    chat_response = generate_chat_completions(prompt)

    return chat_response.strip()

def main():
    query = "Which training method should I use for sentence transformers when I only have pairs of related sentences?"

    # Retrieve relevant context and generate a chat response
    chat_response = retrieve_and_generate_chat_response(query, index)

    print(f"Query: {query}")
    print(f"Response: {chat_response}")

if __name__ == '__main__':
    main()
