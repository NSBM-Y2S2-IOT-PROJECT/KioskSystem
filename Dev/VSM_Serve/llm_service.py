import openai
import chromadb
import pypdf
from chromadb.config import Settings
import os



def initializeChroma():
    pagearray = []
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    pdf_path = os.path.join(base_dir, "RAG_Data", "data.pdf")  # Construct the absolute path

    reader = pypdf.PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()
        pagearray.append(text)

    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="rag_data")
    for i in range(len(pagearray)):
        print(pagearray[i])
        collection.add(
            documents=[pagearray[i]],
            metadatas=[{"page": i}],
            ids=[str(i)]
        )


def RAG(prompt):
    client = chromadb.Client()
    collection = client.get_collection("rag_data")
    results = collection.query(
        query_texts=[prompt],
        n_results=5
    )
    docs = results['documents'][0]
    metadata = results['metadatas'][0]
    ids = results['ids'][0]
    return docs, metadata, ids

def extractJson(llm_output):
    try:
        extract_text = llm_output.split("```json")[1].split("```")[0]
        json_output = eval(extract_text)
        return json_output
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return {"error": "A Serverside Error Occured ! Please try again later."}


def llmBridge(prompt, rag=False):
    if rag:
        docs, metadata, ids = RAG(prompt)
        prompt = f"Based on the following documents: {docs}, please provide a response to the prompt: {prompt}"
    else:
        prompt = f"Please provide a response to the prompt: {prompt}"
    

    client = openai.OpenAI(
        base_url="http://localhost:8080/v1",
        api_key = "sk-no-key-required"
    )

    completion = client.chat.completions.create(
    model="llama3.2",
    temperature=1,
    messages=[
        {"role": "system", "content": "You are  an assistant designed to help with skincare advice. Analyze the input and give appropriate advice. Provide the recommendation in json format."
        "with keys links, products, and ingredients, recommendation_description"},
        {"role": "user", "content": prompt}
    ]
    )

    return (extractJson(completion.choices[0].message.content))


if __name__ == "__main__":
    print("LLM_SERVICE_TEST")
    # llmBridge("SkinColor: Fair, SkinTexture: Dry")
    # initializeChroma()
    llmBridge("SkinColor: Fair, SkinTexture: Dry", rag=True)