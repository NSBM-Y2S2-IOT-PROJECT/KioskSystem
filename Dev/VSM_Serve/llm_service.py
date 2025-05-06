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
    print(llm_output)
    try:
        extract_text = llm_output
        json_output = eval(extract_text)
        print(json_output)
        return json_output
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return llm_output


def llmBridge(prompt, rag=False):
    systemPrompt = '''
    You are a skincare assistant designed to analyze skin characteristics and provide personalized product and ingredient recommendations. Based on the user’s skin tone, texture, and concerns, generate advice in the following JSON structure:

    {
      "recommendations": "A paragraph summarizing your recommendations based on the user’s skin profile. Include suggested product types, ingredient benefits, and how they work together.",
      "recommended_ingredients": [
        "Ingredient: Brief explanation of how it helps",
        "Ingredient: Brief explanation of how it helps"
      ],
      "suggested_products": [
        "Product Name: Short description of what it does and why it's recommended",
        "Product Name: Short description of what it does and why it's recommended"
        "Product Link: A Link that is provided based on the docs. If there is no link no need"
      ]
    }
    Requirements:

    The recommendations field should be a natural, well-written paragraph.

    The recommended_ingredients and suggested_products fields should each contain plain text strings (the client will render them as bullet points).

    No any comments

    Tailor product and ingredient recommendations to the user's specific skin tone, texture, and concerns.

    Use specific product names (e.g., “AXIS-Y Dark Spot Correcting Glow Serum”) when possible.

    Do not include Markdown or formatting—return raw JSON only.
    '''
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
        {"role": "system", "content": f"{systemPrompt}"
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
