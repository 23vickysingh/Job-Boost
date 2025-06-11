
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Edit, User, Mail, Phone, MapPin, Briefcase, Calendar } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface UserProfileProps {
  onEditClick: () => void;
}

const UserProfile: React.FC<UserProfileProps> = ({ onEditClick }) => {
  // This would come from your user context or API in a real app
  const user = {
    name: "John Doe",
    age: 28,
    email: "john.doe@example.com",
    phone: "+1 (555) 123-4567",
    address: "123 Main Street, San Francisco, CA",
    role: "Front-End Developer",
    experience: "3 years",
    education: "Bachelor's in Computer Science"
  };

  return (
    <Card className="mb-6">
      <CardHeader className="pb-4 flex flex-row items-center justify-between">
        <CardTitle className="text-xl font-semibold">Profile</CardTitle>
        <Button variant="outline" size="sm" onClick={onEditClick} className="flex items-center gap-2">
          <Edit className="h-4 w-4" />
          Update Profile
        </Button>
      </CardHeader>
      <CardContent className="grid md:grid-cols-2 gap-6">
        <div className="flex flex-col sm:flex-row gap-4 items-center sm:items-start">
          <Avatar className="h-20 w-20">
            <AvatarImage src="https://github.com/shadcn.png" alt={user.name} />
            <AvatarFallback className="text-lg">
              {user.name.split(' ').map(n => n[0]).join('')}
            </AvatarFallback>
          </Avatar>
          
          <div className="text-center sm:text-left">
            <h3 className="text-xl font-semibold">{user.name}</h3>
            <p className="text-gray-600 dark:text-gray-300">{user.role}</p>
            <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">{user.age} years old</p>
          </div>
        </div>
        
        <div className="space-y-3">
          <div className="flex items-start gap-2">
            <Mail className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Email</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.email}</p>
            </div>
          </div>
          
          <div className="flex items-start gap-2">
            <Phone className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Phone</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.phone}</p>
            </div>
          </div>
          
          <div className="flex items-start gap-2">
            <MapPin className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Address</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.address}</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default UserProfile;
