from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

if __name__ == "__main__":

    sentences = ["This is an example sentence",
                 "Should I sign up for Medicare Part B if I have Veterans’ Benefits?",
                 "Where are is dogs?",
                 "cats is hats",
                 "tigers are red",
                 "three is filing",
                 "The size of our embedded dataset is .shape} and of our embedded query is {query_embeddings.shape}.",
                 "there are three cats",
                 ]

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    corpus_embeddings = model.encode(sentences)
    print(corpus_embeddings)

    question = ["How many cats?"]
    query_embeddings = model.encode(question)
    print(
        f"The size of our embedded dataset is {corpus_embeddings.shape} and of our embedded query is {query_embeddings.shape}.")
    hits = semantic_search(query_embeddings, corpus_embeddings, top_k=5)
    winners = [sentences[hit['corpus_id']] for hit in hits[0]]

    # sentence_transformer = SentenceTransformer()
    # output = sentence_transformer.query_api(texts)
    # sentence_transformer.generate_embeddings()
    # sentence_transformer.save_embeddings()
