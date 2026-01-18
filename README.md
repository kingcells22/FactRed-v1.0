# FactRed - Sistema de Gestión ISP 🚀

FactRed es una plataforma moderna diseñada para proveedores de servicios de internet (ISP) que gestionan clientes, facturación y monitoreo de red en entornos con Starlink y Mikrotik.

![Login Screen](screenshots/login.png)

## ✨ Características Principales

### 📊 Dashboard Interactivo

- **Monitoreo en Tiempo Real**: Visualización de estado de Interfaces, CPU y Uptime de nodos Mikrotik (Simulado/Mock).
- **Estadísticas de Facturación**: Total por cobrar y facturas vencidas.
- **Clientes Activos**: Conteo y variación mensual.
- **Diseño**: Interfaz moderna con fondo dinámico de partículas ("Neural Network").

![Dashboard](screenshots/dashboard.png)

### 👥 Gestión de Clientes

- **CRUD Completo**: Crear, editar y eliminar suscriptores.
- **Asignación de IP**: Control de direcciones IP para clientes (ej: `192.168.88.X`).
- **Estado de Servicio**: Activación/Suspensión visual.
- **Alertas**: Notificaciones de cobro simuladas (🔔).

![Formulario Cliente](screenshots/client_form.png)

### 💰 Facturación Inteligente (En Desarrollo)

- **Tasa BCV Automática**: Integración con **DolarAPI (`ve.dolarapi.com`)** para obtener la tasa oficial del día.
- **Emisión de Facturas**: Generación automática basada en planes.

---

## 🛠️ Stack Tecnológico

Este proyecto utiliza tecnologías de vanguardia para garantizar rendimiento y escalabilidad:

| Componente        | Tecnología                                                                                                    | Descripción                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| **Frontend**      | ![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=flat&logo=vuedotjs&logoColor=4FC08D)               | Vue 3 + Vite + TypeScript         |
| **Estilos**       | ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) | Utility-first CSS Framework       |
| **Backend**       | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)                               | Python API de alto rendimiento    |
| **Base de Datos** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)      | Persistencia robusta (SQLAlchemy) |
| **Visuales**      | `tsparticles`                                                                                                 | Efectos de fondo interactivos     |

---

## ⚙️ Instalación y Despliegue

### Requisitos Previos

- Node.js 18+
- Python 3.9+
- PostgreSQL

### 1. Clonar el repositorio

```bash
git clone https://github.com/TuUsuario/FactRed.git
cd FactRed
```

### 2. Configurar Backend

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Crea un archivo `.env` en `backend/` con:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/factred
```

Inicia el servidor:

```bash
python -m uvicorn main:app --reload
```

### 3. Configurar Frontend

```bash
cd frontend
npm install
npm run dev
```

Visita `http://localhost:5173`.

---

## 🔒 Acceso (Demo)

- **Usuario**: `admin`
- **Contraseña**: `admin`

---

Desarrollado para simplificar la gestión de redes WISP.
