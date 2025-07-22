import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI root
});

// Attach token automatically (if present)
api.interceptors.request.use((cfg) => {
  const token = localStorage.getItem("token");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

export default api;

/* Convenience wrappers */
export const register = (email: string, password: string) =>
  api.post("/user/register", { email, password });

export const requestRegistration = (email: string, password: string) =>
  api.post("/user/request-registration", { email, password });

export const confirmRegistration = (email: string, otp: string) =>
  api.post("/user/confirm-registration", { email, otp });

export const login = (email: string, password: string) =>
  api.post(
    "/user/login",
    new URLSearchParams({ username: email, password }), // OAuth2PasswordRequestForm
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
  );

export const uploadProfile = (form: FormData) =>
  api.post("/profile/", form);

export const savePersonalInfo = (data: Record<string, unknown>) =>
  api.post("/personal-info/", data);

export const uploadResume = (form: FormData) =>
  api.post("/personal-info/resume", form);

export const fetchProfile = () => api.get("/profile/");

export const requestPasswordReset = (email: string) =>
  api.post("/user/request-password-reset", { email });

export const verifyOtp = (email: string, otp: string) =>
  api.post("/user/verify-otp", { email, otp });

export const resetPassword = (email: string, otp: string, password: string) =>
  api.post("/user/reset-password", { email, otp, password });
