## Setup Instructions
1. Clone the project.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set your Groq API Key in a `.env` file:
```bash
GROQ_API_KEY=your_groq_api_key_here
```
4. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

## Example API Request
POST `/query`
```json
{
  "query": "What are the top 3 use cases for GraphQL in enterprise SaaS?"
}
```

## Example API Response
```json
{
  "answer": "- GraphQL provides efficient data fetching [Source: doc_1.txt]\n- Enables flexible queries in SaaS platforms [Source: doc_2.txt]\n- Supports rapid UI development [Source: doc_4.txt]",
  "sources": ["doc_1.txt", "doc_2.txt", "doc_4.txt"]
}
```