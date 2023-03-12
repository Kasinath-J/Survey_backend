import openai

def summarizer_fn(ans):
    
    openai.api_key = "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"
    text=""
    for t in ans:   
        text+=t
    
    length = 40
    model_engine = "text-davinci-002"
    prompt = (f"Summarize the following text in {length} words or fewer: "
            f"{text}")
    completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=length, n=1,stop=None,temperature=0.5)
    summary = completions.choices[0].text

    return summary