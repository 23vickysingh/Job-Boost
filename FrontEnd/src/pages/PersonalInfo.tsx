import React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { savePersonalInfo } from '@/lib/api';

const PersonalInfo = () => {
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const data: Record<string, unknown> = {
      dob: fd.get('dob'),
      country: fd.get('country'),
      state: fd.get('state'),
      city: fd.get('city'),
      street: fd.get('street'),
      house_number: fd.get('house_number'),
      pin_code: fd.get('pin_code'),
      phone_number: fd.get('phone_number'),
      current_job_role: fd.get('current_job_role'),
      company: fd.get('company'),
    };
    try {
      await savePersonalInfo(data);
      toast.success('Information saved');
      navigate('/resume-upload');
    } catch {
      toast.error('Unable to save information');
    }
  };

  const handleSkip = () => {
    if (window.confirm('Skip adding personal info? You can fill it later.')) {
      navigate('/resume-upload');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 hero-gradient flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <Card className="w-full max-w-xl p-8 space-y-6 glass-card animate-fade-in">
          <h2 className="text-2xl font-bold text-center">Personal Information</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="dob">Date of Birth</Label>
              <Input id="dob" name="dob" type="date" />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Input id="country" name="country" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Input id="state" name="state" />
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input id="city" name="city" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="street">Street</Label>
                <Input id="street" name="street" />
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="house_number">House No.</Label>
                <Input id="house_number" name="house_number" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pin_code">PIN Code</Label>
                <Input id="pin_code" name="pin_code" />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone_number">Phone Number</Label>
              <Input id="phone_number" name="phone_number" />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="current_job_role">Current Job Role</Label>
                <Input id="current_job_role" name="current_job_role" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="company">Company</Label>
                <Input id="company" name="company" />
              </div>
            </div>
            <div className="flex justify-end gap-4 pt-4">
              <Button type="button" variant="outline" onClick={handleSkip}>Skip</Button>
              <Button type="submit">Continue</Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default PersonalInfo;
