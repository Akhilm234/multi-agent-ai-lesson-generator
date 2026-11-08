
from prompts.generator_prompt import (
    GENERATOR_SYSTEM_PROMPT,
    build_generator_prompt
)


def generate_lesson(client, topic, feedback=None, memory_context=None):

    print("\n[GENERATOR AGENT] Creating lesson...")

    # Build the prompt
    user_prompt = build_generator_prompt(
        topic=topic,
        feedback=feedback,
        memory_context=memory_context
    )

    # Send instructions to Gemini
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[
            GENERATOR_SYSTEM_PROMPT,
            user_prompt
        ]
    )

    # Extract generated lesson
    lesson = response.text

    print("[GENERATOR AGENT] Lesson generated successfully.")

    return lesson
