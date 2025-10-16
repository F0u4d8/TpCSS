export interface UserResponse {
id: number;
email: string;
}

export interface RegisterRequest {
username?: string;    
email: string;
password: string;
}

export interface LoginRequest {
email: string;
password: string;
}

export interface AuthResponse {
message: string;
user?: UserResponse;
}
