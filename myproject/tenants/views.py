from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tenant
from .serializers import TenantSerializer
import os
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseForbidden

@api_view(['GET'])
def tenant_detail(request, pk):
  try:
    tenant = Tenant.objects.get(pk=pk)
  except Tenant.DoesNotExist:
    return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)
  
  serializer = TenantSerializer(tenant)
  return Response(serializer.data)

def get_config(request, tenant_id):
  config_path = os.path.join(settings.BASE_DIR, 'configs', f'tenant_{tenant_id}_config.json')

  if not os.path.exists(config_path):
    return JsonResponse({'error': 'Config not found'}, status=404)

  with open(config_path) as config_file:
    config_data = json.load(config_file)

  return JsonResponse(config_data)

def tenant_page(request, tenant_id):
  config_path = os.path.join(settings.BASE_DIR, 'configs', f'tenant_{tenant_id}_config.json')

  if not os.path.exists(config_path):
    return JsonResponse({'error': "Config not found"}, status=404)
  with open(config_path) as config_file:
    config_data = json.load(config_file)
    if config_data.get("enable_custom_page"):
      return HttpResponse(config_data.get("page_title"))
    else:
      return HttpResponseForbidden('Custom page is disabled for this tenant.')