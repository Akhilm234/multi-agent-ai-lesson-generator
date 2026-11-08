
from config import client
from core.orchestrator import run_lesson_pipeline


def main():
    topic = "Introduction to RAG"

    print("\n=== SELF-EVALUATING LESSON GENERATOR ===")
    print(f"Topic: {topic}")

    result = run_lesson_pipeline(client, topic)

    print("\n=== FINAL RESULT ===")
    print(f"Status: {result['status']}")
    print(f"Total Attempts: {result['attempts']}")

    if result["status"] == "APPROVED":
        print("\nLesson successfully generated and approved!")
        print("Ready for human review.")
    else:
        print("\nLesson failed the quality evaluation.")


if __name__ == "__main__":
    main()
