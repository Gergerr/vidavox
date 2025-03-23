# rag/rag_pipeline.py
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class RAGPipeline:
    def __init__(self, vector_store, data_loader, groq_api_key, model_name="llama3-8b-8192"):
        self.vector_store = vector_store
        self.data_loader = data_loader
        self.llm = ChatGroq(
            model_name=model_name,
            api_key=groq_api_key
        )

        prompt_template = """Gunakan konteks berikut untuk menjawab pertanyaan tentang GeralBot. Fokus pada informasi yang relevan dengan topik yang diminta. Jika informasi tidak ada di konteks, coba rangkum informasi yang sedikit relevan atau katakan "Informasi tidak ditemukan di dokumen."

Konteks:
{context}

Pertanyaan: {question}

Jawaban:"""
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 15}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def query(self, query):
        try:
            # Cek apakah query terkait CSV
            csv_result = self.data_loader.query_csv(query)
            if csv_result:
                return csv_result, [{"source": "synthetic_data.csv", "heading": "SQL Query Result"}]

            # Query expansion sederhana
            expanded_query = query
            if "mengisi daya" in query.lower():
                expanded_query = query + " pengisian daya"
            if "pembersih" in query.lower():
                expanded_query = query + " pembersihan"

            # Ambil dokumen relevan
            docs = self.vector_store.similarity_search(expanded_query, k=15)
            # Batasi konteks jadi maksimal 4000 karakter (~2000 token)
            context = "\n".join([doc.page_content for doc in docs])[:4000]
            result = self.qa_chain.invoke({"query": query})
            answer = result["result"]
            sources = [doc.metadata for doc in result["source_documents"]]
            return answer, sources
        except Exception as e:
            if "Error code: 413" in str(e):
                print("Request too large, reducing context size and retrying...")
                context = context[:1000]  # Batasi jadi ~500 token
                prompt = self.prompt.format(context=context, question=query)
                answer = self.llm.invoke(prompt).content
                sources = [docs[0].metadata]
                return answer, sources
            else:
                raise e