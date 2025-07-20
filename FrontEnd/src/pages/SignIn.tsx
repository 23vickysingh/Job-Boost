
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import AuthForm from '@/components/AuthForm';
import { useAuth } from "@/contexts/AuthContext";

const SignIn = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const email = fd.get("email") as string;
    const password = fd.get("password") as string;
    try {
      await login(email, password);
      toast.success("Signed in successfully! Redirecting to dashboard...");
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch {
      // Error toast handled in context
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 hero-gradient">
        <div className="w-full max-w-md space-y-8 animate-fade-in">
          <AuthForm type="signin" onSubmit={handleSubmit} />
        </div>
      </div>
    </div>
  );
};

export default SignIn;
