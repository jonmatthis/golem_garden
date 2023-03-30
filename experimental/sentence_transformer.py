import torch
from datasets import load_dataset
from typing import List
import requests
import numpy as np
from dotenv import load_dotenv
import os


class SentenceTransformer:
    def __init__(self, 
                 dataset_name: str, 
                 model_id: str =  "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the SentenceTransformer.

        Args:
            dataset_name (str): The name of the dataset to load.
            model_id (str): The model ID to use for inference.
            hf_token (str): The HuggingFace API token.
        """
        self.dataset = load_dataset(dataset_name)
        self.model_id = model_id
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        
        load_dotenv()
        hf_token = os.getenv("HUGGING_FACE_TOKEN")
        self.headers = {"Authorization": f"Bearer {hf_token}"}
        self.query_response = []
    
    @retry(tries=3, delay=10)
    def query_api(self, knowledge_corpus_strings: List[str]) -> List:
        """
        Perform a query extracting embeddings from given list of strings.

        Args:
            knowledge_corpus_strings (List[str]): The input texts we're creating embeddings for.

        Returns:
            List: The extracted embeddings.
        """
        response = requests.post(self.api_url,
                                headers=self.headers,
                                json={"inputs": knowledge_corpus_strings})
        result = response.json()
        if isinstance(result, list):
            return result
        elif list(result.keys())[0] == "error":
            raise RuntimeError(
                "The model is currently loading, please re-run the query."
            )

    def generate_embeddings(self):
        """
        Generate embeddings for the dataset.
        """
        embeddings = []
        for item in self.dataset["train"]:
            text = item["text"]
            embedding = self.query_api([text])[0]
            embeddings.append(embedding)
        self.query_response = embeddings

    def save_embeddings(self, filename: str = "embeddings.pt"):
        """
        Save generated embeddings as a PyTorch tensor.

        Args:
            filename (str, optional): The filename for the saved embeddings. Defaults to "embeddings.pt".
        """
        embeddings_tensor = torch.from_numpy(np.array(self.query_response)).to(torch.float)
        torch.save(embeddings_tensor, filename)


if __name__ == "__main__":
    dataset_name = "dataset_name"
    texts = ["How do I get a replacement Medicare card?",
             "What is the monthly premium for Medicare Part B?",
             "How do I terminate my Medicare Part B (medical insurance)?",
             "How do I sign up for Medicare?",
             "Can I sign up for Medicare Part B if I am working and have health insurance through an employer?",
             "How do I sign up for Medicare Part B if I already have Part A?",
             "What are Medicare late enrollment penalties?",
             "What is Medicare and who can get it?",
             "How can I get help with my Medicare Part A and Part B premiums?",
             "What are the different parts of Medicare?",
             "Will my Medicare premiums be higher because of my higher income?",
             "What is TRICARE ?",
             "Should I sign up for Medicare Part B if I have Veterans’ Benefits?"]

    output = query(texts)

    sb = SentenceTransformer(dataset_name=dataset_name, model_id=model_id, hf_token=hf_token)
    sb.generate_embeddings()
    sb.save_embeddings()
