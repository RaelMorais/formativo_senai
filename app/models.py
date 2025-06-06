from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your models here.

escolha_funcao = (
    ('ADM', 'Administrador'),
    ('D', 'Diretor'), # Cargo de gestor: Permissão total 
    ('P', 'Professor') # Professores: pode alterar os alunos -> não pode alterar próprio horario ou informações  
)

"""
Ideia básica: escada hierarquica, os diretores controlam tudo, os professores os alunos, e os alunos apenas visualizam. 
"""

class Usuario (AbstractUser):
    username = models.CharField(max_length=150, unique=True, validators=[RegexValidator(regex=r'^[\w.@+-áéíóúàèìòùãõâêîôûçÇÁÉÍÓÚÀÈÌÒÙÃÕÂÊÎÔÛ\s]+$',message='Use apenas letras, números, espaços e símbolos permitidos.')]),
    telefone = models.CharField(max_length=100, null=True, blank=True)
    genero = models.CharField(max_length=100, choices=(('M', 'Masculino'), ('F', 'Feminio'), ('N', 'Neutro')), null=True, blank=True)
    situacao = models.CharField(max_length=100, choices=(('Ef', 'Efetivo'), ('Es','Estagio'), ('Mo','Meio-Oficial'), ('Ap','Aprendiz')), null=True, blank=True)
    cargo = models.CharField(max_length=100, choices=escolha_funcao, default='')
    data_nasc = models.DateTimeField(null=True, blank=True)
    data_contra = models.DateTimeField(null=True, blank=True)
    ni = models.CharField(max_length=100, default='', unique=True, null=True) # Numero de identificação
    REQUIRED_FIELDS = ['ni', 'cargo', 'situacao']

    
    def __str__(self):
        return self.username

# Para cadastro de disciplinas 
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    carga_horaria = models.PositiveIntegerField()
    desc = models.CharField(max_length=100)
    professor = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class Sala(models.Model):
    nome = models.CharField(max_length=255, default='')
    capacidade = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.nome



# Para reserva de ambientes 
class ReservaAmbiente(models.Model):
    data_ini = models.DateField()
    data_fim = models.DateField()
    periodo = models.CharField(max_length=100, choices=(('M', 'Manhã'), ('T', 'Tarde'), ('N', 'Noite')))
    prof_resp = models.ForeignKey(Usuario, on_delete=models.CASCADE, max_length=100)
    disc = models.ForeignKey(Disciplina, on_delete=models.CASCADE, max_length=100)
    sala_reservada = models.ForeignKey(Sala, on_delete=models.CASCADE, default='')

    # feat: adicionar o horario de professor dps 
    
    # verificação no banco de dados
    def clean(self):
        prof_not_available =  ReservaAmbiente.objects.filter(
            prof_resp=self.prof_resp,
            data_fim__gt = self.data_ini,
            data_ini__lt = self.data_fim, 
            periodo=self.periodo 
        )
         # verficação para disponibilidade do professor 

        sala_not_available = ReservaAmbiente.objects.filter(
            data_fim__gt = self.data_ini,
            data_ini__lt = self.data_fim, 
            periodo=self.periodo, 
            sala_reservada = self.sala_reservada
        )

        # verificação para dispnibilidade da sala 

        if self.pk:
            sala_not_available = sala_not_available.exclude(pk=self.pk)
            prof_not_available = prof_not_available.exclude(pk=self.pk)
        
        
        # retornando as mensagens de erros 
        if sala_not_available.exists():
            raise ValidationError ('Sala já cadastrada.')
        if prof_not_available.exists():
            raise ValidationError ('Professor já existe')
        


    def save(self, *args, **kwargs):
        self.clean()
        if self.data_ini > self.data_fim:
            raise ValidationError("A data de início não pode ser posterior à data de término.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.sala_reservada} - {self.get_periodo_display()} ({self.data_ini} a {self.data_fim})'