import torch
from datasets import load_dataset
from typing import List

# Load the dataset you want to embed
dataset = load_dataset('dataset_name')

# Define the model ID and authentication token
model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "get your token in http://hf.co/settings/tokens"

# Define the API URL and headers for the Hugging Face pipeline
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

# Define a function to query the Hugging Face pipeline and generate embeddings
def query(texts: List[str]) -> List:
    response = requests.post(api_url, headers=headers, json={"inputs": texts})
    result = response.json()
    if isinstance(result, list):
      return result
    elif list(result.keys())[0] == "error":
      raise RuntimeError(
          "The model is currently loading, please re-run the query."
          )
    
  
def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts})
    result = response.json()
    if isinstance(result, list):
      return result
    elif list(result.keys())[0] == "error":
      raise RuntimeError(
          "The model is currently loading, please re-run the query."
          )

# Generate the embeddings for each item in the dataset
embeddings = []
for item in dataset["train"]:
    text = item["text"]
    embedding = query([text])[0]
    embeddings.append(embedding)

# Convert the embeddings to a Torch tensor
embeddings_tensor = torch.from_numpy(np.array(embeddings)).to(torch.float)

# Save the embeddings to a file that can be loaded later
torch.save(embeddings_tensor, "embeddings.pt")