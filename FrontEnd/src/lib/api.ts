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

// Add response interceptor to handle authentication errors
api.interceptors.response.use(
  (response) => {
    console.log(`API Success: ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`);
    return response;
  },
  (error) => {
    console.error(`API Error: ${error.config?.method?.toUpperCase()} ${error.config?.url} - ${error.response?.status || 'Network Error'}`);
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem("token");
      window.location.href = "/signin";
    }
    return Promise.reject(error);
  }
);

export default api;

/* Convenience wrappers */
export const register = (email: string, password: string) =>
  api.post("/user/register", { user_id: email, password });

export const requestRegistration = (email: string, password: string) =>
  api.post("/user/request-registration", { user_id: email, password });

export const confirmRegistration = (email: string, otp: string) =>
  api.post("/user/confirm-registration", { user_id: email, otp });

export const login = (email: string, password: string) =>
  api.post(
    "/user/login",
    new URLSearchParams({ username: email, password }), // OAuth2PasswordRequestForm
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
  );

// Job Preferences API
export const saveJobPreferences = (data: Record<string, unknown>) =>
  api.post("/profile/job-preferences", data);

export const uploadResume = (form: FormData) =>
  api.post("/profile/upload-resume", form);

export const fetchProfile = () => api.get("/profile/");

export const fetchCompleteProfile = () => api.get("/profile/complete");

export const updateProfile = (data: Record<string, unknown>) =>
  api.put("/profile/", data);

export const deleteProfile = () => api.delete("/profile/");

// Legacy API endpoints (deprecated)
export const uploadProfile = (form: FormData) =>
  api.post("/profile/", form);

export const savePersonalInfo = (data: Record<string, unknown>) =>
  api.post("/information/", data);

export const fetchPersonalInfo = () => api.get("/information/");

export const requestPasswordReset = (email: string) =>
  api.post("/user/request-password-reset", { user_id: email });

export const verifyOtp = (email: string, otp: string) =>
  api.post("/user/verify-otp", { user_id: email, otp });

export const resetPassword = (email: string, otp: string, password: string) =>
  api.post("/user/reset-password", { user_id: email, otp, password });

// Job Matches API
export const fetchJobMatches = (params?: { limit?: number; offset?: number; min_relevance?: number }) =>
  api.get("/jobs/matches", { params });

export const fetchJobMatchStats = () => api.get("/jobs/matches/stats");

export const fetchJobMatch = (matchId: number) => api.get(`/jobs/matches/${matchId}`);
