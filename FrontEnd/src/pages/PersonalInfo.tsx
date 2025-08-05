import React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { savePersonalInfo, fetchPersonalInfo } from '@/lib/api';

const PersonalInfo = () => {
  const navigate = useNavigate();
  const [info, setInfo] = React.useState<Record<string, string | null>>({});
  const [agree, setAgree] = React.useState(false);

  React.useEffect(() => {
    fetchPersonalInfo()
      .then((res) => setInfo(res.data))
      .catch((error) => {
        if (error.response?.status === 404) {
          // User doesn't have personal info yet - that's OK, start with empty form
        } else if (error.response?.status === 401) {
          // Unauthorized - API interceptor will handle redirect
          console.error("Unauthorized access");
        } else {
          console.error("Failed to fetch personal info:", error);
        }
      });
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const data: Record<string, unknown> = {
      first_name: fd.get('first_name'),
      last_name: fd.get('last_name'),
      phone_number: fd.get('phone_number'),
      country: fd.get('country'),
      state: fd.get('state'),
      city: fd.get('city'),
      street: fd.get('street'),
      alternate_email: fd.get('alternate_email'),
    };
    if (!agree) {
      toast.error('You must agree to the terms');
      return;
    }
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
      navigate('/dashboard');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 hero-gradient flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <Card className="w-full max-w-xl p-8 space-y-6 glass-card animate-fade-in">
          <h2 className="text-2xl font-bold text-center">Personal Information</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="first_name">First Name</Label>
                <Input id="first_name" name="first_name" defaultValue={info.first_name ?? ''} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="last_name">Last Name</Label>
                <Input id="last_name" name="last_name" defaultValue={info.last_name ?? ''} />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone_number">Phone Number</Label>
              <Input id="phone_number" name="phone_number" defaultValue={info.phone_number ?? ''} />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Input id="country" name="country" defaultValue={info.country ?? ''} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Input id="state" name="state" defaultValue={info.state ?? ''} />
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input id="city" name="city" defaultValue={info.city ?? ''} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="street">Street</Label>
                <Input id="street" name="street" defaultValue={info.street ?? ''} />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="alternate_email">Alternate Email</Label>
              <Input id="alternate_email" name="alternate_email" type="email" defaultValue={info.alternate_email ?? ''} />
            </div>
            <div className="flex items-center space-x-2">
              <input
                id="agree"
                type="checkbox"
                checked={agree}
                onChange={(e) => setAgree(e.target.checked)}
              />
              <Label htmlFor="agree" className="text-sm">I agree to the terms and conditions</Label>
            </div>
            <div className="flex justify-end gap-4 pt-4">
              <Button type="button" variant="outline" onClick={handleSkip}>Skip</Button>
              <Button type="submit" disabled={!agree}>Save</Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default PersonalInfo;
