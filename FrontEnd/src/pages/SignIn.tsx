
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import AuthForm from '@/components/AuthForm';
import { useAuth } from "@/contexts/AuthContext";
import { isValidEmail, getEmailErrorMessage } from '@/lib/validation';

const SignIn = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (isLoading) return; // Prevent multiple submissions
    
    const fd = new FormData(e.currentTarget);
    const email = fd.get("email") as string;
    const password = fd.get("password") as string;

    // Update form data to preserve values
    setFormData({ email, password });

    // Validate email format
    if (!isValidEmail(email)) {
      toast.error(getEmailErrorMessage(email));
      return;
    }

    setIsLoading(true);
    try {
      await login(email, password);
      toast.success("Signed in successfully! Redirecting to dashboard...");
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch {

    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 hero-gradient">
        <div className="w-full max-w-md space-y-8 animate-fade-in">
          <AuthForm 
            type="signin" 
            onSubmit={handleSubmit} 
            defaultValues={formData}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
};

export default SignIn;
