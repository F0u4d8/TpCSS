import { Request, Response } from 'express';
import { AuthService } from '../services/auth.service';
import { RegisterRequest, LoginRequest } from '../types/auth.types';
import { AuthenticatedRequest } from '../middleware/auth.middleware';

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
   * Phase 2: Will return user data with authentication token
   */
  async login(req: Request, res: Response): Promise<void> {
    try {
      const { email, password } = req.body as LoginRequest;

      if (!email || !password) {
        res.status(400).json({ error: 'Email and password required' });
        return;
      }

      const user = await authService.login({ email, password });

      // Phase 2: Return user data with a placeholder for proper authentication
      // In a real implementation, we would generate a JWT token here
      res.json({
        message: 'Login successful',
        user,
        // In a future implementation, we would return a JWT token
        // token: generateToken(user.id)
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





   async getProfile(req: AuthenticatedRequest, res: Response): Promise<void> {
    try {
      // The userId is now verified via middleware
      const userId = parseInt(req.params.id);

      if (isNaN(userId)) {
        res.status(400).json({ error: 'Invalid user ID' });
        return;
      }

      // Verify this is the authenticated user's profile
      if (req.userId !== userId) {
        res.status(403).json({ error: 'Access denied: You can only access your own profile' });
        return;
      }

      const user = await authService.getUserById(userId);

      if (!user) {
        res.status(404).json({ error: 'User not found' });
        return;
      }

      res.json({
        user,
        message: 'Profile retrieved successfully'
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
  async getAllUsers(req: AuthenticatedRequest, res: Response): Promise<void> {
    try {
      // For Phase 2, we'll only allow authenticated users to access this endpoint
      // In a real app, we might add role-based access control here
      
      // Note: We're not checking for admin status in this phase
      // That would be Phase 3 functionality
      
      const users = await authService.getAllUsers();
      res.json({
        users,
        message: 'Users retrieved successfully',
        authenticatedUserId: req.userId // For debugging - remove in production
      });
    } catch (error) {
      console.error('Get users error:', error);
      res.status(500).json({ error: 'Failed to get users' });
    }
  }
}
