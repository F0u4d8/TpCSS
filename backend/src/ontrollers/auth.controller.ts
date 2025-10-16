import { Request, Response } from 'express';
import { AuthService } from '../services/auth.service';
import { RegisterRequest, LoginRequest } from '../types/auth.types';

const authService = new AuthService();

export class AuthController {
  /**
   * Register endpoint handler
   */
  async register(req: Request, res: Response): Promise<void> {
    try {
      const { username,email, password } = req.body as RegisterRequest;

      if (!email || !password) {
        res.status(400).json({ error: 'Email and password required' });
        return;
      }

      const user = await authService.register({ email, password });

      res.status(201).json({
        message: 'User registered successfully',
        user,
      });
    } catch (error: any) {
      if (error.message === 'EMAIL_EXISTS') {
        res.status(409).json({ error: 'Email already exists' });
        return;
      }
      console.error('Register error:', error);
      res.status(500).json({ error: 'Registration failed' });
    }
  }

  /**
   * Login endpoint handler
   * ⚠️ INSECURE: Just returns user data, no token/session
   */
  async login(req: Request, res: Response): Promise<void> {
    try {
      const { email, password } = req.body as LoginRequest;

      if (!email || !password) {
        res.status(400).json({ error: 'Email and password required' });
        return;
      }

      const user = await authService.login({ email, password });

      // ⚠️ Phase 1: Just return user data, no authentication mechanism!
      res.json({
        message: 'Login successful',
        user,
      });
    } catch (error: any) {
      if (error.message === 'INVALID_CREDENTIALS') {
        res.status(401).json({ error: 'Invalid credentials' });
        return;
      }
      console.error('Login error:', error);
      res.status(500).json({ error: 'Login failed' });
    }
  }
}
