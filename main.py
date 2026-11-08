
from config import client
from core.orchestrator import run_lesson_pipeline


def main():

    print("======================================")
    print(" SELF-EVALUATING LESSON CONTENT GENERATOR")
    print("======================================")

    topic = "Introduction to RAG"

    result = run_lesson_pipeline(
        client=client,
        topic=topic
    )

    print("\n========== FINAL STATUS ==========")
    print(result["status"])

    print(f"Total attempts: {result['attempts']}")

    if result["status"] == "APPROVED":
        print("The lesson is ready for human review.")
    else:
        print("The lesson did not meet the required quality bar.")


if __name__ == "__main__":
    main()
