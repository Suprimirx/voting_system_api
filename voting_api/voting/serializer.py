from rest_framework import serializers
from .models import Candidate, Voter, Vote

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'

    def validate_email(self, value):
        # Verificar que el email no pertenezca a un candidato
        if Candidate.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Este email ya está registrado como candidato"
            )
        return value
    
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

    def validate_email(self, value):
        # Verificar que el email no pertenezca a un votante
        if Voter.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Este email ya está registrado como votante"
            )
        return value
    
class VoteSerializer(serializers.ModelSerializer):
    voter_name = serializers.CharField(source='voter.name', read_only=True)
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    
    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, data):
        voter = data.get('voter')
        candidate = data.get('candidate')

        # Verificar que el votante existe
        if not Voter.objects.filter(id=voter.id).exists():
            raise serializers.ValidationError("Votante no encontrado")

        # Verificar que el candidato existe
        if not Candidate.objects.filter(id=candidate.id).exists():
            raise serializers.ValidationError("Candidato no encontrado")

        # Verificar que el votante no haya votado ya
        if voter.has_voted:
            raise serializers.ValidationError("Este votante ya ha emitido su voto")

        # Verificar que no existe un voto previo
        if Vote.objects.filter(voter=voter).exists():
            raise serializers.ValidationError("Este votante ya ha emitido su voto")

        return data
    
class VoteStatisticsSerializer(serializers.Serializer):
    total_votes = serializers.IntegerField()
    total_voters = serializers.IntegerField()
    voters_who_voted = serializers.IntegerField()
    participation_rate = serializers.FloatField()
    candidates_results = serializers.ListField()