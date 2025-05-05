from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

escolha_funcao = (
    ('ADM', 'Administrador'),
    ('D', 'Diretor'), # Cargo de gestor: Permissão total 
    ('P', 'Professor'), # Professores: pode alterar os alunos -> não pode alterar próprio horario ou informações 
    ('E', 'Estudante') # Apenas visualiza
)

"""
Ideia básica: escada hierarquica, os diretores controlam tudo, os professores os alunos, e os alunos apenas visualizam. 
"""

class Usuario (AbstractUser):
    telefone = models.CharField(max_length=100, null=True, blank=True)
    genero = models.CharField(max_length=100, choices=(('M', 'Masculino'), ('F', 'Feminio'), ('N', 'Neutro')), null=True, blank=True)
    situacao = models.CharField(max_length=100, choices=(('Ef', 'Efetivo'), ('Es','Estagio'), ('Mo','Meio-Oficial'), ('Ap','Aprendiz')), null=True, blank=True)
    cargo = models.CharField(max_length=100, choices=escolha_funcao, default='')
    data_nasc = models.DateTimeField(null=True, blank=True)
    data_contra = models.DateTimeField(null=True, blank=True)
    ni = models.CharField(max_length=100, default='') # Numero de identificação
    REQUIRED_FIELDS = ['cargo', 'situacao']

    
    def __str__(self):
        return self.nome

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

    
    def __str__(self):
        return f'{self.sala_reservada} - {self.get_periodo_display()} ({self.data_ini} a {self.data_fim})'