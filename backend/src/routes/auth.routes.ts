import { Router } from 'express';
import { AuthController } from '../ontrollers/auth.controller';

const router = Router();
const authController = new AuthController();

// Health check
router.get('/health', (req, res) => {
res.json({ status: 'ok', message: 'Auth service is running' });
});

// Auth routes
router.post('/register', (req, res) => authController.register(req, res));
router.post('/login', (req, res) => authController.login(req, res));


export default router;