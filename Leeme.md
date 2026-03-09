# Sistema de Registro Médico ("AppFinalPro")

Este proyecto es la entrega final de programación en Python. Es una aplicación orientada a registrar, buscar y exportar datos del personal médico y áreas de guardia. Para la interfaz gráfica utilizamos la librería `customtkinter` y para el almacenamiento de datos usamos una base de datos local `SQLite`.

## ⚙️ ¿Qué necesitas para ejecutarlo?

Asegúrate de tener Python (versión 3.x) instalado en tu computadora. Luego sigue estos pasos para instalar los paquetes necesarios:

### Paso 1 — Abrir la terminal

- En **Windows**: Presiona `Win + R`, escribe `cmd` y presiona Enter. También puedes buscar **"Símbolo del sistema"** o **"PowerShell"** en el menú Inicio.
- Otra opción: dentro de la carpeta del proyecto, haz clic en la barra de direcciones del Explorador de archivos, escribe `cmd` y presiona Enter. Esto abrirá la terminal ya posicionada en la carpeta correcta.

### Paso 2 — Instalar los paquetes

Con la terminal abierta, escribe el siguiente comando y presiona Enter:

```bash
pip install customtkinter pandas docxtpl openpyxl Pillow
```

Espera a que termine la descarga e instalación de todos los paquetes. Verás mensajes de progreso y al final aparecerá `Successfully installed ...`.

## Estructura del Proyecto

Organizamos el proyecto en varias carpetas para estructurarlo mejor:

*   `codigo/`: Contiene los módulos de Python.
    *   `principal.py`: Es el archivo principal. Ejecútalo para abrir el programa.
    *   `basededatos.py`: Se encarga de conectarse a la base de datos para consultar o guardar la información.
    *   `documentos.py`: Es el encargado de generar y exportar los reportes en Word y Excel.
    *   `ui_login.py`: Interfaz de la pantalla de inicio de sesión.
    *   `ui_menu.py`: Interfaz de botones del menú principal.
    *   `ui_formulario.py`: Interfaz del formulario de registros y búsquedas.
*   `bases_de_datos/`: Carpeta donde se almacena la información relacional de la aplicación.
    *   `database_final.db`: Este es el archivo real de la base de datos.
*   `imagenes/`: Los fondos de la interfaz (`fondo_app.jpg`, etc).
*   `plantilla.docx`: Un documento base de Word que el programa utiliza para generar automáticamente los expedientes.
*   `Leeme.md`: Este manual de usuario.

## 🚀 ¿Cómo se usa?

1. Verifica que en tu carpeta del proyecto tengas todo esto guardado manteniendo la estructura original.
2. Abre la terminal posicionada dentro de la carpeta raíz del proyecto (la carpeta que contiene `codigo/`, `bases_de_datos/`, etc.). Si no lo hiciste en el Paso 1 anterior, puedes hacerlo desde el Explorador de archivos: haz clic en la barra de direcciones, escribe `cmd` y presiona Enter.
3. Ejecuta el programa con este comando:
   ```bash
   python codigo/principal.py
   ```
   En pocos segundos se abrirá la ventana de la aplicación.
4. Las credenciales de acceso por defecto asignadas al Administrador son: usuario **admin**, clave **admin**.

---

## 📖 Manual Práctico

### 📝 1. Agregar a un residente nuevo
- Entra a **"📝 Nuevo Registro"**.
- Rellena todos los campos. Al escribir la fecha o la cédula el sistema valida automáticamente para evitar que ingreses letras donde van números.
- Presiona **"💾 GUARDAR"** y el sistema confirmará la creación del registro.

### 🔍 2. Editar, Buscar o Borrar registros
- En el menú principal, ve a la opción **"🔍 Buscar y Gestionar"**.
- Arriba a la derecha hay una barra de búsqueda: escribe un nombre o cédula y abajo te aparecerán coincidencias. Selecciona a la persona que buscas.
- El formulario en pantalla se llenará automáticamente con sus datos actuales.
- Modifica los campos que necesites y presiona **"💾 ACTUALIZAR CAMBIOS"**.
- Si iniciaste sesión como Administrador, tendrás un botón rojo extra que dice **"ELIMINAR"** por si deseas borrar permanentemente a ese usuario del sistema.

### 📄 3. Sacar un documento Word
Para generar e imprimir el expediente consolidado:
- Busca a la persona en el sistema (Paso 2) para que todos sus datos particulares carguen en pantalla.
- Selecciona el botón naranja **"📄 WORD"**.
- El sistema procesará la información, abrirá nuestra `plantilla.docx`, la rellenará y generará un documento nuevo (ej: `Expediente_1234567.docx`) listo para la impresión.

### 📂 4. Exportar resúmenes a Excel
Para generar un reporte general con toda la nómina, ve a la pantalla inicial del sistema y haz clic en **"📂 Exportar a Excel"**. El programa creará un documento general de registros y lo guardará en la carpeta `bases_de_datos` con el nombre `Reporte_General_Residentes.xlsx`.

### 💾 5. Respaldo (Backup) de la Base de Datos
Para el control de registros es clave respaldar la información. Con el rol de Administrador tendrás visible el botón: **"💾 Crear Respaldo (Backup)"**. Úsalo para guardar una copia íntegra de toda la base de datos en una ubicación externa elegida (ej. Flash Drive USB).
* **Restauración de base de datos:**
  En caso de migración o formateo del equipo de uso, pega el archivo de repaldo que posees desde de tu unidad física a la carpeta `bases_de_datos` de la instalación nueva del software, y **modifica el nombre del archivo a `database_final.db`** (reemplazando cualquier archivo idéntico que estuviese allí previamente o borrándolo). Al abrir el programa nuevamente, la información se cargará con total normalidad.

### 💡 Atajos
- El botón **"🧹 LIMPIAR TODO"** limpia los campos para empezar el ingreso de un registro desde cero.
- Ante dudas con el flujo de información, presiona el botón amarillo **"❓ AYUDA"** dentro del formulario.

---

## 🛠️ Plan de Mantenimiento del Sistema

Para garantizar que este proyecto se mantenga sustentable y funcional a largo plazo, debe aplicarse este plan logístico:

1. **Mantenimiento Preventivo (Rutina Semanal):**
   *   **Creación de Backups (Respaldos):** Una o dos veces a la semana, ejecutar la herramienta de Respaldo en la aplicación y descargar la base de datos a una unidad extraíble portátil. Esto prevendrá pérdidas masivas de información en escenarios de daño al hardware base.
   *   **Almacenamiento Virtual:** Ademas del resguardo físico, se sugiere agendar rutinas para subir los respaldos clave a servicios nube, como Google Drive / OneDrive.

2. **Mantenimiento Correctivo (Rutina Mensual/Semestral):**
   *   **Auditoría de Documentos:** Corroborar cada ciertas semanas que las exportaciones en formato Microsoft (.xlsx y .docx) mantengan total integridad de lectura y ejecución. Verificar frecuentemente que la `plantilla.docx` base no haya sufrido alteraciones gráficas causadas directamente por administradores en Windows.
   *   **Limpieza de Directorios:** Examinar la carpeta operativa `bases_de_datos`. Descartar .db residuales conservando únicamente el archivo de lectura actual (`database_final.db`) y uno o dos backups adyacentes a la fecha para no comprometer el procesamiento del ordenador base.
   *   **Actualización de Librerías:** Una vez durante el semestre, es prudente validar mediante la terminal del entorno de ejecución `pip install --upgrade customtkinter pandas docxtpl openpyxl` para importar optimizaciones inherentes a las librerías base del software.
