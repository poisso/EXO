from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .decorators import user_session_cap

from .gpt import *

from django.conf import settings

def index(request):
    ## if the dic key doesn't yet exist it is created and init with
    ## the second argument of the function
    num_visit = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visit
    if num_visit < 700:
        return render(request, "translator/index.html")
    else:
        return HttpResponse(str(num_visit))


# def result(request):
#     text = request.GET["text"]
#
#     answer = ask_gpt(text)
#
#     return render(request, "translator/result.html", {"text":answer})

@login_required
@user_session_cap
def result(request):
    text = request.GET["text"]

    with open("translator/data/examples_exo.txt") as f:
        examples = f.readlines()

    # test = "Subject to your compliance with these Conditions of Use and any Service Terms, and your payment of any " \
    #        "applicable fees, Amazon or its content providers grant you a limited, non-exclusive, non-transferable, " \
    #        "non-sublicensable license to access and make personal and non-commercial use of the Amazon Services. "

    gpt = GPT(engine='davinci',
              temperature=0,
              max_tokens=100,
              frequency_penalty=1,
              input_prefix="Legalese:",
              input_suffix="\n",
              output_prefix="Plain English:",
              output_suffix="\n\n",
              append_output_prefix_to_query=True)

    inputs = [examples[i][:-1] for i in range(0, 8, 2)]
    outputs = [examples[i][:-1] for i in range(1, 9, 2)]

    for i in range(4):
        gpt.add_example(Example(inputs[i], outputs[i]))

    set_openai_key(settings.API_KEY)

    answer = gpt.get_top_reply(text)

    return render(request, "translator/result.html", {"text":answer})

def about(request):
    return render(request, "translator/about.html")

def contact(request):
    return render(request, "translator/contact.html")