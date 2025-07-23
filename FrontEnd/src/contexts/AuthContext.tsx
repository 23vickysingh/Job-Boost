import React, { createContext, useContext, useState } from "react";
import { login as apiLogin, register as apiRegister } from "@/lib/api";
import { toast } from "sonner";
import axios from "axios";

interface AuthCtx {
  token: string | null;
  login: (e: string, p: string) => Promise<void>;
  register: (e: string, p: string) => Promise<void>;
  logout: () => void;
}
const AuthContext = createContext<AuthCtx | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem("token")
  );

  const login = async (email: string, password: string) => {
    try {
      const { data } = await apiLogin(email, password);
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("email", email);
      setToken(data.access_token);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        toast.error(err.response.data.detail || "Invalid credentials");
      } else {
        toast.error("Unable to sign in");
      }
      throw err;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      await apiRegister(email, password);
      const { data } = await apiLogin(email, password);
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("email", email);
      setToken(data.access_token);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        toast.error(err.response.data.detail || "Unable to register");
      } else {
        toast.error("Unable to register");
      }
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
};
