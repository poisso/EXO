from translator.api import GPT, Example, set_openai_key

def ask_gpt(text):
    set_openai_key("sk-HAwwF1i4u6XZp4dTJETVBYnIRz7n1Uuix5ZlrkAd")

    with open('translator/data/training_exo.txt') as f:
        examples = f.read().split(sep="\n")

    gpt = GPT(input_prefix="I asked my lawyer what this passage means: ",
              output_prefix="Here it how he rephrased it in plain English: ",
              engine="davinci",
              temperature=0.50,
              max_tokens=100)

    for ex in range(0, len(examples) // 2, 2):
        gpt.add_example(Example(examples[ex],
                                examples[ex + 1]))

    return gpt.get_top_reply(text)