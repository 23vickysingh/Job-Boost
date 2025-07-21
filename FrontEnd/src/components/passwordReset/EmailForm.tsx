import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface Props {
  onSubmit: (email: string) => void;
}

const EmailForm: React.FC<Props> = ({ onSubmit }) => {
  const handle = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const email = fd.get('email') as string;
    if (email) onSubmit(email);
  };
  return (
    <form onSubmit={handle} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="fp-email">Registered Email</Label>
        <Input id="fp-email" name="email" type="email" required />
      </div>
      <Button type="submit" className="w-full">Send OTP</Button>
    </form>
  );
};

export default EmailForm;
