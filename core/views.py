from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from decouple import config
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

#Local imports
from core.forms import *
from .utils import *

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

@login_required
def pagina_sucesso(request):
    template_name = 'commons/include/msg_pages/pagina_sucesso.html'
    return render(request, template_name)

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
def perfil(request):
    template_name = 'auth/perfil.html'

    objs = DadosPessoais.objects.filter(usuario=request.user)

    return render(request, template_name, {'objs': objs})

@login_required
def editar_perfil(request, id):
    template_name = 'auth/alt_dados.html'

    dados = DadosPessoais.objects.filter(usuario=id).first()

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

# @login_required
# def solic_pesquisa(request):
#     template_name = 'commons/include/solic_pesquisa.html'

#     user = request.user

#     # dados_pessoais = DadosPessoais.objects.filter(usuario=request.user)
#     MembroEquipeFormset = inlineformset_factory(
#         DadosSolicPesquisa, MembroEquipe, form=MembroEquipeForm,
#         extra=1, can_delete=True
#     )

#     prefix = 'membros'

#     # usuario = request.user.id
#     # dados_pss = DadosPessoais.objects.filter(usuario=usuario).first()

#     # if dados_pss == None:
#     #     return redirect('dados_pessoais')

#     if request.method == 'GET':
#         form = DadosPesqForm()
#         formset = MembroEquipeFormset(prefix=prefix)
#         context = {
#             'form': form,
#             'formset': formset,
#         }
#         return render(request, template_name, context)

#     # POST
#     form = DadosPesqForm(request.POST)
#     if form.is_valid():
#         obj_paiSaved = form.save(commit=False)
#         obj_paiSaved.user_solic = user
#         obj_paiSaved.save()

#         formset = MembroEquipeFormset(request.POST, instance=obj_paiSaved, prefix=prefix)

#         if formset.is_valid():

#             try:
#                 formset.save()
#                 messages.success(request, 'Pesquisa solicitada com sucesso!')

#                 data = format_data_br(str(obj_paiSaved.data_solicitacao))

#                 destinatarios = ['wilianaraujo407@gmail.com']  # pode adicionar outros
#                 assunto = "STATUS: Aguardando aprovação"

#                 # Corpo em texto simples (fallback)
#                 texto_simples = "Sua pesquisa foi solicitada com sucesso!"

#                 html_content = f"""
#                 <html>
#                 <body style="font-family: Arial, sans-serif; color: #333;">

#                     <h2 style="color:#2c3e50;">
#                         Pesquisa Solicitada com Sucesso!
#                     </h2>

#                     <p style="font-size: 15px;">
#                         <strong>Solicitante:</strong> {request.user.username}<br>
#                         <strong>Ação a ser realizada:</strong> {obj_paiSaved.acao_realizada}<br>
#                         <strong>Data da solicitação:</strong> {data}
#                     </p>

#                     <br>
#                     <p style="font-size: 14px; color:#555;">
#                         Atenciosamente,<br>
#                         <strong>SEMA - ECO Permis</strong>
#                     </p>

#                 </body>
#                 </html>
#                 """

#                 email = EmailMultiAlternatives(
#                     subject=assunto,
#                     body=texto_simples,
#                     from_email=settings.EMAIL_HOST_USER,
#                     to=destinatarios
#                 )

#                 email.attach_alternative(html_content, "text/html")
#                 email.send()
#             except Exception as e:
#                 messages.error(request, f'ocorreu um erro: {e}')


#             return redirect('info_pesquisa', obj_paiSaved.id)
#         else:
#             # formset invalid, fall through to re-render with errors
#             pass
#     else:
#         # parent form invalid; bind formset to POST so user entries are preserved
#         formset = MembroEquipeFormset(request.POST, prefix=prefix)
#         print((request, f"Erros: {form.errors}"))

#     context = {
#         'form': form,
#         'formset': formset,
#     }

#     return render(request, template_name, context)

@login_required
def pesquisas_aprovadas(request):
    template_name = 'commons/include/nav_pesquisas/pesq_aprovadas.html'
    return render(request, template_name)

@login_required
def pesquisas_n_aprovadas(request):
    template_name = 'commons/include/nav_pesquisas/pesq_n_aprov.html'
    return render(request, template_name)

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
#------------------------------------------------------------------------#
@login_required
def ugais_naprov(request):
    template_name = 'commons/include/ugais/ped_ugai_pend.html'
    return render(request, template_name)

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
@dados_pessoais_required
def solic_ugais(request):
    template_name = 'commons/include/ugais/solic_ugai.html'

    form = Solic_Ugai(request.POST or None)

    user = request.user
    usuario = request.user.id
    dados_pss = DadosPessoais.objects.filter(usuario=usuario).first()

    if dados_pss == None:
        return redirect('dados_pessoais')

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_solic = user
            obj.save()
            messages.success(request, 'Solicitação efetuada com sucesso!')
            return redirect('home')
        else:
            messages.error(request, f"Erros: {form.errors}")
    else:
        form = Solic_Ugai()

    context = {
        'form': form
    }

    return render(request, template_name, context)

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
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#

#Solicitação de pesquisa
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
@login_required
@dados_pessoais_required
def solic_pesquisa(request):
    template_name = 'commons/include/solic_pesquisa.html'

    user = request.user

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
        obj_paiSaved = form.save(commit=False)
        obj_paiSaved.user_solic = user
        obj_paiSaved.save()

        formset = MembroEquipeFormset(request.POST, instance=obj_paiSaved, prefix=prefix)

        if formset.is_valid():

            try:
                formset.save()
                messages.success(request, 'Pesquisa solicitada com sucesso!')

                data = format_data_br(str(obj_paiSaved.data_solicitacao))

                destinatarios = ['wilianaraujo407@gmail.com']  # pode adicionar outros
                assunto = "STATUS: Aguardando aprovação"

                # Corpo em texto simples (fallback)
                texto_simples = "Sua pesquisa foi solicitada com sucesso!"

                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333;">

                    <h2 style="color:#2c3e50;">
                        Pesquisa Solicitada com Sucesso!
                    </h2>

                    <p style="font-size: 15px;">
                        <strong>Solicitante:</strong> {request.user.username}<br>
                        <strong>Ação a ser realizada:</strong> {obj_paiSaved.acao_realizada}<br>
                        <strong>Data da solicitação:</strong> {data}
                    </p>

                    <br>
                    <p style="font-size: 14px; color:#555;">
                        Atenciosamente,<br>
                        <strong>SEMA - ECO Permis</strong>
                    </p>

                </body>
                </html>
                """

                email = EmailMultiAlternatives(
                    subject=assunto,
                    body=texto_simples,
                    from_email=settings.EMAIL_HOST_USER,
                    to=destinatarios
                )

                email.attach_alternative(html_content, "text/html")
                email.send()
            except Exception as e:
                messages.error(request, f'ocorreu um erro: {e}')


            return redirect('info_pesquisa', obj_paiSaved.id)
        else:
            # formset invalid, fall through to re-render with errors
            pass
    else:
        # parent form invalid; bind formset to POST so user entries are preserved
        formset = MembroEquipeFormset(request.POST, prefix=prefix)
        print((request, f"Erros: {form.errors}"))

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template_name, context)

@login_required
def pesquisas_aprovadas(request):
    template_name = 'commons/include/nav_pesquisas/pesq_aprovadas.html'
    return render(request, template_name)

@login_required
def pesquisas_n_aprovadas(request):
    template_name = 'commons/include/nav_pesquisas/pesq_n_aprov.html'
    return render(request, template_name)

def api_pesq_aprov(request):
    # Filtra apenas registros com status=False
    dados = DadosSolicPesquisa.objects.filter(status=True)

    paginator = Paginator(dados, 5)

    # Número da página vindo da query string (?page=)
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

@login_required
@user_passes_test(is_staff, login_url='permission_denied')
def aprovar_pesquisa(request, id):

    if request.method == 'POST':
        # MaterialTipo.objects.filter(id=item.id).update(saida_obj=None)
        try:
            DadosSolicPesquisa.objects.filter(id=id).update(status=True)
            messages.success(request, 'Pesquisa aprovada com sucesso!')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {e}')

    return redirect('info_pesquisa', id)

#Solicitações de pesquisas por parte do usuario
@login_required
def minhas_solic(request):
    template_name = 'commons/include/nav_pesquisas/minhas_solic.html'

    user = request.user.id
    pesq_user = DadosSolicPesquisa.objects.filter(user_solic=user)

    contador = 0
    for x in pesq_user: contador+=1

    context = {
        'pesquisas': pesq_user,
        'quant_pesq': contador
    }

    return render(request, template_name, context)
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
@login_required
def realizar_solic(request):
    template_name = 'commons/realizar_solic.html'
    return render(request, template_name)

@login_required
def listar_solicitacoes(request):
    template_name = 'commons/listar_solic.html'
    return render(request, template_name)

@login_required
def pagina_teste(request):
    template_name = 'commons/include/pagina_test.html'

    return render(request, template_name)

@login_required
def realizar_busca(request):
    template_name = 'commons/search.html'
    return render(request, template_name)
