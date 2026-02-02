from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import JsonResponse
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives
# from decouple import config
# from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from datetime import date
from django.shortcuts import get_object_or_404

#Local imports
from core.forms import *
from .utils import *

import json

#Debug the code
# messages.error(request, f"Erros: {form.errors}")
# print((request, f"Erros: {form.errors}"))

def dados_pessoais_required(view_func):
    #usar wraps para evitar: quebrar reverse, perder o nome da view, quebrar permissões e logs
    @wraps(view_func)
    #quando alguém acessar essa URL, execute o wrapper primeiro
    def wrapper(request, *args, **kwargs):

        if not DadosPessoais.objects.filter(
            usuario=request.user.id
        ).exists():
            return redirect('dados_pessoais')

        #Caso o if não seja executado retorna o objeto request e os parametros da view
        #return view_func(request) → executa a view
        #A view só roda se o wrapper permitir
        return view_func(request, *args, **kwargs)

    return wrapper

def is_staff(user):
    return user.is_staff

def login_view(request):
    template_name = 'auth/login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Caso não exista vai retornar None
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                login(request, user)
                return redirect('home')
            except Exception as e:
                messages.error(request, f'{e}')
        else:
            messages.error(request, 'Login ou senha incorretos!')

    return render(request, template_name)

def logoutView(request):
    auth_logout(request)
    return redirect('login')

@login_required
@dados_pessoais_required
def perfil(request):
    template_name = 'auth/perfil.html'

    objs = DadosPessoais.objects.filter(usuario=request.user)

    return render(request, template_name, {'objs': objs})

@login_required
def editar_perfil(request, id):
    template_name = 'auth/alt_dados.html'

    dados = get_object_or_404(DadosPessoais, usuario=id)

    if request.method == 'POST':
        form = DadosPssForm(request.POST or None, instance=dados)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alteração realizada com sucesso!')
            return redirect('perfil')
    else:
        form = DadosPssForm(instance=dados)

    context = {
        'id': id,
        'form': form
    }

    return render(request, template_name, context)

#------------------------------------------------------------------------#
#------------------------------------------------------------------------#

@login_required
def home(request):
    template_name = 'commons/home.html'
    return render(request, template_name)

#------------------------------------------------------------------------#
#------------------------------------------------------------------------#

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

                messages.success(request, 'Informações atualizadas com sucesso!')
                return redirect('realizar_solic')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro: {e}')
    else:
        form = DadosPssForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)

def api_pesq_aprov(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Usuario não autenticado!'},
            status=401
        )

    # Filtra apenas registros com status=False
    dados = DadosSolicPesquisa.objects.filter(status=True)

    paginator = Paginator(dados, 5)

    # Número da página vindo da query string (?page=)
    # vem do request recebido
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Converte os objetos em dicionários incluindo o campo id
    itens_json = []
    for item in page_obj.object_list:
        d = model_to_dict(item)
        d['id'] = str(item.id)  # UUID convertido para string
        itens_json.append(d)

    # Retorna os dados em formato JSON
    return JsonResponse({
        'items': itens_json,
        'currentPage': page_obj.number,
        'totalPages': paginator.num_pages,
        'hasNext': page_obj.has_next(),
        'hasPrevious': page_obj.has_previous(),
    })

def api_pesq_n_aprovadas(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Usuario não autenticado!'},
            status=401
        )

    #Dessa vez filtra pelo items com status = false
    dados = DadosSolicPesquisa.objects.filter(status=False).order_by('data_solicitacao')

    paginator = Paginator(dados, 5)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    itens_json = []
    for item in page_obj.object_list:
        d = model_to_dict(item)
        d['id'] = str(item.id)
        itens_json.append(d)

    # Retorna os dados em formato JSON
    return JsonResponse({
        'items': itens_json,
        'currentPage': page_obj.number,
        'totalPages': paginator.num_pages,
        'hasNext': page_obj.has_next(),
        'hasPrevious': page_obj.has_previous(),
    })

#Utilização de UGAI
#------------------------------------------------------------------------#
#------------------------------------------------------------------------
def api_ugai_solicitadas(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Usuario não autenticado!'},
            status=401
        )

    dados = SolicitacaoUgais.objects.filter(status=False).order_by('data_solicitacao')

    paginator = Paginator(dados, 5)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    itens_json = []
    for item in page_obj.object_list:
        d = model_to_dict(item)
        d['id'] = str(item.id)
        itens_json.append(d)

    return JsonResponse({
        'items': itens_json,
        'currentPage': page_obj.number,
        'totalPages': paginator.num_pages,
        'hasNext': page_obj.has_next(),
        'hasPrevious': page_obj.has_previous(),
    })

@login_required
def info_solic_ugai(request, id):
    template_name = 'commons/include/ugais/info_solic_ugai.html'

    usuario = request.user.id
    dados_pss = DadosPessoais.objects.filter(usuario=usuario).first()

    if dados_pss == None:
        return redirect('dados_pessoais')

    solic_ugai = SolicitacaoUgais.objects.filter(id=id)

    context = {
        'obj': solic_ugai
    }

    return render(request, template_name, context)

@login_required
@user_passes_test(is_staff, login_url='permission_denied')
def aprov_uso_ugai(request, id):

    username = request.user.username

    if request.method == 'POST':
        try:
            # SolicitacaoUgais.objects.filter(id=id).update(status=True)
            obj = get_object_or_404(SolicitacaoUgais, id=id)
            obj.status = True
            obj.save()

            messages.success(request, 'Solicitação aprovada com sucesso!')
            email_ugai_aprov(request, username)

        except SolicitacaoUgais.DoesNotExist:
            messages.error(request, 'Solicitação de UGAI não encontrada.')

        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {e}')

    return redirect('info_solic_ugai', id)
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#

#Solicitação de pesquisa
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
@login_required
@dados_pessoais_required
def realizar_solic(request):
    template_name = 'commons/realizar_solic.html'

    # dados_user = DadosPessoais.objects.filter(usuario=request.user).first()
    dados_user = get_object_or_404(DadosPessoais, usuario=request.user)

    MembroEquipeFormset = inlineformset_factory(
            DadosSolicPesquisa, MembroEquipe, form=MembroEquipeForm,
            extra=1, can_delete=True
        )

    #Declaração de variaveis locais
    prefix = 'membros'
    form_solic = DadosPesqForm()
    formset = MembroEquipeFormset(prefix=prefix)
    form_ugai = Solic_Ugai()

    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'solic_pesq':
            user = request.user

            # POST
            form_solic = DadosPesqForm(request.POST)
            if form_solic.is_valid():
                obj_paiSaved = form_solic.save(commit=False)
                obj_paiSaved.user_solic = user
                obj_paiSaved.save()

                formset = MembroEquipeFormset(request.POST, instance=obj_paiSaved, prefix=prefix)

                if formset.is_valid():
                    try:
                        formset.save()
                        messages.success(request, 'Pesquisa solicitada com sucesso!')

                        data = format_data_br(str(obj_paiSaved.data_solicitacao))
                        username = request.user.username
                        acao_realizada = obj_paiSaved.acao_realizada

                        email_solic_ugai(request, username, acao_realizada, data)
                        return redirect('info_pesquisa', obj_paiSaved.id)
                    except Exception as e:
                        messages.error(request, f'ocorreu um erro: {e}')
                else:
                    messages.error(request, f"Erro: {formset.errors}")
            else:
                # parent form invalid; bind formset to POST so user entries are preserved
                formset = MembroEquipeFormset(request.POST, prefix=prefix)
                # print((request, f"Erros: {form_solic.errors}"))

        elif form_type == 'aut_ugai':
            form_ugai = Solic_Ugai(request.POST or None)

            user = request.user

            if form_ugai.is_valid():
                obj = form_ugai.save(commit=False)
                id_ugai = obj.id
                obj.user_solic = user
                try:
                    obj.save()
                    messages.success(request, 'Solicitação efetuada com sucesso!')

                    data_hoje = date.today()
                    data_br = data_hoje.strftime('%d/%m/%Y')

                    username = request.user.username
                    ativ_desenv = obj.ativ_desenv

                    email_solic_ugai(request, username, ativ_desenv, data_br)
                    return redirect('info_solic_ugai', id_ugai)
                except Exception as e:
                    messages.error(request, f'ocorreu um erro: {e}')
            else:
                messages.error(request, f"Erros: {form_ugai.errors}")

    context = {
        'form_solic': form_solic,
        'formset': formset,
        'form_ugai': form_ugai,
        'dados_user': dados_user,
    }

    return render(request, template_name, context)

@login_required
def info_pesquisa(request, id):
    template_name = 'commons/include/nav_pesquisas/info_pesquisa.html'

    obj = DadosSolicPesquisa.objects.filter(id=id)
    documentos = ArquivosRelFinal.objects.filter(pesquisa=obj.first())
    membro_equip = MembroEquipe.objects.filter(pesquisa=obj.first())

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
        'membro_equip': membro_equip,
    }

    return render(request, template_name, context)

#Only action
@login_required
def excluir_arq(request, id):

    # pesquisa = DadosSolicPesquisa.objects.filter(id=id).first()
    pesquisa = get_object_or_404(DadosSolicPesquisa, id=id)
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

@login_required
@user_passes_test(is_staff, login_url='permission_denied')
def aprovar_pesquisa(request, id):

    username = request.user.username

    if request.method == 'POST':
        try:
            obj = get_object_or_404(DadosSolicPesquisa, id=id)
            obj.status = True
            obj.save()
            messages.success(request, 'Pesquisa aprovada com sucesso!')

            #Email to user
            email_pesq_aprov(request, username)

        except DadosSolicPesquisa.DoesNotExist:
            messages.error(request, 'Pesquisa não encontrada.')

        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {e}')

    return redirect('info_pesquisa', id)

#Solicitações de pesquisas por parte do usuario
@login_required
def minhas_solic(request):
    template_name = 'commons/include/nav_pesquisas/minhas_solic.html'

    user = request.user.id
    pesq_user = DadosSolicPesquisa.objects.filter(user_solic=user)

    contador_pesq = 0
    for x in pesq_user: contador_pesq+=1

    ugais_solic = SolicitacaoUgais.objects.filter(user_solic=user)

    contador_ugai = 0
    for x in ugais_solic: contador_ugai+=1

    context = {
        'pesquisas': pesq_user,
        'quant_pesq': contador_pesq,

        'ugais': ugais_solic,
        'quant_ugai': contador_ugai
    }

    return render(request, template_name, context)
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
@login_required
def listar_solicitacoes(request):
    template_name = 'commons/listar_solic.html'
    return render(request, template_name)

@login_required
def realizar_busca(request):
    template_name = 'commons/search.html'
    return render(request, template_name)

def resp_get_years(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Usuario não autenticado!'},
            status=401
        )

    if request.method == 'GET':
        years = SolicitacaoUgais.objects.values('data_solicitacao__year')

        resultado = []
        for x in years:
            if x not in resultado:
                resultado.append(x)

        return JsonResponse({
            'mensagem': 'mensagem enviada com sucesso!',
            'years': resultado
        })


    if request.method == 'POST':
        data = json.loads(request.body)
        year = data.get('year')

        objs = SolicitacaoUgais.objects.filter(data_solicitacao__year=year)

        paginator = Paginator(objs, 5)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        itens_json = []
        for item in objs:
            d = model_to_dict(item)
            d['id'] = str(item.id)
            itens_json.append(d)

        return JsonResponse({
            'mensagem': 'mensagem enviada com sucesso! (POST)',
            'objs': itens_json,
            'currentPage': page_obj.number,
            'totalPages': paginator.num_pages,
            'hasNext': page_obj.has_next(),
            'hasPrevious': page_obj.has_previous()
        })

#-------------------------------------------------------------------#

@login_required
def render_teste_page(request):
    template_name = 'commons/include/test_filter_resp.html'
    return render(request,template_name)

def get_page_by_year(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Usuario não autenticado!'},
            status=401
        )

    if request.method == 'GET':
        year = request.GET.get('year')
        page = request.GET.get('page')

        objs = SolicitacaoUgais.objects.all()

        if year:
            objs = SolicitacaoUgais.objects.filter(data_solicitacao__year=year)

        paginator = Paginator(objs, 5)
        page_obj = paginator.get_page(page)

        years = SolicitacaoUgais.objects.values('data_solicitacao__year')

        resultado = []
        for x in years:
            if x not in resultado:
                resultado.append(x)

        return JsonResponse({
            'results': list(page_obj.object_list.values()),
            'page': page_obj.number,
            'num_pages': paginator.num_pages,
            'years': resultado
        })

    # if request.method == 'POST':
    #     data = json.loads(request.body)
    #     year = data.get('year')

    #     objs = SolicitacaoUgais.objects.filter(data_solicitacao__year=year)

    #     itens_json = []
    #     for item in objs:
    #         d = model_to_dict(item)
    #         d['id'] = str(item.id)
    #         itens_json.append(d)

    #     return JsonResponse({
    #         'objs': itens_json,
    #     })