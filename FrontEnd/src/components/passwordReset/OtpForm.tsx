import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface Props {
  onSubmit: (otp: string) => void;
}

const OtpForm: React.FC<Props> = ({ onSubmit }) => {
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
      </div>
      <Button type="submit" className="w-full">Verify OTP</Button>
    </form>
  );
};

export default OtpForm;
