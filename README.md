# FactRed - Sistema de Gestión ISP 🚀

FactRed es una plataforma moderna diseñada para proveedores de servicios de internet (ISP) que gestionan clientes, facturación y monitoreo de red en entornos con Starlink, MikroTik y Fortinet.

![Login](Login.png)

## ✨ Características Principales

### 📊 Dashboard Interactivo

- **Monitoreo en Tiempo Real**: Visualización de estado de Interfaces, CPU y Uptime de nodos MikroTik y Fortigate.
- **Estadísticas de Facturación**: Total por cobrar y facturas vencidas.
- **Clientes Activos**: Conteo y variación mensual.
- **Diseño**: Interfaz corporativa en Dark Mode con fondo dinámico interactivo.

![Dashboard](Dashboard.png)

### 👥 Gestión de Clientes

- **CRUD Completo**: Crear, editar y eliminar suscriptores.
- **Asignación de IP**: Control de direcciones IP para clientes en su respectivo segmento.
- **Estado de Servicio**: Activación/Suspensión automatizada y visual.
- **Alertas**: Notificaciones simuladas de cobro por WhatsApp (🔔).

![Gestión de Clientes](Clientes.png)

### 🔌 Gestión de Switches y Nodos

- **Administración Centralizada**: Control de equipos de red (MikroTik, Fortinet).
- **Despliegue Automático**: Inyección de reglas de corte y redirección de morosos directamente por SSH con un solo clic.

![Gestión de Switches](Gestion%20Switches.png)

### 💰 Facturación Inteligente

- **Tasa BCV Automática**: Integración con **DolarAPI (`ve.dolarapi.com`)** para obtener la tasa oficial del día en tiempo real.
- **Emisión de Facturas**: Generación automática basada en los planes contratados.
- **Ejecución de Cortes**: Suspensión masiva de clientes con facturas vencidas.

![Facturación](Facturacion.png)

---

## 🛠️ Stack Tecnológico

Este proyecto utiliza tecnologías de vanguardia para garantizar rendimiento y escalabilidad:

| Componente        | Tecnología                                                                                                    | Descripción                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| **Frontend** | ![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=flat&logo=vuedotjs&logoColor=4FC08D)               | Vue 3 + Vite + TypeScript         |
| **Estilos** | ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) | Utility-first CSS Framework       |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)                               | Python API de alto rendimiento    |
| **Base de Datos** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)      | Persistencia robusta (SQLAlchemy) |
| **Visuales** | `tsparticles`                                                                                                 | Efectos de fondo interactivos     |

---

## ⚙️ Instalación y Despliegue

### Requisitos Previos

- Node.js 18+
- Python 3.9+
- PostgreSQL

### 1. Clonar el repositorio

```bash
git clone [https://github.com/kingcells22/FactRed-v1.0.git](https://github.com/kingcells22/FactRed-v1.0.git)
cd FactRed-v1.0

cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

DATABASE_URL=postgresql://usuario:password@localhost:5432/factred

python -m uvicorn main:app --reload

cd frontend
npm install
npm run dev

🔒 Acceso (Demo)
Usuario: admin

Contraseña: admin


