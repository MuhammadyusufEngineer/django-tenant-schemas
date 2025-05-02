from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Tenant
import os
import json
from django.conf import settings

class TenantAPITestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.tenant = Tenant.objects.create(
      name = "Tests tenant",
      domain = "testtenant.com",
      config_json = {"enable_feature_x": True, "theme": "dark"}
    )
  def test_get_existing_tenant(self):
    response = self.client.get(f'/api/tenants/{self.tenant.id}/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], "Tests tenant")

  def test_get_nonexistent_tenant(self):
    response = self.client.get('/api/tenants/999/')
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertIn('error', response.data)

# class TenantViewsTestCase(TestCase):
#   def setUp(self):
#     self.client = Client()
#     self.tenant = Tenant.objects.create(name="Tenant A", domain="domain-a.com", config_json={"test": True})

#     self.tenant_id = 'a'
#     self.config_path = os.path.join(settings.BASE_DIR, 'configs', f'tenant_{self.tenant_id})config.json')
#     os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
#     with open(self.config_path, 'w') as f:
#       json.dump({'tenant_id': "a", "enable_custom_page": True, "page_title": "Welcome Tenant A"}, f)

#   def tearDown(self):
#     if os.path.exists(self.config_path):
#       os.remove(self.config_path)

#   def test_get_tenant_detail(self):
#     response = self.client.get(reverse('tenant_detail', args=[self.tenant.pk]))
#     self.assertEqual(response.status_code, 200)
#     self.assertEqual(response.data['name'], "Tenant A")

#   def test_get_config(self):
#     response = self.client.get(reverse('get_config', args=[self.tenant_id]))
#     self.assertEqual(response.status_code, 200)
#     self.assertIn("enable_custom_page", response.json())

#   def test_tenant_page_enabled(self):
#     response = self.client.get(reverse('tenant_page', args=[self.tenant_id]))
#     self.assertEqual(response.status_code, 200)
#     self.assertIn("Welcome to A", response.content.decode())

#   def test_tenant_page_disabled(self):
#         with open(self.config_path, 'w') as f:
#             json.dump({"tenant_id": "a", "enable_custom_page": False}, f)

#         response = self.client.get(reverse('tenant_page', args=[self.tenant_id]))
#         self.assertEqual(response.status_code, 403)
class TenantViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name="Tenant A", domain="tenant-a.com", config_json={"test": True})

        # Create sample config file
        self.tenant_id = "a"
        self.config_path = os.path.join(settings.BASE_DIR, 'configs', f'tenant_{self.tenant_id}_config.json')
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({"tenant_id": "a", "enable_custom_page": True, "page_title": "Welcome Tenant A"}, f)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_get_tenant_detail(self):
        response = self.client.get(reverse('tenant_detail', args=[self.tenant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Tenant A")

    def test_get_config(self):
        response = self.client.get(reverse('get_config', args=[self.tenant_id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("enable_custom_page", response.json())

    def test_tenant_page_enabled(self):
        response = self.client.get(reverse('tenant_page', args=[self.tenant_id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome Tenant A", response.content.decode())

    def test_tenant_page_disabled(self):
        # Modify config to disable custom page
        with open(self.config_path, 'w') as f:
            json.dump({"tenant_id": "a", "enable_custom_page": False}, f)

        response = self.client.get(reverse('tenant_page', args=[self.tenant_id]))
        self.assertEqual(response.status_code, 403)
