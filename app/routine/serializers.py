from core.models import Exercise, Routine, RoutineDay, SetRoutine,SerieRoutine,Serie
from rest_framework import serializers
from exercise.serializers import ExerciseSerializer



class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerieRoutine
        fields = ('id', 'reps', 'weight', 'comment')


class SetSerializer(serializers.ModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(
         queryset=Exercise.objects.all()
    )
    series = SerieSerializer(many=True)
    class Meta:
        model = SetRoutine
        fields = ['id','series','exercise']
        extra_keyargs = {
            "exercise":{
                "write_only":True
            }
        }

class SetDetailSerializer(SetSerializer):
    exercise= ExerciseSerializer()
    series = serializers.SerializerMethodField(
        method_name='get_series')
    def get_series(self,instance):
        serializer = SerieSerializer(SerieRoutine.objects.filter(
            father_set=instance),many=True)
        return serializer.data
     

class RoutineDaySerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True)
    class Meta:
        model = RoutineDay
        fields = ('id', 'day','sets')


class RoutineDetailSerializer(RoutineDaySerializer):
    sets = serializers.SerializerMethodField(
        method_name='get_sets')

    def get_sets(self,instance):
        serializer = SetDetailSerializer(SetRoutine.objects.filter(
            routine=instance),many=True)
        return serializer.data


class RoutineSerializer(serializers.ModelSerializer):
    routines = RoutineDaySerializer(many=True)

    class Meta:
        model = Routine
        fields = ('id', 'name', 'routines')
        read_only_fields = ('id',)

    def create(self, validated_data):
        routine_days = validated_data.pop('routines')
        routine = Routine.objects.create(name=validated_data['name'],
                                         user=self.context['request'].user)
        for routine_day in routine_days:

            sets = routine_day.pop('sets')
            routine_created = RoutineDay.objects.create(
                day=routine_day['day'], routine=routine)
            for st in sets:
                print(st)
                series = st.pop('series')
                set_created = SetRoutine.objects.create(routine=routine_created,
                                                 exercise=st['exercise'])
                for sr in series:
                    SerieRoutine.objects.create(father_set=set_created, **sr)

        return routine


class RoutineDetailSerializer(RoutineSerializer):
    routines = RoutineDetailSerializer(many=True)

    class Meta:
        model = Routine
        fields = ('id', 'name', 'routines')
        read_only_fields = ('id',)

