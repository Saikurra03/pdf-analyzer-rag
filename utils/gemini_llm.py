from config import groq_client, GROQ_MODEL


def generate_answer(prompt):

    print("\n" + "=" * 60)
    print("STEP 8 : GROQ GENERATING ANSWER")
    print("=" * 60)

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=GROQ_MODEL,
        temperature=0.3,
        max_tokens=2048,
    )

    response = chat_completion.choices[0].message.content

    print("\nGroq Response\n")
    print(response)

    return response
