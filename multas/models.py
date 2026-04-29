from django.db import models


class Proprietario(models.Model):
    nome_completo = models.CharField(max_length=150)
    cidade = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.nome_completo}"


class Veiculo(models.Model):
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE, related_name="veiculos")
    marca = models.CharField(max_length=150)
    modelo = models.CharField(max_length=150)
    cor = models.CharField(max_length=50)
    matricula = models.CharField(max_length=150, unique=True)

    foto_frontal = models.ImageField(upload_to="fotos/", blank=True, null=True)
    foto_traseira = models.ImageField(upload_to="fotos/", blank=True, null=True)
    foto_lateralE = models.ImageField(upload_to="fotos/", blank=True, null=True)
    foto_lateralD = models.ImageField(upload_to="fotos/", blank=True, null=True)

        
    def __str__(self):
        return f"{self.modelo} - {self.matricula}"


class Multa(models.Model):

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="multas")
    foto = models.ImageField(upload_to="foto/", null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    localizacao = models.CharField(max_length=200)
    data = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(blank=True)
    velocidade = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    agente = models.CharField(max_length=15, blank=True)   
    confirmada = models.BooleanField(default=False)  # 👈 NOVO CAMPO
    def __str__(self):
        return f"{self.id} - {self.valor}"
