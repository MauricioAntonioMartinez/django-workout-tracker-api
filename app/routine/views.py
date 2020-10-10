from core.models import Routine
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Workout, Set, Serie, Exercise
from django.db import transaction


from .serializers import RoutineSerializer, RoutineDetailSerializer, AddRoutineWorkout


class RoutineViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RoutineSerializer
    queryset = Routine.objects.all()

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'add_routine_workout':
            return AddRoutineWorkout
        if self.action == 'create' or self.action == 'partial_update':
            return self.serializer_class
        return RoutineDetailSerializer

    @transaction.atomic
    @action(methods=['POST'], url_path='add-workout', detail=False)
    def add_routine_workout(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                workout, _ = Workout.objects.get_or_create(workout_date=serializer.data['date'],
                                                           user=request.user)
                sets = serializer.data['sets']
                for _set in sets:
                    set_created = Set.objects.create(
                        work_out=workout, exercise=Exercise.objects.get(
                            id=_set['exercise'], user=request.user))
                    for serie in _set['series']:
                        set_created.series.create(weight=serie.weight,
                                                  reps=serie['reps'], comment=serie['comment'])
        except:
            return Response({"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Created successfully"}, status=status.HTTP_200_OK)
