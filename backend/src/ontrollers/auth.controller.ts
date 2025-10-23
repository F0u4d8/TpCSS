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

      const user = await authService.register({ username,email, password });

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





   async getProfile(req: Request, res: Response): Promise<void> {
    try {
      // In Phase 1, we trust the userId from the request
      // ⚠️ Anyone can claim to be any user!
      const userId = parseInt(req.params.id);

      if (isNaN(userId)) {
        res.status(400).json({ error: 'Invalid user ID' });
        return;
      }

      const user = await authService.getUserById(userId);

      if (!user) {
        res.status(404).json({ error: 'User not found' });
        return;
      }

      res.json({ 
        user,
        warning: '⚠️ Phase 1: Backend cannot verify this request is from the actual user!'
      });
    } catch (error) {
      console.error('Profile error:', error);
      res.status(500).json({ error: 'Failed to get profile' });
    }
  }

  /**
   * Get all users (admin-like endpoint)
   * ⚠️ INSECURE: No authorization check!
   */
  async getAllUsers(req: Request, res: Response): Promise<void> {
    try {
      const users = await authService.getAllUsers();
      res.json({ 
        users,
        warning: '⚠️ Phase 1: Anyone can access this - no authorization!'
      });
    } catch (error) {
      console.error('Get users error:', error);
      res.status(500).json({ error: 'Failed to get users' });
    }
  }
}
