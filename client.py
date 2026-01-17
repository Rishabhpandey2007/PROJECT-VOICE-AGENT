from groq import Groq

client = Groq(api_key="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")

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a voice assistant named Jarvis"},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(completion.choices[0].message.content)
