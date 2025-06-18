def build_prompt(context, question):
    return f"""You are a helpful teaching assistant for the Tools in Data Science (TDS) course at IITM Online BSc.

Use the following course or discussion content to answer the question.

Context:
---------
{context}

---------

Question: {question}

Answer:"""
