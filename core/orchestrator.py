
import json
from pathlib import Path

from agents.generator import generate_lesson
from agents.evaluator import evaluate_lesson


MAX_RETRIES = 2
OUTPUT_DIR = Path("outputs")

OUTPUT_DIR.mkdir(exist_ok=True)


def save_json(filename, data):
    file_path = OUTPUT_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def run_lesson_pipeline(client, topic):

    print("\n========== LESSON GENERATOR ==========")
    print(f"Topic: {topic}")
    print(f"Maximum retries: {MAX_RETRIES}")

    feedback = None
    rejection_log = []
    final_lesson = None
    final_evaluation = None

    # Remove results from the previous run
    (OUTPUT_DIR / "lesson.md").unlink(missing_ok=True)
    (OUTPUT_DIR / "rejected_lesson.md").unlink(missing_ok=True)

    # First attempt + maximum retries
    for attempt in range(1, MAX_RETRIES + 2):

        print(f"\n--- Attempt {attempt} ---")

        # Generate the lesson
        print("[Orchestrator] Generating lesson...")

        lesson = generate_lesson(
            client=client,
            topic=topic,
            feedback=feedback
        )

        if not lesson or not lesson.strip():
            raise ValueError("Generated lesson is empty.")

        # Evaluate the generated lesson
        print("[Orchestrator] Evaluating lesson...")

        evaluation = evaluate_lesson(
            client=client,
            lesson=lesson
        )

        result = evaluation.get("overall_result")

        if result not in ["PASS", "FAIL"]:
            raise ValueError("Invalid evaluation result.")

        final_lesson = lesson
        final_evaluation = evaluation

        # Store the result of this attempt
        rejection_log.append({
            "attempt": attempt,
            "topic": topic,
            "result": result,
            "evaluations": evaluation["evaluations"],
            "rejection_reasons": evaluation["rejection_reasons"],
            "improvement_summary": evaluation.get("improvement_summary", "")
        })

        # Accept the lesson if all checks pass
        if result == "PASS":

            print("\n[Orchestrator] Lesson approved!")

            with open(OUTPUT_DIR / "lesson.md", "w", encoding="utf-8") as file:
                file.write(lesson)

            break

        # Display reasons for rejection
        print("\n[Orchestrator] Lesson needs improvement.")

        for reason in evaluation["rejection_reasons"]:
            print(f"- {reason}")

        # Stop if all retries have been used
        if attempt == MAX_RETRIES + 1:
            print("\n[Orchestrator] Maximum retries reached.")
            break

        # Send evaluation feedback to the Generator Agent
        feedback = "\n".join(evaluation["rejection_reasons"])

        summary = evaluation.get("improvement_summary", "")

        if summary:
            feedback += "\nAdditional improvements: " + summary

        print("[Orchestrator] Sending feedback for regeneration...")

    if final_evaluation is None:
        raise RuntimeError("No evaluation was generated.")

    # Save the final evaluation and attempt history
    save_json("final_evaluation.json", final_evaluation)
    save_json("rejection_log.json", rejection_log)

    approved = final_evaluation["overall_result"] == "PASS"

    # Save the final lesson based on its evaluation
    if approved:
        status = "APPROVED"
        print("\n[Final Status] APPROVED")
        print("Saved: outputs/lesson.md")

    else:
        status = "REJECTED"

        with open(OUTPUT_DIR / "rejected_lesson.md", "w", encoding="utf-8") as file:
            file.write(final_lesson)

        print("\n[Final Status] REJECTED")
        print("Saved: outputs/rejected_lesson.md")

    # Display a summary of the execution
    rejected_attempts = sum(
        1 for item in rejection_log if item["result"] == "FAIL"
    )

    print("\n========== EXECUTION SUMMARY ==========")
    print(f"Topic: {topic}")
    print(f"Total attempts: {len(rejection_log)}")
    print(f"Rejected attempts: {rejected_attempts}")
    print(f"Final result: {status}")
    print("Evaluation: outputs/final_evaluation.json")
    print("History: outputs/rejection_log.json")
    print("=======================================")

    return {
        "status": status,
        "topic": topic,
        "lesson": final_lesson,
        "evaluation": final_evaluation,
        "attempts": len(rejection_log),
        "rejection_log": rejection_log
    }
