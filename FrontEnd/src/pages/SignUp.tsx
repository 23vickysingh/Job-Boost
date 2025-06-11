
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import AuthForm from '@/components/AuthForm';

const SignUp = () => {
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, you would handle the sign-up logic here
    toast.success("Account created successfully! Redirecting to dashboard...");
    setTimeout(() => navigate('/dashboard'), 2000);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 hero-gradient">
        <div className="w-full max-w-md space-y-8 animate-fade-in">
          <AuthForm type="signup" onSubmit={handleSubmit} />
        </div>
      </div>
    </div>
  );
};

export default SignUp;
