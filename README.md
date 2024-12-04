# Examen Final - IS
---

## Integrantes
---
* Ernesto Ormeño
* Esteban Sulca

## Pregunta 3
---

**Se requiere realizar un cambio en el software para adicionar una validación del máximo número de contactos y la eliminación de contactos y de usuarios (considerar que los mensajes ya enviados a contactos que serán eliminados deben mantenerse).**

**Qué cambiaría en el código (Clases / Métodos) - No implementación.**

Para adicionar una validación del máximo número de contactos, reestructuraría los contactos de un usuario de esta manera:

```
contacts: {
	count: int,
	list: Contact[]
}
```

Así, cada vez que se agregue un contacto se sumaría 1, y cuando se elimine se restaría 1. También, cada vez que se agregue se validaría que tenga menos contactos que el límite. 

Por otro lado, para eliminar contactos y usuarios manteniendo los mensajes ya eliminados, aplicaría una eliminación lógica. Agregaría un atributo isDeleted que inicialmente está en False y cuando se “elimina” pasa a True. De igual manera, cada vez que se trabaje con contactos y usuarios debería validarse que el isDeleted sea False. 


**Nuevos casos de prueba a adicionar**
* Se debería adicionar 3 casos de pruebas sobre contactos: uno cuando “count” es menor que el máximo permitido, otro cuando lo alcanza y otro cuando lo supera. 
* Respecto a la eliminación de contactos y usuarios. Debería agregarse un caso de prueba sobre enviar un mensaje a un contacto eliminado, lo cual no debería permitirse. Al igual que ver los contactos o enviar un mensaje desde un usuario eliminado. 

**¿Cuánto riesgo hay de “romper” lo que ya funciona?**
El mayor riesgo está en la gestión de la eliminación de usuarios y contactos. Aquí el riesgo es medio, ya que si no se ajustan correctamente las condicionales sobre las eliminaciones, podría enviarse un mensaje desde un usuario o contacto eliminado. Por otra parte, sobre el máximo de contactos permitidos, si este falla, no es un error catastrófico, por lo que el riesgo es bajo. 
