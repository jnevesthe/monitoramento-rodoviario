
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import DeleteView
#Josemar Neves
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from .models import Proprietario, Veiculo, Multa



class List(LoginRequiredMixin, ListView):
    model=Veiculo
    template_name='list.html'
    context_object_name="veiculos"
    login_url='login'

    
def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=authenticate(request,username=username, password=password)
        
        if(user):
            login(request, user)
            #print(user.autorizado)
            return redirect('list')                    
            
    return render(request, 'login.html')     
    
def logout_view(request):
    logout(request) 
    return redirect('login')
def pagina_404(request, exception=None):
    return render(request, '404.html', status=404)     


@login_required
def multar(request , pk):
    if request.method=='POST':
        foto = request.FILES.get('foto')
        valor=request.POST.get('valor')
        local=request.POST.get('local')
        tipo = request.POST.get('tipo_infracao')
        try:
          velocidade = request.POST.get('velocidade') # Virá vazio se não for excesso de velocidade
        except:
          velocidade=0
        if tipo == "sinal_vermelho":
            valor = 5000
                        
        print("ok")

        multa=Multa.objects.create(
            veiculo=Veiculo.objects.filter(id=pk).first(),
            foto=foto,
            valor=valor,
            localizacao=local,
            data=timezone.now(),
            tipo=tipo,
	    velocidade=velocidade,
            agente=request.user,
            confirmada=False
   	    
        )

        #m=Multa.objects.filter(id=multa.id)
        return redirect('confirm', multa.id)


    v=Veiculo.objects.filter(id=pk).first()
    return render(request,'multar.html',{'v':v})
    


def confirm(request, pk):
    multa=get_object_or_404(Multa, id=pk)
    return render(request, 'confirm.html', {'multa':multa})


@login_required
def confirmar_multa(request, pk):
    multa = get_object_or_404(Multa, id=pk)

    multa.confirmada = True
    multa.save()

    return redirect('list')


    
class Delete(LoginRequiredMixin, DeleteView):
    model=Multa
    template_name='delete.html'
    context_object_name='multa'
    success_url=reverse_lazy('listb')
    login_url='login'

    def dispatch(self, request, *args, **kwargs):
        multa = self.get_object()

        if multa.confirmada:
            return redirect('list_c')  # 🚫 bloqueia delete

        return super().dispatch(request, *args, **kwargs)


class Detail(LoginRequiredMixin, DetailView):
    model = Veiculo
    template_name = "detail.html"
    context_object_name = "veiculo"    
    login_url='login'



import requests
from django.http import JsonResponse


def get_view(request):
    if request.method == "POST":
        tipo_busca = request.POST.get("tipo_busca")
        matricula = ""

        if tipo_busca == "texto":
            # Busca simples por texto
            matricula = request.POST.get("matricula", "").strip().upper()
        
        elif tipo_busca == "foto":
            # Busca por imagem
            foto = request.FILES.get("foto")
            if foto:
                print("OK")
                try:
                  
                    api_key = 'a8c272060a88957'  # sua chave OCR.Space
                    response = requests.post(
                        'https://api.ocr.space/parse/image',
                        files={'file': foto},       # aceita InMemoryUploadedFile
                        data={'apikey': api_key, 'language': 'por'}
                )

        # Converte a resposta em JSON
                    result = response.json()

        # Extrai o texto
                    try:
                        texto = result['ParsedResults'][0]['ParsedText']
                    except (KeyError, IndexError, TypeError):
                        texto = ''

        # Limpa apenas letras e números
                    matricula = texto.strip().upper()
                except Exception as e:
                    print(e)
                    return render(request, "get.html", {"erro": "Erro ao processar a imagem."})
            else:
                return render(request, "get.html", {"erro": "Nenhuma foto foi enviada."})

        # Processamento comum para ambos os casos
        if matricula:
            veiculo = Veiculo.objects.filter(matricula__icontains=matricula).first()

            if veiculo:
                # Se encontrou, redireciona para a página de detalhes/lista
                return redirect('lista', pk=veiculo.id)
            else:
                return render(request, "get.html", {
                    "erro": f"Nenhum veículo encontrado para a matrícula: {matricula}"
                })
        else:
            return render(request, "get.html", {"erro": "Não foi possível identificar a matrícula."})

    return render(request, "get.html")




@login_required
def listb(request):
    # select_related busca o proprietário (ForeignKey)
    # prefetch_related busca todas as multas associadas (Related Name)
    veiculos = Veiculo.objects.select_related('proprietario').prefetch_related('multas').all()
    
    return render(request, 'listb.html', {'veiculos': veiculos})


@login_required
def logout_confirm(request):
    return render(request, 'logout_confirm.html')



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Veiculo, Multa
from .serializers import MultaSerializer
import hashlib

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_multar2(request):

    # ---------------- FOTO ----------------
    if 'foto' not in request.FILES:
        return Response({'erro': 'Foto obrigatória'}, status=400)

    try:
        arquivo = request.FILES.get('foto')
    except Exception as e:
        return Response({'erro': 'Falha ao ler arquivo da foto', 'detalhes': str(e)}, status=500)

    # ---------------- DADOS OPCIONAIS ----------------
    velocidade = request.data.get('velocidade')
    tipo = request.data.get('tipo_infracao', 'desconhecido')
    local = request.data.get('local', 'Radar automático')
    valor = request.data.get('valor', 10000)

    # converte velocidade
    if velocidade:
        try:
            velocidade = float(velocidade)
        except ValueError:
            velocidade = None
    else:
        velocidade = None

    # ---------------- OCR ----------------
    try:
        

    # envia a imagem direto para OCR.Space
        api_key = 'a8c272060a88957'  # sua chave gratuita OCR.Space
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'file': arquivo},  # arquivo já em bytes
            data={'apikey': api_key, 'language': 'por'}
        )

        result = response.json()

        try:
            texto = result['ParsedResults'][0]['ParsedText']
        except (KeyError, IndexError, TypeError):
            texto = ''

        matricula = texto.strip().upper()
    except Exception as e:
        matricula = None

    if not matricula:
        matricula = "N/A"

    # ---------------- PROCURAR VEÍCULO ----------------
    veiculo = None
    if matricula != "N/A":
        try:
            veiculo = Veiculo.objects.filter(matricula__icontains=matricula).first()
        except:
            veiculo = None

    if not veiculo:
        veiculo = None  # mantém None se não encontrou

    # ---------------- HASH 32 ----------------
    try:
        hash_input = arquivo + str(timezone.now()).encode()
        if matricula:
            hash_input += matricula.encode()
        hash_id = hashlib.md5(hash_input).hexdigest()
    except:
        hash_id = None

    # ---------------- CRIAR MULTA ----------------
    try:
        multa = Multa.objects.create(
            veiculo=veiculo,
            foto=arquivo,
            valor=valor,
            localizacao=local,
            data=timezone.now(),
            tipo=tipo,
            velocidade=velocidade,
            agente="admin",
            confirmada=False
        )
    except Exception as e:
        return Response({'erro': 'Falha ao criar multa', 'detalhes': str(e)}, status=500)

    serializer = MultaSerializer(multa)

    # ---------------- RESPOSTA ----------------
    return Response({
        'status': 'ok',
        'matricula_detectada': matricula,
        'hash_id': hash_id,
        'multa': serializer.data
    })




from PIL import Image
import hashlib
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_multar3(request):

    # ---------------- FOTO ----------------
    if 'foto' not in request.FILES:
        return Response({'erro': 'Foto obrigatória'}, status=400)

    arquivo = request.FILES.get('foto')

    # ---------------- DADOS ----------------
    velocidade = request.data.get('velocidade')
    tipo = request.data.get('tipo_infracao', 'desconhecido')
    local = request.data.get('local', 'Radar automático')
    valor = request.data.get('valor', 10000)


    # converter velocidade
    try:
        velocidade = float(velocidade) if velocidade else None
    except:
        velocidade = None

    # ---------------- DETECÇÃO DE COR ----------------
    try:
        img = Image.open(arquivo).convert("RGB")
        img = img.resize((100, 100))

        r_total = g_total = b_total = 0
        pixels = 0

        for r, g, b in img.getdata():
            r_total += r
            g_total += g
            b_total += b
            pixels += 1

        if r_total > g_total and r_total > b_total:
            cor = "R"
        elif g_total > r_total and g_total > b_total:
            cor = "G"
        else:
            cor = "B"

    except:
        cor = "B"

    # ---------------- MATRÍCULA POR COR ----------------
    matricula = None

    if cor == "R":
        matricula = "LD-45-04-FH"

    elif cor == "G":
        matricula = "LD-45-04-EG"

    else:  # B
        matricula = "LD-45-04-EG"
    try:
        veiculo = Veiculo.objects.filter(matricula__icontains=matricula).first()
        
    except:
        veiculo = None

    # ---------------- HASH ----------------
    try:
        arquivo_bytes = arquivo.read()
        arquivo.seek(0)

        hash_input = arquivo_bytes + str(timezone.now()).encode() + matricula.encode()
        hash_id = hashlib.md5(hash_input).hexdigest()

    except:
        hash_id = None

    # ---------------- MULTA ----------------
    try:
        multa = Multa.objects.create(
            veiculo=veiculo,
            foto=arquivo,
            valor=valor,
            localizacao=local,
            data=timezone.now(),
            tipo=tipo,
            velocidade=velocidade,
            agente="admin",
            confirmada=False
        )
    except Exception as e:
        return Response({'erro': 'Falha ao criar multa', 'detalhes': str(e)}, status=500)

    return Response({
        "status": "ok",
        "cor_detectada": cor,
        "matricula_usada": matricula,
        "hash_id": hash_id
    })




import random


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_multar24(request):

    # ---------------- FOTO ----------------
    if 'foto' not in request.FILES:
        return Response({
            'erro': 'Foto obrigatória'
        }, status=400)

    arquivo = request.FILES.get('foto')

    # ---------------- DADOS ----------------
    velocidade = request.data.get('velocidade')
    tipo = request.data.get('tipo_infracao', 'desconhecido')
    local = request.data.get('local', 'Radar automático')
    valor = request.data.get('valor', 10000)

    # ---------------- VELOCIDADE ----------------
    try:
        velocidade = float(velocidade) if velocidade else None
    except:
        velocidade = None

    # ---------------- MATRÍCULA RANDOM ----------------
    numero = random.randint(0, 2)

    if numero == 0:
        matricula = "LD-45-04-FH"

    elif numero == 1:
        matricula = "LD-45-04-EG"

    else:
        matricula = "LD-45-04-AB"
    try:
        veiculo = Veiculo.objects.filter(matricula__icontains=matricula).first()
        
    except:
        veiculo = None

    # ---------------- HASH ----------------
    try:
        arquivo_bytes = arquivo.read()
        arquivo.seek(0)

        hash_input = (
            arquivo_bytes +
            str(timezone.now()).encode() +
            matricula.encode()
        )

        hash_id = hashlib.md5(hash_input).hexdigest()

    except:
        hash_id = None

    # ---------------- MULTA ----------------
    try:
        multa = Multa.objects.create(
            veiculo=veiculo,
            foto=arquivo,
            valor=valor,
            localizacao=local,
            data=timezone.now(),
            tipo=tipo,
            velocidade=velocidade,
            agente="admin",
            confirmada=False
        )

    except Exception as e:
        return Response({
            'erro': 'Falha ao criar multa',
            'detalhes': str(e)
        }, status=500)

    # ---------------- RESPOSTA ----------------
    return Response({
        "status": "ok",
        "matricula_usada": matricula,
        "hash_id": hash_id
    })



import random
import hashlib
import io
from PIL import Image, ImageOps

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile


def espelhar_e_recortar(arquivo, faixa):
    """
    1. Espelha a imagem horizontalmente.
    2. Recorta:
       - faixa1 → metade esquerda  (lado do condutor, pós-espelho)
       - faixa2 → metade direita
    Devolve um InMemoryUploadedFile pronto para salvar no model.
    """
    img = Image.open(arquivo)
    img = ImageOps.mirror(img)           # espelho horizontal

    largura, altura = img.size
    metade = largura // 2

    if faixa == "faixa1":
        box = (0, 0, metade, altura)     # esquerda
    else:
        box = (metade, 0, largura, altura)  # direita (faixa2 ou qualquer outro valor)

    img = img.crop(box)

    # Serializa de volta para JPEG em memória
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    return InMemoryUploadedFile(
        buffer,
        field_name="foto",
        name="foto.jpg",
        content_type="image/jpeg",
        size=buffer.getbuffer().nbytes,
        charset=None,
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_multar132(request):

    # ---------------- FOTO ----------------
    if 'foto' not in request.FILES:
        return Response({'erro': 'Foto obrigatória'}, status=400)

    arquivo = request.FILES.get('foto')

    # ---------------- DADOS ----------------
    velocidade = request.data.get('velocidade')
    tipo       = request.data.get('tipo_infracao', 'desconhecido')
    local      = request.data.get('local', 'Radar automático')
    valor      = request.data.get('valor', 10000)
    faixa      = request.data.get('faixa', 'faixa1')   # novo campo

    # ---------------- VELOCIDADE ----------------
    try:
        velocidade = float(velocidade) if velocidade else None
    except:
        velocidade = None

    # ---------------- ESPELHAR E RECORTAR ----------------
    try:
        arquivo = espelhar_e_recortar(arquivo, faixa)
    except Exception as e:
        return Response({'erro': 'Falha ao processar imagem', 'detalhes': str(e)}, status=500)

    # ---------------- MATRÍCULA RANDOM ----------------
    

    if faixa == "faixa1":
        matricula = "LD-45-04-FH"
    elif faixa == "faixa2":
        matricula = "LD-45-04-EG"
    else:
        matricula = "LD-45-04-AB"

    try:
        veiculo = Veiculo.objects.filter(matricula__icontains=matricula).first()
    except:
        veiculo = None

    # ---------------- HASH ----------------
    try:
        arquivo_bytes = arquivo.read()
        arquivo.seek(0)

        hash_input = (
            arquivo_bytes +
            str(timezone.now()).encode() +
            matricula.encode()
        )

        hash_id = hashlib.md5(hash_input).hexdigest()
    except:
        hash_id = None

    # ---------------- MULTA ----------------
    try:
        multa = Multa.objects.create(
            veiculo=veiculo,
            foto=arquivo,
            valor=valor,
            localizacao=local,
            data=timezone.now(),
            tipo=tipo,
            velocidade=velocidade,
            agente="admin",
            confirmada=False
        )
    except Exception as e:
        return Response({'erro': 'Falha ao criar multa', 'detalhes': str(e)}, status=500)

    # ---------------- RESPOSTA ----------------
    return Response({
        "status": "ok",
        "matricula_usada": matricula,
        "hash_id": hash_id
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_multar0(request):

    # ---------------- FOTO ----------------
    if 'foto' not in request.FILES:
        return Response({'erro': 'Foto obrigatória'}, status=400)

    arquivo = request.FILES.get('foto')

    # ---------------- DADOS ----------------
    velocidade = request.data.get('velocidade')
    tipo       = request.data.get('tipo_infracao', 'desconhecido')
    local      = request.data.get('local', 'Radar automático')
    valor      = request.data.get('valor', 10000)
    faixa      = request.data.get('faixa', 'faixa1')

    # ---------------- VELOCIDADE ----------------
    try:
        velocidade = float(velocidade) if velocidade else None
    except:
        velocidade = None

    # ---------------- ESPELHAR E RECORTAR ----------------
    try:
        arquivo = espelhar_e_recortar(arquivo, faixa)
    except Exception as e:
        return Response({'erro': 'Falha ao processar imagem', 'detalhes': str(e)}, status=500)

    # ---------------- DETEÇÃO DE COR ----------------
    try:
        img = Image.open(arquivo)
        pixels = np.array(img.convert("RGB").resize((50, 50)), dtype=float)
        r = pixels[:, :, 0].mean()
        g = pixels[:, :, 1].mean()
        b = pixels[:, :, 2].mean()

        if r > 150 and r > g * 1.4 and r > b * 1.4:
            cor = "vermelho"
            matricula = "LD-45-04-FH"
        elif b > 100 and b > r * 1.3 and b > g * 1.1:
            cor = "azul"
            matricula = "LD-45-04-EG"
        else:
            cor = "outro"
            matricula = "LD-45-04-AB"

        arquivo.seek(0)  # reset após leitura do PIL
    except:
        cor = "outro"
        matricula = "LD-45-04-AB"

    # ---------------- VEÍCULO ----------------
    try:
        veiculo = Veiculo.objects.filter(matricula__icontains=matricula).first()
    except:
        veiculo = None

    # ---------------- HASH ----------------
    try:
        arquivo_bytes = arquivo.read()
        arquivo.seek(0)

        hash_input = (
            arquivo_bytes +
            str(timezone.now()).encode() +
            matricula.encode()
        )

        hash_id = hashlib.md5(hash_input).hexdigest()
    except:
        hash_id = None

    # ---------------- MULTA ----------------
    try:
        multa = Multa.objects.create(
            veiculo=veiculo,
            foto=arquivo,
            valor=valor,
            localizacao=local,
            data=timezone.now(),
            tipo=tipo,
            velocidade=velocidade,
            agente="admin",
            confirmada=False
        )
    except Exception as e:
        return Response({'erro': 'Falha ao criar multa', 'detalhes': str(e)}, status=500)

    # ---------------- RESPOSTA ----------------
    return Response({
        "status": "ok",
        "matricula_usada": matricula,
        "cor_detetada": cor,
        "hash_id": hash_id
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_multar(request):

    # ---------------- FOTO ----------------
    if 'foto' not in request.FILES:
        return Response({'erro': 'Foto obrigatória'}, status=400)

    arquivo = request.FILES.get('foto')

    # ---------------- DADOS ----------------
    velocidade = request.data.get('velocidade')
    tipo       = request.data.get('tipo_infracao', 'desconhecido')
    local      = request.data.get('local', 'Radar automático')
    valor      = request.data.get('valor', 10000)
    faixa      = request.data.get('faixa', 'faixa1')

    # ---------------- VELOCIDADE ----------------
    try:
        velocidade = float(velocidade) if velocidade else None
    except:
        velocidade = None

    # ---------------- ESPELHAR E RECORTAR ----------------
    try:
        arquivo = espelhar_e_recortar(arquivo, faixa)
    except Exception as e:
        return Response({'erro': 'Falha ao processar imagem', 'detalhes': str(e)}, status=500)

    # ---------------- DETEÇÃO DE COR ----------------
    try:
        arquivo_bytes = arquivo.read()
        arquivo.seek(0)

        img = Image.open(io.BytesIO(arquivo_bytes))
        pixels = np.array(img.convert("RGB").resize((50, 50)), dtype=float)
        r = pixels[:, :, 0].mean()
        g = pixels[:, :, 1].mean()
        b = pixels[:, :, 2].mean()

        if r > 70 and r > g * 0.9 and r > b * 0.9:
            cor = "vermelho"
            matricula = "LD-45-04-FH"
        elif b > 60 and b > r * 0.7 and b > g * 0.7:
            cor = "azul"
            matricula = "LD-45-04-EG"
        else:
            cor = "outro"
            matricula = "LD-45-04-AB"
    except:
        cor = "outro"
        matricula = "LD-45-04-AB"

    # ---------------- VEÍCULO ----------------
    try:
        veiculo = Veiculo.objects.filter(matricula__icontains=matricula).first()
    except:
        veiculo = None

    # ---------------- HASH ----------------
    try:
        arquivo_bytes = arquivo.read()
        arquivo.seek(0)

        hash_input = (
            arquivo_bytes +
            str(timezone.now()).encode() +
            matricula.encode()
        )

        hash_id = hashlib.md5(hash_input).hexdigest()
    except:
        hash_id = None

    # ---------------- MULTA ----------------
    try:
        multa = Multa.objects.create(
            veiculo=veiculo,
            foto=arquivo,
            valor=valor,
            localizacao=local,
            data=timezone.now(),
            tipo=tipo,
            velocidade=velocidade,
            agente="admin",
            confirmada=False
        )
    except Exception as e:
        return Response({'erro': 'Falha ao criar multa', 'detalhes': str(e)}, status=500)

    # ---------------- RESPOSTA ----------------
    return Response({
        "status": "ok",
        "matricula_usada": matricula,
        "cor_detetada": cor,
        "hash_id": hash_id
    })
