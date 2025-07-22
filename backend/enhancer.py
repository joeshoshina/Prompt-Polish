from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-2.5-flash')

"""
Debugging: Print the model name to ensure it's loaded correctly.""
response = model.generate_content("What's a fun fact about space?")
print(response.text)
"""

"""
Prompt Booster Backend
----------------------
This module takes a raw prompt input (e.g., from a Chrome extension),
applies a set of universal prompt improvement heuristics, and sends the
enhanced prompt to Gemini for final refinement. The final output is a 
polished prompt ready for use in any AI service like ChatGPT, Gemini, or Claude.
"""

def add_clarity(prompt: str) -> str:
    """
    Enhance the prompt by adding instructions to be specific and clear.
    Suggest replacing vague terms with concrete details, adding constraints 
    (length, format, style), and specifying the desired output structure.
    """
    additions = (
        "\n\nPlease be specific and clear. Replace vague terms with concrete details, "
        "and add constraints such as length, format, and style if applicable."
        " Specify the desired output structure."
    )
    return prompt.strip() + additions


def add_context(prompt: str) -> str:
    """
    Add relevant background information and specify the purpose or goal of the prompt.
    Encourage consideration of the target audience if applicable.
    """
    additions = (
        "\n\nInclude relevant background information and specify the purpose or goal. "
        "If relevant, consider the target audience."
    )
    return prompt.strip() + additions


def add_examples(prompt: str) -> str:
    """
    Suggest providing one or two concrete examples illustrating the desired input/output format.
    Use "For example..." constructions to improve AI understanding.
    """
    additions = (
        "\n\nFor example, you can provide 1–2 input/output samples illustrating the desired format or content."
    )
    return prompt.strip() + additions


def request_step_by_step(prompt: str) -> str:
    """
    Request the AI to think step-by-step and explain its reasoning.
    Ask the AI to show its work to improve response quality.
    """
    additions = (
        "\n\nPlease think step-by-step, explain your reasoning, and show your work."
    )
    return prompt.strip() + additions


def define_output_format(prompt: str) -> str:
    """
    Specify the desired output structure and format clearly.
    Recommend using numbered lists, bullet points, headers, or JSON formatting as appropriate.
    """
    additions = (
        "\n\nStructure the output clearly: use numbered lists, bullet points, headers, or specific formats like JSON if suitable."
    )
    return prompt.strip() + additions


def add_quality_instructions(prompt: str) -> str:
    """
    Add instructions to be accurate and thorough.
    Ask the AI to state uncertainty if any and to double-check its reasoning.
    """
    additions = (
        "\n\nBe accurate and thorough. If uncertain, please say so. Double-check your reasoning."
    )
    return prompt.strip() + additions


def enhance_prompt(prompt: str) -> str:
    """
    Wrapper method that applies all internal prompt-enhancing heuristics to the user's raw input.
    Returns a richer, more structured intermediate prompt.
    """
    p = prompt
    p = add_clarity(p)
    p = add_context(p)
    p = define_output_format(p)
    p = add_examples(p)
    p = request_step_by_step(p)
    p = add_quality_instructions(p)
    return p.strip()


def polish_with_gemini(enhanced_prompt: str) -> str:
    """
    Sends the intermediate enhanced prompt to Gemini and asks it to polish the prompt itself —
    not answer it. Returns Gemini's revised version of the prompt.
    """
    polishing_instruction = (
        "Below is a user prompt. Improve the clarity, specificity, and structure of the prompt. "
        "Do not answer the prompt. Only return the revised version of the prompt, ready for input into an AI assistant."
        "\n\nPrompt:\n"
    )

    final_input = polishing_instruction + enhanced_prompt
    response = model.generate_content(final_input)
    return response.text.strip()


def get_boosted_prompt(prompt: str) -> str:
    """
    Complete boosting flow: takes raw user prompt, applies heuristics, then has Gemini polish it.
    Returns final, ready-to-copy improved prompt.
    """
    enhanced = enhance_prompt(prompt)
    polished = polish_with_gemini(enhanced)
    return polished