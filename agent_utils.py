import time

def timed_generate(client, model, prompt):
    start = time.time()
    response = client.models.generate_content(model=model, contents=prompt)
    elapsed = round(time.time() - start, 2)
    usage = response.usage_metadata
    return {
        "text": response.text,
        "elapsed_seconds": elapsed,
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
        "total_tokens": usage.total_token_count,
    }
