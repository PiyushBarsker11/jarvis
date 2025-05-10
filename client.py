from openai import OpenAI

client = OpenAI(api_key ='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')

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a  virtual assistant named jarvis, skilled in genral task like alexa and google."},
        {"role": "user", "content": " what is coading"}
    ]
)

print(completion.choices[0].message.content )
