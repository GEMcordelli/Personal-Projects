'''
The following is an example python code of a customized GPT
agent that is primed by relevant information associated with
the repuational risks of employee activism for corporations...

How It Works:
1. We ping openAI using an API key to embed relevant documents. Embedding is like taking 
a piece of text and converting it to a mathematical language computers can understand.

2. We store the embeddings into a database called ChromaDB. This will be where the "context" lives for our GPT agent to use.

3. When a user asks a question or "query", we will embed the query into the same language we used for the documents, so we can compare them via search.

4. The most relevant documents will then be passed to the GPT as context, along with a users query; it can be the same query as step 3, or a follow up/modified version.

5. This way, the GPT is primed with relevant information to give a more accurate answer!

THE DOCUMENTS WE WILL USE AS CONTEXT (RAG MODELING):

The Pew Research API will be good for baseline public opinion data, which could be relevant when talking about reputational risk,
and updated research data about the dynamics between employee activism and corporations

The News API (https://newsapi.org/) will be better for incorporating up to date information on employee activism, 
and other events thats are associated with it, may they ever arise (could be political)

The SEC has an API where we can get company submission histories for profit filing; I checked out the filing history for Amazon,
and it goes back several years with lots of detailed info. This will be great to see direct financial states of companies in tandem with
previous employee activism events & will help us predict future financial risks!

Using an existing GPT assistant at Gravity, we can also pull individual news story URLs about employee activism events, 
compile them into organized data, and convert them to csv. This, along with fact checking, can be automated via comapny LLMs

Lastly, I found a scholarly paper called "THE RISE OF CORPORATE ACTIVISM: A DOUBLE-EDGED SWORD FOR MULTINATIONAL CORPORATIONS" from University of Novi Sad, Serbia
http://ebooks.ien.bg.ac.rs/1783/1/Nau%C4%8Dni%20rad%20-%20Jolovi%C4%87%20%26%20Jolovi%C4%87.pdf
Although this is more about corporate activism than employee activism, it has a lot of helpful and relevant information about the commercial, fincancial, and 
reputational risks when public social stances are associated with corporations. This can be a good foundational document to embed into the database as well


'''



# 🛠️ STEP 0: SETUP
# pip install chromadb openai tiktoken
import chromadb
from chromadb.config import Settings
from openai import OpenAI
import tiktoken  # Optional: helps manage token limits
import os

# GPT + embedding model config
openai_client = OpenAI(api_key="you'll put the key here; keep this private!")
EMBEDDING_MODEL = "text-embedding-3-small"
GPT_MODEL = "gpt-4o"

# 🔧 Setup Chroma (local vector DB)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("activism_insights")

# 🧠 STEP 1: EMBED YOUR DOCUMENTS (AFTER CLEANING TEXT)
def embed_text(text):
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding

# Example raw doc from NewsAPI, SEC API, Pew, etc.
# With access to the real APIs and/or news scraped material, these documents would be different, and larger scale
doc1 = "In 2019, Wayfair employees protested sales to ICE detention centers. This led to public backlash and a company-wide walkout. The business relationship with ICE was eventually terminated"
doc2 = "Google employees raised censorship concerns over the company's contract with the Pentagon, resulting in project cancellation."

documents = [doc1, doc2]
metadata = [{"source": "NewsAPI"}, {"source": "SEC Filing"}]

# Embed + store in Chroma
for i, doc in enumerate(documents):
    vector = embed_text(doc)
    collection.add(
        documents=[doc],
        metadatas=[metadata[i]],
        ids=[f"doc_{i}"],
        embeddings=[vector]
    )

# 🔎 STEP 2: QUERY THE VECTOR DB
def search_similar_documents(query, top_k=3):
    query_vector = embed_text(query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    return results["documents"][0]  # Top K matching docs

# 🧠 STEP 3: GENERATE ANSWER USING GPT
def ask_gpt(user_question, context_docs):
    context = "\n\n".join(context_docs)
    prompt = f"""
You are an analyst producing insight on reputational risks for corporate leadership.

Here is relevant background information:
{context}

Question:
{user_question}

Answer clearly and concisely, drawing only from the context above.
"""
    response = openai_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content

# 🧪 TEST
user_query = "How can employee activism lead to contract losses?"
top_docs = search_similar_documents(user_query)
answer = ask_gpt(user_query, top_docs)

print("\n📣 GPT Answer:\n", answer)
'''
NOTE: my personal openai account hit its rate limit due to workshopping bugged code, so I was not able to run through the full example end-to-end. 
# However, this is an example of what the output may look like:
# GPT Answer:
#Here is relevant background information:
#In 2019, Wayfair employees protested sales to ICE detention centers. This led to public backlash and a company-wide walkout. 
#The business relationship with ICE was eventually terminated.
#Google employees raised censorship concerns over the company's contract with the Pentagon, resulting in project cancellation.

'''
