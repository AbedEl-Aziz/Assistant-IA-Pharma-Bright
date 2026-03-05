from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.llms import GPT4All
from app.utils.embeddings import get_embeddings
import os
model_path = os.path.abspath("app/models/mistral-7b-instruct-v0.1.Q4_0.gguf")

class RagPipeline:
    def __init__(self):
        self.documents_path = Path(__file__).parent.parent / "documents"
        self.chunk_size = 500
        self.chunk_overlap = 50
        self.embeddings = get_embeddings()
        self.vectorstores = {}

    def _load_documents(self, tenant_id: str):
        tenant_folder = self.documents_path / tenant_id
        if not tenant_folder.exists():
            raise FileNotFoundError(f"No documents found for tenant {tenant_id}")
        docs = []
        for file_path in tenant_folder.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                docs.append({"content": content, "source": file_path.name})
        return docs

    def _get_vectorstore(self, tenant_id: str):
        if tenant_id in self.vectorstores:
            return self.vectorstores[tenant_id]

        docs = self._load_documents(tenant_id)
        texts, metadatas = [], []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        for doc in docs:
            chunks = splitter.split_text(doc["content"])
            texts.extend(chunks)
            metadatas.extend([{"source": doc["source"]}] * len(chunks))

        vectorstore = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        self.vectorstores[tenant_id] = vectorstore
        return vectorstore

    def run(self, question: str, tenant_id: str):

        vectorstore = self._get_vectorstore(tenant_id)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        llm = GPT4All(
            model=str(model_path),
            verbose=False
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        result = qa_chain.invoke({"query": question})
        answer = result["result"]

        sources = [
            {"source": doc.metadata.get("source", ""), "text": doc.page_content}
            for doc in result["source_documents"]
        ]

        return {"answer": answer, "sources": sources}