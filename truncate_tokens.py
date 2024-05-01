import tiktoken

tokenizer = tiktoken.encoding_for_model("gpt-4")

TEXT="""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure 
dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non 
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

print()
print("Original text")
print(TEXT)

# Number of tokens we want to truncate to
tokens_count=50

tokens = tokenizer.encode(TEXT)
print()
print("Tokens")
print(tokens)
print()
print(f"Text contains {len(tokens)} tokens")

truncated_tokens = tokens[:tokens_count]

print()
print(f"Text truncated to {len(truncated_tokens)} tokens")
print(tokenizer.decode(truncated_tokens))
