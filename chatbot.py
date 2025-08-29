# chatbot.py
import os
from typing import List, Dict, Any

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from openai import OpenAI

from book_data import get_summary_by_title,search_summaries_by_keyword

CHROMA_PATH = "chroma"
COLLECTION_NAME = "book_summaries"

SYSTEM_PROMPT = (
    "You are Smart Librarian, an assistant that recommends books. "
    "Using the retrieved context (titles, themes, short summaries), "
    "propose one clear recommendation (maximum two if there is a tie). "
    "After you decide the title, CALL THE TOOL `get_summary_by_title` with the exact title. "
    "Then compose the final answer in English:\n"
    "1) The recommendation (title + why it matches)\n"
    "2) The detailed summary (from the tool)\n"
    "3) 2–3 key themes\n"
    "If the user asks 'What is <title>?', provide the summary directly via the tool."
)

TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Return the full summary for the given exact book title.",
            "parameters": {
                "type": "object",
                "properties": {"title": {"type": "string"}},
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_summaries_by_keyword",
            "description": "Search all summaries by a keyword (case-insensitive) and return matches.",
            "parameters": {
                "type": "object",
                "properties": {"keyword": {"type": "string"}},
                "required": ["keyword"],
            },
        },
    },
]



class RAGChatbot:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        self.chat_model = os.getenv("CHAT_MODEL", "gpt-4o-mini")
        self.embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")

        # Setup ChromaDB client and collection
        self.chroma = chromadb.PersistentClient(path=CHROMA_PATH)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=self.embed_model,
        )
        self.col = self.chroma.get_or_create_collection(
            name=COLLECTION_NAME, embedding_function=openai_ef
        )

        self.history: List[Dict[str, str]] = []

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search in Chroma vector store for the most relevant book summaries."""
        res = self.col.query(query_texts=[query], n_results=k)
        items = []
        for i in range(len(res["ids"][0])):
            items.append(
                {
                    "id": res["ids"][0][i],
                    "document": res["documents"][0][i],
                    "metadata": res["metadatas"][0][i],
                }
            )
        return items

    def build_context(self, items: List[Dict[str, Any]]) -> str:
        """Format retrieved items into a context string for GPT."""
        lines = ["## Candidates (from retriever):"]
        for it in items:
            md = it["metadata"]
            lines.append(
                f"- Title: {md['title']} | Themes: {', '.join(md['themes'])}\n"
                f"  Snippet: {it['document'][:240]}..."
            )
        return "\n".join(lines)

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call the specified tool with arguments and return the result."""
        if name == "get_summary_by_title":
            return get_summary_by_title(arguments.get("title", ""))
        elif name == "search_summaries_by_keyword":
            results = search_summaries_by_keyword(arguments.get("keyword", ""))
            if not results:
                return f"No matches found for keyword '{arguments.get('keyword')}'."
            return "\n\n".join([f"{t}: {s}" for t, s in results.items()])
        return ""


    def ask(self, user_msg: str) -> str:
        """Main entry point: takes user input, queries retriever + LLM + tool, returns final answer."""
        # 1) Retrieve candidates
        items = self.retrieve(user_msg, k=5)
        
        context = self.build_context(items)

        # 2) Build messages
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self.history,
            {"role": "system", "content": context},
            {"role": "user", "content": user_msg},
        ]

        # 3) First GPT call (may request a tool)
        resp = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            tools=TOOLS_SPEC,
            tool_choice="auto",
            temperature=0.2,
        )

        choice = resp.choices[0]
        finish = choice.finish_reason

        if finish == "tool_calls":
            tool_call = choice.message.tool_calls[0]
            tool_name = tool_call.function.name
            import json as _json
            args = _json.loads(tool_call.function.arguments or "{}")

            # Run the tool
            tool_result = self.call_tool(tool_name, args)

            # Add assistant message with tool_calls
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": choice.message.tool_calls,
            })

            # Add the tool's response message (IMPORTANT!)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result or "(Summary unavailable)",
            })

            # Final GPT call to integrate the tool result
            final = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.2,
            )
            text = final.choices[0].message.content.strip()

        else:
            # GPT answered directly without tool
            text = choice.message.content.strip()

        # Update history (truncate for memory management)
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": text[:2000]})
        if len(self.history) > 10:
            self.history = self.history[-10:]

        return text
