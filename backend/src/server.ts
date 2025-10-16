

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.routes';
import prisma from './config/database';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);

// Global health check
app.get('/api/health', (req, res) => {
res.json({ status: 'ok', message: 'Server is running' });
});

// 404 handler
app.use((req, res) => {
res.status(404).json({ error: 'Route not found' });
});

// Graceful shutdown
process.on('SIGINT', async () => {
console.log('\n🛑 Shutting down gracefully...');
await prisma.$disconnect();
process.exit();
});

// Start server
app.listen(PORT, () => {
    console.log(' Server running on http://localhost:3000');
console.log('📊 API endpoints: http://localhost:3000/api/auth');
console.log('⚠️ WARNING: Phase 1 - INSECURE by design');
console.log('📊 Prisma Studio: npx prisma studio');
});