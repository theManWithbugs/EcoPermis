from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from django.contrib import messages

#Local imports
from core.forms import *

def pagina_sucesso(request):
    template_name = 'commons/include/msg_pages/pagina_sucesso.html'
    return render(request, template_name)

def login_view(request):
    template_name = 'auth/login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
        except Exception as e:
            messages.error(request, f'{e}')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login ou senha incorretos!')

    return render(request, template_name)

@login_required
def perfil(request):
    template_name = 'auth/perfil.html'

    objs = DadosPessoais.objects.filter(usuario=request.user)

    return render(request, template_name, {'objs': objs})

def home(request):
    template_name = 'commons/home.html'
    return render(request, template_name)

@login_required
def solic_pesquisa(request):
    template_name = 'commons/include/solic_pesquisa.html'

    dados_pessoais = DadosPessoais.objects.filter(usuario=request.user)

    if request.method == 'POST':
        form = DadosPssForm(request.POST or None)
        form_pesquisa = DadosPesqForm(request.POST or None)
        if form.is_valid():
            pesquisa_form = form.save(commit=False)
            pesquisa_form.usuario = request.user
            pesquisa_form.save()
            return redirect('home')
    else:
        form = DadosPssForm()
        form_pesquisa = DadosPesqForm()

    context = {
        'form': form,
        'form_pesq': form_pesquisa,
        'dados_pessoais': dados_pessoais
    }

    return render(request, template_name, context)

def pagina_test(request):
    template_name = 'commons/include/pagina_test.html'

    # dados_pessoais = DadosPessoais.objects.filter(usuario=request.user)
    MembroEquipeFormset = inlineformset_factory(
        DadosSolicPesquisa, MembroEquipe, form=MembroEquipeForm,
        extra=1, can_delete=True
    )

    prefix = 'membros'

    if request.method == 'GET':
        form = DadosPesqForm()
        formset = MembroEquipeFormset(prefix=prefix)
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, template_name, context)

    # POST
    form = DadosPesqForm(request.POST)
    if form.is_valid():
        obj_paiSaved = form.save()

        formset = MembroEquipeFormset(request.POST, instance=obj_paiSaved, prefix=prefix)

        if formset.is_valid():
            formset.save()
            return redirect('pagina_sucesso')
        else:
            # formset invalid, fall through to re-render with errors
            pass
    else:
        # parent form invalid; bind formset to POST so user entries are preserved
        formset = MembroEquipeFormset(request.POST, prefix=prefix)

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template_name, context)

def pesquisas(request):
    template_name = 'commons/include/pesquisas.html'

    objs = DadosSolicPesquisa.objects.filter(status=True)

    context = {
        'objs': objs
    }

    return render(request, template_name, context)

def info_pesquisa(request, id):
    template_name = 'commons/include/info_pesquisa.html'

    obj = DadosSolicPesquisa.objects.filter(id=id)

    context = {
        'obj': obj
    }

    return render(request, template_name, context)