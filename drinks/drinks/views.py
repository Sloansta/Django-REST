from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def drink_list(req, format=None):

    # get all the drinks, serialize them and return json
    if req.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response({'drinks': serializer.data})
    elif req.method == 'POST':
        serializer = DrinkSerializer(data=req.data)
        if serializer.is_valid:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(req, id, format=None):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if req.method == 'GET':

        serializer = DrinkSerializer(drink)
        return Response(serializer.data)

    elif req.method == 'PUT':
        serializer = DrinkSerializer(drink, data=req.data)

        if serializer.is_valid:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    elif req.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)