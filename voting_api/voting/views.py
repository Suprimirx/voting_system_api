from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from rest_framework import viewsets, status
from .models import Voter, Candidate, Vote
from .serializer import VoterSerializer, CandidateSerializer, VoteSerializer, VoteStatisticsSerializer
# Create your views here.
class VoterViewSet(viewsets.ModelViewSet):

    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    
    def destroy(self, request, *args, **kwargs):
        voter = self.get_object()
        
        # Si el votante ya votó, no se puede eliminar
        if voter.has_voted:
            return Response(
                {"error": "No se puede eliminar un votante que ya ha emitido su voto"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)
    
class CandidateViewSet(viewsets.ModelViewSet):

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    
    def destroy(self, request, *args, **kwargs):
        candidate = self.get_object()
        
        # Si el candidato tiene votos, no se puede eliminar
        if candidate.votes > 0:
            return Response(
                {"error": "No se puede eliminar un candidato que ya tiene votos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)
    
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    http_method_names = ['get', 'post']  # Solo GET y POST

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Estadísticas generales
        total_votes = Vote.objects.count()
        total_voters = Voter.objects.count()
        voters_who_voted = Voter.objects.filter(has_voted=True).count()
        
        participation_rate = 0
        if total_voters > 0:
            participation_rate = round((voters_who_voted / total_voters) * 100, 2)

        # Resultados por candidato
        candidates_results = []
        candidates = Candidate.objects.all().order_by('-votes')
        
        for candidate in candidates:
            percentage = 0
            if total_votes > 0:
                percentage = round((candidate.votes / total_votes) * 100, 2)
            
            candidates_results.append({
                'id': candidate.id,
                'name': candidate.name,
                'party': candidate.party,
                'votes': candidate.votes,
                'percentage': percentage
            })

        statistics_data = {
            'total_votes': total_votes,
            'total_voters': total_voters,
            'voters_who_voted': voters_who_voted,
            'participation_rate': participation_rate,
            'candidates_results': candidates_results
        }

        serializer = VoteStatisticsSerializer(statistics_data)
        return Response(serializer.data)