import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface Props {
  onSubmit: (otp: string) => void;
  onExpire: () => void;
}

const SignupOtpForm: React.FC<Props> = ({ onSubmit, onExpire }) => {
  const [timeLeft, setTimeLeft] = useState(60);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(interval);
          onExpire();
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [onExpire]);

  const handle = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const otp = fd.get('otp') as string;
    if (otp) onSubmit(otp);
  };

  return (
    <form onSubmit={handle} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="otp">Enter OTP sent to your email</Label>
        <Input id="otp" name="otp" required />
        <p className="text-sm text-gray-500">Time remaining: {timeLeft}s</p>
      </div>
      <Button type="submit" className="w-full">Verify OTP</Button>
    </form>
  );
};

export default SignupOtpForm;
