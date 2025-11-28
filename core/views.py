from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from django.contrib import messages

#Local imports
from core.forms import *
from .utils import *

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
def dados_pessoais(request):
    template_name = 'commons/include/dados_pessoais.html'

    usuario = request.user

    if request.method == 'POST':
        form = DadosPssForm(request.POST or None)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.usuario = usuario
                obj.save()

                messages.success(request, 'Cadastro atualizado!')
                return redirect('solic_pesq')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro: {e}')
    else:
        form = DadosPssForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)

@login_required
def solic_pesquisa(request):
    template_name = 'commons/include/solic_pesquisa.html'

    # dados_pessoais = DadosPessoais.objects.filter(usuario=request.user)
    MembroEquipeFormset = inlineformset_factory(
        DadosSolicPesquisa, MembroEquipe, form=MembroEquipeForm,
        extra=1, can_delete=True
    )

    prefix = 'membros'

    usuario = request.user.id
    dados_pss = DadosPessoais.objects.filter(usuario=usuario).first()

    if dados_pss == None:
        return redirect('dados_pessoais')

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

def pesquisas_solic(request):
    template_name = 'commons/include/pesquisas_solic.html'

    objs = DadosSolicPesquisa.objects.all().order_by('data_solicitacao')

    context = {
        'objs': objs
    }

    return render(request, template_name, context)

def info_pesquisa(request, id):
    template_name = 'commons/include/info_pesquisa.html'

    obj = DadosSolicPesquisa.objects.filter(id=id)
    documentos = ArquivosRelFinal.objects.filter(pesquisa=obj.first())

    form = Arq_Rel_Form(request.POST or None, request.FILES or None)

    for x in obj:
        inicio = x.inicio_atividade
        final = x.final_atividade

    duracao_pesq = calcular_data(str(inicio), str(final))

    if request.method == 'POST':
        if form.is_valid():
            arq_pesquisa = form.save(commit=False)
            arq_pesquisa.pesquisa = obj.first()

            caminho_doc = str(arq_pesquisa.documento)
            caminho_doc = caminho_doc.split('.')
            doc_type = caminho_doc[-1]

            if doc_type != 'pdf':
                messages.error(request, 'Arquivos aceitos apenas em formato pdf!')
                return redirect('info_pesquisa', id)

            #Salva o arquivo
            arq_pesquisa.save()

            messages.success(request, 'Arquivo anexado com sucesso!')
            return redirect('info_pesquisa', id)
        else:
            print(f"Erros do form: {form.errors}")
            messages.error(request, 'Erro ao tentar salvar!')

    context = {
        'obj': obj,
        'documentos': documentos,
        'duracao_pesq': duracao_pesq,
    }

    return render(request, template_name, context)

def excluir_arq(request, id):

    pesquisa = DadosSolicPesquisa.objects.filter(id=id).first()
    if request.method == 'POST':
        documento_id = request.POST.get('documento_id')

        if documento_id:
            try:
                arquivo = ArquivosRelFinal.objects.get(id=documento_id)
                if pesquisa:

                    documentos_associados = ArquivosRelFinal.objects.filter(id=documento_id)
                    for doc in documentos_associados:
                        doc.delete_documento()
                    # pesquisa.delete()

                arquivo.delete_documento()

                messages.success(request, 'Arquivo Excluido com sucesso!')
            except ArquivosRelFinal.DoesNotExist:
                messages.error(request, 'Documento não encontrado!')

    return redirect('info_pesquisa', id)