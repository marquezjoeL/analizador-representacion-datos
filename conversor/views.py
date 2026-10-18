from django.shortcuts import render

from .utils import analizar_cadena_utf8, convertir_numero


def index(request):
    contexto = {"accion": "", "numero": "", "base": "10", "texto": ""}
    if request.method == "POST":
        accion = request.POST.get("accion", "")
        contexto["accion"] = accion
        if accion == "convertir":
            valor = request.POST.get("numero", "")
            contexto["numero"] = valor
            contexto["base"] = request.POST.get("base", "10")
            try:
                base = int(contexto["base"])
                contexto["conversion"] = convertir_numero(valor, base)
            except (TypeError, ValueError) as error:
                contexto["error_numero"] = str(error)
        elif accion == "analizar":
            texto = request.POST.get("texto", "")
            contexto["texto"] = texto
            try:
                contexto["analisis"] = analizar_cadena_utf8(texto)
            except (TypeError, ValueError) as error:
                contexto["error_texto"] = str(error)
        else:
            contexto["error_general"] = "Selecciona una acción válida."
    return render(request, "conversor/index.html", contexto)
