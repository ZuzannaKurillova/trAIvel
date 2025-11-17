# Getting Started with trAIvel

## 🎯 What You Have

Your Nx monorepo is set up with:
- **Frontend**: Angular application (mobile-responsive web app)
- **Backend**: Python FastAPI REST API

## 📁 Project Structure

```
trAIvel/
├── apps/
│   ├── frontend/          # Angular web application
│   │   ├── src/           # Source code
│   │   ├── project.json   # Nx project configuration
│   │   └── ...
│   └── backend/           # Python FastAPI backend
│       ├── main.py        # Main API file
│       ├── requirements.txt
│       ├── project.json   # Nx project configuration
│       └── README.md
├── package.json           # Node.js dependencies & scripts
├── nx.json                # Nx workspace configuration
└── README.md              # Full documentation
```

## 🚀 Quick Start

### 1. Install Dependencies

**Node.js (for frontend):**
```bash
npm install
```

**Python (for backend):**
```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../..
```

### 2. Run the Applications

**Option A: Using npm scripts**
```bash
# Terminal 1 - Frontend
npm run start:frontend

# Terminal 2 - Backend (activate venv first!)
npm run start:backend
```

**Option B: Using Nx directly**
```bash
# Terminal 1 - Frontend
nx serve frontend

# Terminal 2 - Backend
nx serve backend
```

### 3. Access Your Apps

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## 🛠️ Available Commands

### Frontend
```bash
npm run start:frontend    # Start dev server
npm run build:frontend    # Build for production
npm run test:frontend     # Run unit tests
npm run lint:frontend     # Lint code
```

### Backend
```bash
nx serve backend          # Start FastAPI server
nx install backend        # Install Python dependencies
```

## 📱 Mobile-Responsive Web App

Your Angular frontend is a **responsive web application** that works on:
- Desktop browsers
- Mobile browsers (iOS Safari, Chrome, etc.)
- Tablets

No separate mobile app needed - it's a Progressive Web App (PWA) ready setup!

## 🔗 Frontend-Backend Communication

The backend is already configured with CORS to accept requests from the frontend:
- Frontend: `http://localhost:4200`
- Backend: `http://localhost:8000`

Example API call from Angular:
```typescript
this.http.get('http://localhost:8000/api/health')
  .subscribe(data => console.log(data));
```

## 📝 Next Steps

1. **Customize the frontend**: Edit `apps/frontend/src/app/app.component.ts`
2. **Add API endpoints**: Edit `apps/backend/main.py`
3. **Add environment variables**: Copy `apps/backend/.env.example` to `.env`
4. **Explore Nx**: Run `nx graph` to visualize your workspace

## 🆘 Troubleshooting

**Frontend won't start?**
- Make sure you ran `npm install`
- Check if port 4200 is available

**Backend won't start?**
- Activate the virtual environment first
- Make sure Python 3.8+ is installed
- Check if port 8000 is available

**Need help?**
- Check the main [README.md](./README.md)
- Backend docs: [apps/backend/README.md](./apps/backend/README.md)
