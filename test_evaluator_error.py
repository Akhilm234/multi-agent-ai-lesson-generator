
import json
from config import client
from agents.evaluator import evaluate_lesson


# Lesson containing one intentional technical error
incorrect_lesson = """
# Introduction to RAG

RAG stands for Random Answer Generation.

RAG is a technique where an AI model generates
answers without retrieving information from
external sources.

It does not use document retrieval or external
knowledge sources.

RAG is useful for building AI applications.

It can help users get answers to their questions.
"""


def main():
    print("\n=== EVALUATOR ERROR DETECTION TEST ===")

    print("\nSending lesson with an intentional error...")
    print("Incorrect definition: Random Answer Generation")

    # Send the incorrect lesson to the Evaluator Agent
    result = evaluate_lesson(
        client=client,
        lesson=incorrect_lesson
    )

    print("\n=== EVALUATION RESULT ===")
    print(json.dumps(result, indent=4))

    print("\n=== TEST VERIFICATION ===")

    accuracy = next(
        item for item in result["evaluations"]
        if item["id"] == "C1"
    )

    if (
        accuracy["status"] == "FAIL"
        and result["overall_result"] == "FAIL"
    ):
        print("SUCCESS: Evaluator detected the technical error!")
    else:
        print("The expected error detection was not confirmed.")


if __name__ == "__main__":
    main()
