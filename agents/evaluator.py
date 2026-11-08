
import json

from core.rubric import RUBRIC
from prompts.evaluator_prompt import EVALUATOR_SYSTEM_PROMPT
from config import GEMINI_MODEL


def evaluate_lesson(client, lesson):

    print("\n[EVALUATOR AGENT] Evaluating lesson...")

    # Convert rubric into readable text
    rubric_text = json.dumps(RUBRIC, indent=2)

    # Prepare evaluation request
    evaluation_prompt = f"""
Evaluate the following lesson using this rubric:

RUBRIC:
{rubric_text}

LESSON TO EVALUATE:
<lesson>
{lesson}
</lesson>

Evaluate all six criteria independently.
Return the required JSON structure.
"""

    # Ask Gemini to evaluate
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            EVALUATOR_SYSTEM_PROMPT,
            evaluation_prompt
        ],
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise ValueError("Evaluator returned an empty response.")

    # Convert JSON response into Python dictionary
    result = json.loads(response.text)

    # Validate the evaluator's response
    expected_ids = {item["id"] for item in RUBRIC}
    evaluations = result.get("evaluations", [])

    actual_ids = [item.get("id") for item in evaluations]

    if len(actual_ids) != len(expected_ids):
        raise ValueError("Evaluator did not return exactly six checks.")

    if set(actual_ids) != expected_ids:
        raise ValueError("Evaluator returned missing or unexpected criteria.")

    if len(set(actual_ids)) != len(actual_ids):
        raise ValueError("Duplicate evaluation criteria detected.")

    for item in evaluations:
        if item.get("status") not in ("PASS", "FAIL"):
            raise ValueError("Invalid evaluation status detected.")

        if not item.get("reason"):
            raise ValueError("Evaluation reason is missing.")

    # Calculate the final result ourselves
    # Never blindly trust the model's overall_result.
    all_passed = all(
        item["status"] == "PASS"
        for item in evaluations
    )

    result["overall_result"] = "PASS" if all_passed else "FAIL"

    # Generate rejection reasons from failed checks
    result["rejection_reasons"] = [
        f'{item["id"]} - {item["criterion"]}: {item["reason"]}'
        for item in evaluations
        if item["status"] == "FAIL"
    ]

    print(f"[EVALUATOR AGENT] Result: {result['overall_result']}")

    return result
