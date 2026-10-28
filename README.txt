SUPERVISOR DE APRENDIZAJE IA — PAQUETE PARA DESPLIEGUE EN LÍNEA

Incluye:
- Interfaz web adaptable a móvil.
- Backend Flask que llama a la OpenAI Responses API.
- Protección por código de acceso de la aplicación (APP_ACCESS_TOKEN).
- La clave API se mantiene en variables de entorno del servidor, nunca en el navegador.
- Alertas heurísticas, pausa local, exportación JSON.
- Configuración para Render mediante render.yaml.

PUBLICACIÓN SENCILLA CON RENDER
1. Descarga y descomprime este ZIP.
2. Sube el contenido de la carpeta a un repositorio privado de GitHub.
3. En Render, crea un nuevo Blueprint y conecta ese repositorio.
4. Render leerá render.yaml y creará el servicio.
5. En la configuración del servicio, añade estas variables secretas:
   OPENAI_API_KEY = tu clave de API
   APP_ACCESS_TOKEN = una contraseña larga y aleatoria que tú elijas
6. Espera a que termine el despliegue. Render mostrará una URL pública HTTPS.
7. Abre esa URL desde Android e introduce APP_ACCESS_TOKEN en el campo “Código de acceso”.

SEGURIDAD Y COSTES
- No publiques tu clave API en HTML, JavaScript, GitHub ni en el chat.
- Si un repositorio incluye secretos por accidente, revoca y rota esas claves.
- La URL pública puede ser compartida, pero las consultas requieren el código de acceso.
- El código de acceso es una protección básica compartida; para uso multiusuario o comercial, agrega cuentas, límites de uso y almacenamiento seguro.
- El plan gratuito de alojamiento puede suspenderse o tener límites/cambios del proveedor.
- El uso de la API puede generar cargos según tu cuenta y modelo. Configura límites de gasto en tu plataforma API.
- Se envía store=false en la solicitud de Responses API. Revisa la documentación y las políticas del proveedor antes de enviar información sensible.
- El registro de supervisión se conserva en el navegador y no se guarda en una base de datos del servidor.
- La pausa detiene nuevas solicitudes desde la interfaz; no detiene una solicitud ya enviada ni controla el sistema remoto.

MODELO
El campo de modelo comienza con gpt-6-astra como ejemplo. Si no está habilitado en tu cuenta, sustitúyelo por un modelo al que sí tengas acceso.

ESTRUCTURA
app.py
static/index.html
requirements.txt
render.yaml
