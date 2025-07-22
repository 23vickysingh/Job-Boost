
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import AuthForm from '@/components/AuthForm';
import SignupOtpForm from '@/components/signup/OtpForm';
import { useAuth } from "@/contexts/AuthContext";
import { requestRegistration, confirmRegistration } from '@/lib/api';

const SignUp = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState<'form' | 'otp'>('form');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const em = fd.get("email") as string;
    const pw = fd.get("password") as string;
    const confirm = fd.get("confirm") as string;

    if (pw !== confirm) {
      toast.error("Passwords do not match");
      return;
    }
    try {
      await requestRegistration(em, pw);
      setEmail(em);
      setPassword(pw);
      toast.success('OTP sent to your email');
      setStep('otp');
    } catch {
      toast.error('Unable to register');
    }
  };

  const handleOtp = async (otp: string) => {
    try {
      await confirmRegistration(email, otp);
      toast.success('Account verified');
      await login(email, password);
      navigate('/personal-info');
    } catch {
      toast.error('OTP incorrect');
    }
  };

  const handleExpire = () => {
    toast.error('OTP expired. Please sign up again');
    setStep('form');
  };

  const renderStep = () => {
    return step === 'form' ? (
      <AuthForm type="signup" onSubmit={handleSubmit} />
    ) : (
      <SignupOtpForm onSubmit={handleOtp} onExpire={handleExpire} />
    );
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 hero-gradient">
        <div className="w-full max-w-md space-y-8 animate-fade-in">
          {renderStep()}
        </div>
      </div>
    </div>
  );
};

export default SignUp;
