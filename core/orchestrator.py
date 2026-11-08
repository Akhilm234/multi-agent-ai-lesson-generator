
import json
from pathlib import Path

from agents.generator import generate_lesson
from agents.evaluator import evaluate_lesson


# ==========================================
# CONFIGURATION
# ==========================================

MAX_RETRIES = 2

OUTPUT_DIR = Path("outputs")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# HELPER FUNCTION: SAVE JSON
# ==========================================

def save_json(filename, data):

    file_path = OUTPUT_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# MAIN ORCHESTRATOR
# ==========================================

def run_lesson_pipeline(client, topic):

    print("\n========================================")
    print(" SELF-EVALUATING LESSON GENERATOR")
    print("========================================")

    print(f"\nTopic: {topic}")
    print(f"Maximum retries: {MAX_RETRIES}")

    # --------------------------------------
    # INITIALIZE PIPELINE VARIABLES
    # --------------------------------------

    rejection_log = []

    feedback = None

    final_lesson = None

    final_evaluation = None

    # Remove outdated results from previous runs
    (OUTPUT_DIR / "lesson.md").unlink(missing_ok=True)

    (OUTPUT_DIR / "rejected_lesson.md").unlink(missing_ok=True)

    # --------------------------------------
    # GENERATION + EVALUATION LOOP
    # --------------------------------------

    for attempt in range(1, MAX_RETRIES + 2):

        print("\n----------------------------------------")
        print(f" ATTEMPT {attempt}")
        print("----------------------------------------")

        # STEP 1: GENERATE LESSON

        print("\n[ORCHESTRATOR] Calling Generator Agent...")

        lesson = generate_lesson(
            client=client,
            topic=topic,
            feedback=feedback
        )

        if not lesson or not lesson.strip():
            raise ValueError("Generator returned an empty lesson.")

        print("[ORCHESTRATOR] Lesson generated.")

        # STEP 2: EVALUATE LESSON

        print("\n[ORCHESTRATOR] Calling Evaluator Agent...")

        evaluation = evaluate_lesson(
            client=client,
            lesson=lesson
        )

        # Validate overall result
        if evaluation.get("overall_result") not in ("PASS", "FAIL"):
            raise ValueError("Invalid evaluator result.")

        final_lesson = lesson

        final_evaluation = evaluation

        # STEP 3: RECORD ATTEMPT

        attempt_record = {
            "attempt": attempt,
            "topic": topic,
            "result": evaluation["overall_result"],
            "evaluations": evaluation["evaluations"],
            "rejection_reasons": evaluation["rejection_reasons"],
            "improvement_summary": evaluation.get(
                "improvement_summary", ""
            )
        }

        rejection_log.append(attempt_record)

        # STEP 4: CHECK PASS OR FAIL

        if evaluation["overall_result"] == "PASS":

            print("\n[SUCCESS] Lesson passed all six criteria!")

            # Save approved lesson
            with open(
                OUTPUT_DIR / "lesson.md",
                "w",
                encoding="utf-8"
            ) as file:

                file.write(lesson)

            print("[ORCHESTRATOR] Approved lesson saved.")

            # Remove any previous rejected draft
            (OUTPUT_DIR / "rejected_lesson.md").unlink(
                missing_ok=True
            )

            break

        # ----------------------------------
        # STEP 5: HANDLE REJECTION
        # ----------------------------------

        print("\n[REJECTED] Lesson failed evaluation.")

        for reason in evaluation["rejection_reasons"]:

            print(f"  - {reason}")

        # ----------------------------------
        # STEP 6: CHECK RETRY LIMIT
        # ----------------------------------

        if attempt > MAX_RETRIES:

            print("\n[STOP] Maximum retry limit reached.")

            print("[ORCHESTRATOR] Pipeline terminated.")

            break

        # ----------------------------------
        # STEP 7: PREPARE FEEDBACK
        # ----------------------------------

        feedback = "\n".join(
            evaluation["rejection_reasons"]
        )

        improvement_summary = evaluation.get(
            "improvement_summary", ""
        )

        if improvement_summary:

            feedback += (
                "\n\nAdditional improvements required:\n"
                + improvement_summary
            )

        print("\n[ORCHESTRATOR] Rejection feedback prepared.")

        print(
            f"[ORCHESTRATOR] Regenerating lesson "
            f"using retry {attempt}..."
        )

    # ======================================
    # FINALIZE PIPELINE
    # ======================================

    if final_evaluation is None:

        raise RuntimeError("Pipeline did not produce an evaluation.")

    approved = (
        final_evaluation["overall_result"] == "PASS"
    )

    # STEP 8: SAVE FINAL EVALUATION

    save_json(
        "final_evaluation.json",
        final_evaluation
    )

    # STEP 9: SAVE REJECTION LOG

    save_json(
        "rejection_log.json",
        rejection_log
    )

    # STEP 10: HANDLE FINAL OUTPUT

    if approved:

        status = "APPROVED"

        print("\n[FINAL STATUS] APPROVED")

        print("[OUTPUT] outputs/lesson.md")

    else:

        status = "REJECTED"

        # Save final rejected lesson separately
        with open(
            OUTPUT_DIR / "rejected_lesson.md",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(final_lesson)

        # Ensure rejected lesson is never published
        (OUTPUT_DIR / "lesson.md").unlink(
            missing_ok=True
        )

        print("\n[FINAL STATUS] REJECTED")

        print("[OUTPUT] outputs/rejected_lesson.md")

    # ======================================
    # PIPELINE SUMMARY
    # ======================================

    print("\n========================================")
    print(" PIPELINE EXECUTION SUMMARY")
    print("========================================")

    print(f"Topic             : {topic}")

    print(f"Total Attempts    : {len(rejection_log)}")

    print(f"Maximum Retries   : {MAX_RETRIES}")

    print(f"Final Result      : {status}")

    print(
        f"Rejected Attempts : "
        f"{sum(1 for item in rejection_log if item['result'] == 'FAIL')}"
    )

    print("\nGenerated Files:")

    print("- outputs/final_evaluation.json")

    print("- outputs/rejection_log.json")

    if approved:

        print("- outputs/lesson.md")

    else:

        print("- outputs/rejected_lesson.md")

    print("\n========================================")
    print(" PIPELINE EXECUTION COMPLETED")
    print("========================================")

    # ======================================
    # RETURN COMPLETE PIPELINE RESULT
    # ======================================

    return {

        "status": status,

        "topic": topic,

        "lesson": final_lesson,

        "evaluation": final_evaluation,

        "attempts": len(rejection_log),

        "rejection_log": rejection_log

    }
