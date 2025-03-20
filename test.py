from ai import OpenAIChat
message = "what color is a grape"
response = OpenAIChat()
print(response.get_response(message))