from minimal_agents.llm.gemini import GeminiProvider

llm = GeminiProvider()
print(llm.generate("Say hello in one short sentence."))