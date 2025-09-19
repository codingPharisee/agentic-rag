from vector_store import retrieve

query= input("what is an API: ")

print("query:", query)

results= retrieve(query)

print("results", results)