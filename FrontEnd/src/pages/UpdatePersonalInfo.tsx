import React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { savePersonalInfo, fetchPersonalInfo } from '@/lib/api';
import { useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@/contexts/AuthContext';
import axios from 'axios';

const UpdatePersonalInfo = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { token } = useAuth();
  const [info, setInfo] = React.useState<Record<string, string | null>>({});
  const [isEditing, setIsEditing] = React.useState(false);
  const email = localStorage.getItem('email') || '';

  React.useEffect(() => {
    fetchPersonalInfo()
      .then((res) => setInfo(res.data))
      .catch(() => {});
  }, []);

  React.useEffect(() => {
    if (!token) {
      navigate('/signin');
    }
  }, [token, navigate]);

  React.useEffect(() => {
    fetchPersonalInfo()
      .then((res) => setInfo(res.data))
      .catch((err) => {
        if (axios.isAxiosError(err) && err.response?.status === 401) {
          toast.error('Session expired. Please sign in again.');
          navigate('/signin');
        } else {
          toast.error('Unable to load information');
        }
      });
  }, [navigate]);

  const handleEdit = () => setIsEditing(true);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const data: Record<string, unknown> = {};
    [
      'dob',
      'country',
      'state',
      'city',
      'street',
      'house_number',
      'pin_code',
      'phone_number',
      'current_job_role',
      'company',
    ].forEach((key) => {
      const val = fd.get(key);
      if (val !== null && val !== (info[key] ?? '')) {
        data[key] = val || null;
      }
    });
    if (Object.keys(data).length === 0) {
      toast.info('No changes to save');
      return;
    }
    try {
      await savePersonalInfo(data);
      toast.success('Information saved');
      queryClient.invalidateQueries();
      setInfo((prev) => ({ ...prev, ...data }));
      setIsEditing(false);
      navigate('/dashboard');
    } catch {
      toast.error('Unable to save information');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 hero-gradient flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <Card className="w-full max-w-xl p-8 space-y-6 glass-card animate-fade-in">
          <h2 className="text-2xl font-bold text-center">Update Personal Information</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" name="email" type="email" value={email} disabled />
            </div>
            <div className="space-y-2">
              <Label htmlFor="dob">Date of Birth</Label>
              <Input id="dob" name="dob" type="date" defaultValue={info.dob ?? ''} disabled={!isEditing} />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Input id="country" name="country" defaultValue={info.country ?? ''} disabled={!isEditing} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Input id="state" name="state" defaultValue={info.state ?? ''} disabled={!isEditing} />
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input id="city" name="city" defaultValue={info.city ?? ''} disabled={!isEditing} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="street">Street</Label>
                <Input id="street" name="street" defaultValue={info.street ?? ''} disabled={!isEditing} />
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="house_number">House No.</Label>
                <Input id="house_number" name="house_number" defaultValue={info.house_number ?? ''} disabled={!isEditing} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pin_code">PIN Code</Label>
                <Input id="pin_code" name="pin_code" defaultValue={info.pin_code ?? ''} disabled={!isEditing} />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone_number">Phone Number</Label>
              <Input id="phone_number" name="phone_number" defaultValue={info.phone_number ?? ''} disabled={!isEditing} />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="current_job_role">Current Job Role</Label>
                <Input id="current_job_role" name="current_job_role" defaultValue={info.current_job_role ?? ''} disabled={!isEditing} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="company">Company</Label>
                <Input id="company" name="company" defaultValue={info.company ?? ''} disabled={!isEditing} />
              </div>
            </div>
            <div className="flex justify-end gap-4 pt-4">
              {!isEditing && (
                <Button type="button" variant="outline" onClick={handleEdit}>
                  Edit
                </Button>
              )}
              <Button type="submit" disabled={!isEditing}>Save</Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default UpdatePersonalInfo;
