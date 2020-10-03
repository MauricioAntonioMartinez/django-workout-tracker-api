
import datetime as dt
from collections.abc import Iterable

from core.models import Serie, Set, Workout
from exercise.views import Auth
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (SerieSerializer, SetDetailSerializer, SetSerializer,
                          WorkoutSerializer)


class WorkoutViewSet(Auth):
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all()


class SerieViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SerieSerializer
    queryset = Serie.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            father_set__work_out__user=self.request.user)

    def perform_create(self, serializer):
        _set = int(self.request.query_params.get('set'))
        if not _set or not isinstance(_set, int):
            raise ValidationError('Invalid set')
        try:
            set_fetched = Set.objects.get(
                id=_set, work_out__user=self.request.user)
            serializer.save(father_set=set_fetched)
        except Set.DoesNotExist:
            raise ValidationError('Set Not Found')


class SetViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = SetSerializer
    queryset = Set.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _get_workout(self, date, creation=True):
        try:
            real_date = dt.datetime.strptime(date, '%Y-%m-%d')
            return Workout.objects.get(
                workout_date=real_date, user=self.request.user)
        except Workout.DoesNotExist:
            if creation:
                return Workout.objects.create(workout_date=real_date,
                                              user=self.request.user)
            return False
        except (ValueError, TypeError):
            return False

    def perform_create(self, serializer):
        date = self.request.query_params.get('date')
        exercise = serializer.validated_data['exercise']
        work_out = self._get_workout(date)
        if (not work_out) or (exercise.user != self.request.user):
            raise ValidationError('Permission Error')
        serializer.save(
            work_out=work_out,
            exercise=exercise)

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'create' or self.action == 'partial_update':
            return self.serializer_class
        return SetDetailSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        work_out = self._get_workout(date, False)
        if not work_out:
            return []
        return self.queryset.filter(work_out=work_out)
