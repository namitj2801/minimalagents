from minimal_agents.llm.groq import GroqProvider


llm = GroqProvider()
print(llm.generate("Explain the working of dijkstra's aglorithm in 1 line."))

