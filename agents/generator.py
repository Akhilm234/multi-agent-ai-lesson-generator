
from prompts.generator_prompt import (
    GENERATOR_SYSTEM_PROMPT,
    build_generator_prompt
)
from config import GEMINI_MODEL


def generate_lesson(client, topic, feedback=None, memory_context=None):

    print("\n[Generator] Creating lesson...")

    # Prepare instructions for Gemini
    prompt = build_generator_prompt(
        topic=topic,
        feedback=feedback,
        memory_context=memory_context
    )

    # Generate the lesson
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            GENERATOR_SYSTEM_PROMPT,
            prompt
        ]
    )

    if not response.text:
        raise ValueError("Gemini did not generate any lesson.")

    lesson = response.text

    print("[Generator] Lesson generated successfully.")

    return lesson
