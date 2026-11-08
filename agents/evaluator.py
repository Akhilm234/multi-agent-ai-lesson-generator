
import json

from core.rubric import RUBRIC
from prompts.evaluator_prompt import EVALUATOR_SYSTEM_PROMPT
from config import GEMINI_MODEL


def evaluate_lesson(client, lesson):

    print("\n[Evaluator] Checking generated lesson...")

    rubric_text = json.dumps(RUBRIC, indent=2)

    prompt = f"""
    Evaluate the lesson using the following rubric:

    {rubric_text}

    Lesson:
    {lesson}

    Evaluate all six criteria separately.
    Return the result in the required JSON format.
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            EVALUATOR_SYSTEM_PROMPT,
            prompt
        ],
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise ValueError("No evaluation response received.")

    result = json.loads(response.text)

    # Check whether all rubric criteria are included
    evaluations = result.get("evaluations", [])
    expected_ids = {item["id"] for item in RUBRIC}
    actual_ids = {item.get("id") for item in evaluations}

    if len(evaluations) != len(expected_ids) or actual_ids != expected_ids:
        raise ValueError("Evaluation criteria are missing or incorrect.")

    # Check the evaluation results
    for item in evaluations:

        if item.get("status") not in ["PASS", "FAIL"]:
            raise ValueError("Invalid evaluation status.")

        if not item.get("reason"):
            raise ValueError("Evaluation reason is missing.")

    # Decide the final result based on individual checks
    passed = all(item["status"] == "PASS" for item in evaluations)

    result["overall_result"] = "PASS" if passed else "FAIL"

    # Collect feedback for criteria that failed
    result["rejection_reasons"] = []

    for item in evaluations:
        if item["status"] == "FAIL":
            reason = f'{item["id"]} - {item["criterion"]}: {item["reason"]}'
            result["rejection_reasons"].append(reason)

    print(f"[Evaluator] Result: {result['overall_result']}")

    return result
