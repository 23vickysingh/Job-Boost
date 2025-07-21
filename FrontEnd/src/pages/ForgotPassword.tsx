import React, { useState } from 'react';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import EmailForm from '@/components/passwordReset/EmailForm';
import OtpForm from '@/components/passwordReset/OtpForm';
import NewPasswordForm from '@/components/passwordReset/NewPasswordForm';
import { requestPasswordReset, verifyOtp, resetPassword } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

const ForgotPassword = () => {
  const [step, setStep] = useState<'email' | 'otp' | 'reset'>('email');
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleEmail = async (em: string) => {
    try {
      await requestPasswordReset(em);
      setEmail(em);
      toast.success('OTP sent to your email');
      setStep('otp');
    } catch (err) {
      toast.error('Unable to send OTP');
    }
  };

  const handleOtp = async (o: string) => {
    try {
      await verifyOtp(email, o);
      setOtp(o);
      toast.success('OTP verified');
      setStep('reset');
    } catch {
      toast.error('Invalid OTP');
    }
  };

  const handleReset = async (password: string, confirm: string) => {
    if (password !== confirm) {
      toast.error('Passwords do not match');
      return;
    }
    const valid = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/;
    if (!valid.test(password)) {
      toast.error('Password must be 8+ chars with letters, numbers and symbol');
      return;
    }
    try {
      await resetPassword(email, otp, password);
      toast.success('Password updated');
      await login(email, password);
      navigate('/dashboard');
    } catch {
      toast.error('Failed to reset password');
    }
  };

  const renderStep = () => {
    switch (step) {
      case 'email':
        return <EmailForm onSubmit={handleEmail} />;
      case 'otp':
        return <OtpForm onSubmit={handleOtp} />;
      case 'reset':
        return <NewPasswordForm onSubmit={handleReset} />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 hero-gradient">
        <div className="w-full max-w-md space-y-8 animate-fade-in glass-card p-8 rounded-xl shadow-xl">
          {renderStep()}
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
