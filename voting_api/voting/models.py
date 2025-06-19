from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Voter(models.Model):
    name = models.CharField(max_length=101)
    email = models.EmailField(unique=True)
    has_voted = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"

    # Función especifica para el panel de administración de Django
    def clean(self):
        # Verificar que el votante no sea también candidato
        if Candidate.objects.filter(email=self.email).exists():
            raise ValidationError("Una persona no puede ser votante y candidato a la vez")

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    votes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-votes', 'name']

    def __str__(self):
        return f"{self.name} - {self.party or 'Independiente'}"

    # Función especifica para el panel de administración de Django
    def clean(self):
        # Verificar que el candidato no sea también votante
        if Voter.objects.filter(email=self.email).exists():
            raise ValidationError("Una persona no puede ser candidato y votante a la vez")

class Vote(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE, related_name='vote')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='received_votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['voter']

    def __str__(self):
        return f"{self.voter.name} votó por {self.candidate.name}"

    def save(self, *args, **kwargs):
        # Marcar al votante como que ya ha votado
        if not self.pk:  # Solo en creación
            self.voter.has_voted = True
            self.voter.save()
            
            # Incrementar contador de votos del candidato
            self.candidate.votes += 1
            self.candidate.save()
        
        super().save(*args, **kwargs)