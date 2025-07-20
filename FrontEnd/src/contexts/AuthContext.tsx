import React, { createContext, useContext, useState } from "react";
import { login as apiLogin, register as apiRegister } from "@/lib/api";
import { toast } from "sonner";

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
    const { data } = await apiLogin(email, password);
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
    toast.success("Signed in successfully");
  };

  const register = async (email: string, password: string) => {
    await apiRegister(email, password);
    toast.success("Account created! Please sign in.");
  };

  const logout = () => {
    localStorage.removeItem("token");
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
