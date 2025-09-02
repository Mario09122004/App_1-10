from django.shortcuts import render
from . import translate

def translate_View(request):
    if request.method == "POST":
        text_to_translate = request.POST["text_to_translate"]
        output = translate.translate_text(text_to_translate)
        return render(request, 'translate.html', {'output_text': output})
    else:
        return render(request, 'translate.html')
