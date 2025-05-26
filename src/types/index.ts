export interface User {
    id: string;
    username: string;
    password: string;
    role: 'admin' | 'doctor' | 'patient';
}

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface SignUpDetails {
    username: string;
    password: string;
    confirmPassword: string;
    role: 'doctor' | 'patient';
}