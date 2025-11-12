import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service';

export interface AuthenticatedRequest extends Request {
  userId?: number;
}

export const authMiddleware = async (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    // In Phase 2, we'll implement proper JWT authentication
    // For now, we'll simulate authentication by checking if a userId is provided
    // In a real implementation, we would verify a JWT token here
    
    const userId = req.headers['x-user-id'];
    
    if (!userId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const userIdNum = parseInt(userId as string, 10);
    
    if (isNaN(userIdNum)) {
      res.status(401).json({ error: 'Invalid user ID in token' });
      return;
    }

    // Verify that the user exists
    const authService = new AuthService();
    const user = await authService.getUserById(userIdNum);
    
    if (!user) {
      res.status(401).json({ error: 'User not found' });
      return;
    }

    // Add the user ID to the request object for use in subsequent handlers
    req.userId = userIdNum;
    next();
  } catch (error) {
    console.error('Authentication error:', error);
    res.status(500).json({ error: 'Authentication failed' });
  }
};

// Authorization middleware to check if the user can access a specific resource
export const authorizationMiddleware = (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): void => {
  const requestedUserId = parseInt(req.params.id, 10);

  // Check if the authenticated user is trying to access their own profile
  if (req.userId === requestedUserId) {
    next();
    return;
  }

  // For now, only allow users to access their own profiles
  // Admin functionality can be added later
  res.status(403).json({ error: 'Access denied: You can only access your own profile' });
};