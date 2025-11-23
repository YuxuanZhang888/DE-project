from pymongo import MongoClient
from langchain.embeddings import HuggingFaceEmbeddings




MONGO_URI = ""
DB_NAME = "de-project"
COLLECTION_NAME = "embeddings"
VECTOR_INDEX_NAME = "vector_index"  
VECTOR_FIELD = "embedding"  
VECTOR_DIMENSIONS = 512 


def init_embeddings_model() -> HuggingFaceEmbeddings:
   

    model_name = "distiluse-base-multilingual-cased-v2"
    model_kwargs = {"device": "cpu"} 
    encode_kwargs = {"normalize_embeddings": True}  
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    

    test_dim = len(embeddings.embed_query("test"))
    if test_dim != VECTOR_DIMENSIONS:
        raise ValueError(f"The model output dimension is{test_dim}，It must be consistent with the database vector dimension {VECTOR_DIMENSIONS}!")
    
    return embeddings


def search_similar_docs(question: str, top_k: int = 3) -> list:
    """
    Use LangChain to generate question vectors and query the TopK similar documents in MongoDB.
    """
    try:
        embeddings = init_embeddings_model()
        
       
        query_vector = embeddings.embed_query(question)
        
        
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        
        pipeline = [
            
            {
                "$vectorSearch": {
                    "index": VECTOR_INDEX_NAME,
                    "queryVector": query_vector,
                    "path": VECTOR_FIELD,
                    "limit": top_k,
                    "numCandidates": top_k * 10 ,
                    "filter": {  
                        "content": {"$exists": True, "$ne": ""}
                    }
                }
            },
            {
                "$addFields": {
                    "similarity_score": {"$meta": "vectorSearchScore"}  
                }
            },
            {
                "$project": {
                    "content": 1,
                    "document": 1,
                    "source_file": 1,
                    "type":1,
                    "similarity_score": 1,
                    "_id": 0
                }
            }
        ]
        
        results = list(collection.aggregate(pipeline))
        return results
    
    except Exception as e:
        raise Exception(f"Search failed：{str(e)}")
    finally:
        client.close()  

