import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from app.services.vector_store import vector_store_manager
from typing import List, Dict, Generator

SYSTEM_PROMPT = """You are a helpful AI assistant. Answer ONLY from the provided document context. If answer is not present, say 'Answer not found in document.'

Context:
{context}

Question: {question}
Answer:"""

class RAGPipeline:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        
        self.api_key = os.getenv("GROQ_API_KEY")
        if self.api_key:
            self.llm = ChatGroq(temperature=0, api_key=self.api_key, model="llama-3.1-8b-instant")
            self.chain = self.prompt | self.llm | StrOutputParser()
        else:
            self.llm = None
            self.chain = None

    def _get_context_and_sources(self, document_id: str, question: str):
        results = vector_store_manager.search(document_id, question, k=3)
        context_texts = []
        sources = []
        
        for doc, score in results:
            context_texts.append(doc.page_content)
            sources.append({
                "page_num": doc.metadata.get("page_num", 0),
                "similarity_score": float(score),
                "text_snippet": doc.page_content[:100] + "..."
            })
            
        return "\n\n".join(context_texts), sources
        
    def query(self, document_id: str, question: str) -> Dict:
        context_str, sources = self._get_context_and_sources(document_id, question)
        
        if not context_str:
            return {"answer": "Answer not found in document.", "sources": []}
            
        if self.chain:
            try:
                answer = self.chain.invoke({"context": context_str, "question": question})
            except Exception as e:
                import traceback
                print(f"Error invoking chain: {e}")
                traceback.print_exc()
                answer = "Error generating answer. Please check backend logs."
        else:
            answer = f"[MOCK LLM - No API Key] Based on the context: {context_str[:200]}..."
            
        return {
            "answer": answer,
            "sources": sources
        }

    def query_stream(self, document_id: str, question: str):
        context_str, sources = self._get_context_and_sources(document_id, question)
        
        if not context_str:
            yield "Answer not found in document."
            yield f"__SOURCES__:{json.dumps([])}"
            return

        if self.chain:
            try:
                for chunk in self.chain.stream({"context": context_str, "question": question}):
                    yield chunk
            except Exception as e:
                import traceback
                print(f"Error streaming chain: {e}")
                traceback.print_exc()
                yield "Error generating answer. Please check backend logs."
        else:
            import time
            answer = f"[MOCK LLM - No API Key] Based on the context: {context_str[:200]}..."
            for word in answer.split(" "):
                yield word + " "
                time.sleep(0.05)
                
        yield f"__SOURCES__:{json.dumps(sources)}"

rag_pipeline = RAGPipeline()
