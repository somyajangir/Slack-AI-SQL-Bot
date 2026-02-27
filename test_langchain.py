# test_langchain.py
"""
Test if LangChain SQL integration works
"""

from llm import sql_chain

# Test questions
questions = [
    "Show total revenue",
    "Revenue by region",
    "How many orders total?",
]

print("Testing LangChain SQL Chain...")
print("=" * 60)

for question in questions:
    print(f"\nQuestion: {question}")
    print("-" * 60)

    try:
        result = sql_chain.execute(question)
        print(f"Result:\n{result['result']}")
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing complete!")