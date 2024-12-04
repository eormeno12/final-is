import unittest
import json
from app import app, data

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar el cliente de pruebas
        cls.app = app.test_client()
        app.config['TESTING'] = True
      
    # ----------------------------
    # Prueba de Caso de Éxito
    # ----------------------------
    
    def test_add_contact_success(self):
        """
        Verifica que se añade un nuevo contacto exitosamente.
        """
        payload = {
            "contacto": "user2",
            "nombre": "User 2"
        }
        response = self.app.post('/mensajeria/contactos/user1',
                                 json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]['alias'], 'user2')
        
        # Verificar que el contacto se añadió correctamente en los datos
        user1 = next((u for u in data['users'] if u['alias'] == 'user1'), None)
        self.assertIsNotNone(user1)
        self.assertEqual(len(user1['contacts']), 1)
        self.assertEqual(user1['contacts'][0]['alias'], 'user2')

    # ----------------------------
    # Pruebas de Casos de Error
    # ----------------------------
    
    def test_add_contact_already_exists(self):
        """
        Intenta añadir un contacto que ya existe y espera un error 400.
        """
        # Añadir primero el contacto
        payload = {
            "contacto": "user2",
            "nombre": "User 2"
        }
        self.app.post('/mensajeria/contactos/user1',
                      json=payload)
        
        # Intentar añadir el mismo contacto nuevamente
        response = self.app.post('/mensajeria/contactos/user1',
                                 json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("The contact is already in the contacts list", response.get_data(as_text=True))

    def test_add_contact_non_existing_user(self):
        """
        Intenta añadir un contacto para un usuario que no existe y espera un error 404.
        """
        # Payload para añadir un contacto a un usuario inexistente
        payload = {
            "contacto": "user2",
            "nombre": "User 2"
        }
        response = self.app.post('/mensajeria/contactos/nonexistent_user',
                                 json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("The user does not exist.", response.get_data(as_text=True))

    def test_send_message_receiver_not_in_contacts(self):
        """
        Intenta enviar un mensaje a un receptor que no está en la lista de contactos y espera un error 400.
        """
        # Intentar enviar un mensaje sin que 'user2' esté en los contactos de 'user1'
        message_payload = {
            "usuario": "user1",
            "contacto": "user2",
            "mensaje": "Hola, User 2!"
        }
        response = self.app.post('/mensajeria/enviar',
                                 json=message_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("The receiver is not in the contacts list", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()