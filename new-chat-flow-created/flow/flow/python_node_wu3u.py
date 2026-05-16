from promptflow import tool
from promptflow.connections import CognitiveSearchConnection

@tool
def retrieve_documents(
    query: str,
    search_connection: CognitiveSearchConnection,
    index_name: str,
    top_k: int = 3
) -> str:
    if not query:
        return ""

    try:
        # Local imports to avoid Prompt Flow meta issues
        from azure.core.credentials import AzureKeyCredential
        from azure.search.documents import SearchClient
        from azure.core.pipeline.transport import RequestsTransport

        search_client = SearchClient(
            endpoint=search_connection.api_base,
            index_name=index_name,
            credential=AzureKeyCredential(search_connection.api_key),
            transport=RequestsTransport()
        )

        results = list(search_client.search(search_text=query, top=top_k))

        docs = []
        for result in results:
            content = result.get('content') or result.get('text') or str(result)
            source = result.get('sourcepage') or result.get('title') or ""

            if source:
                docs.append(f"Source: {source}\nContent: {content}")
            else:
                docs.append(content)

        return "\n\n".join(docs)

    except Exception as e:
        return f"Error retrieving documents: {str(e)}"