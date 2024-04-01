from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TemperatureStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city_id):
        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT temperature FROM temperature WHERE city_id = %s
            """, [city_id])
            rows = cursor.fetchall()

        # Convert the result to a list of temperatures
        temperatures = [row[0] for row in rows]
        
        if temperatures:
            mean_temp = sum(temperatures) / len(temperatures)
            max_temp = max(temperatures)
            min_temp = min(temperatures)
            return Response({'mean': mean_temp, 'max': max_temp, 'min': min_temp})
        else:
            return Response({'message': 'No temperature readings found for the specified city.'}, status=404)
