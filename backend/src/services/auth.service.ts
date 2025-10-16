import prisma from '../config/database';
import { RegisterRequest, LoginRequest, UserResponse } from '../types/auth.types';

export class AuthService {
/**

Register a new user

⚠️ INSECURE: Storing plaintext password (Phase 1 only)
*/
async register(data: RegisterRequest): Promise<UserResponse> {
const { username,email, password } = data;


// Check if user already exists

const existingUser = await prisma.user.findUnique({
  where: { email },
});

if (existingUser) {
  throw new Error('EMAIL_EXISTS');
}

// Create user with plaintext password (INSECURE - Phase 1)
const user = await prisma.user.create({
  data: {
    email,
    password, // ⚠️ Plaintext password
  },
});

return {
  id: user.id,
  email: user.email,
};
}

/**

Login user

⚠️ INSECURE: Plaintext password comparison (Phase 1 only)
*/
async login(data: LoginRequest): Promise<UserResponse> {
const { email, password } = data;


// Find user

const user = await prisma.user.findUnique({
  where: { email },
});

if (!user) {
  throw new Error('INVALID_CREDENTIALS');
}

// Compare plaintext passwords (INSECURE - Phase 1)
if (user.password !== password) {
  throw new Error('INVALID_CREDENTIALS');
}

return {
  id: user.id,
  email: user.email,
};
}

/**

Get user by ID
*/
async getUserById(id: number): Promise<UserResponse | null> {
const user = await prisma.user.findUnique({
where: { id },
});


if (!user) {

  return null;
}

return {
  id: user.id,
  email: user.email,
};
}
}