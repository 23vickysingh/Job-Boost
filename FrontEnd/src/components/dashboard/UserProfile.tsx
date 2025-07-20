
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Edit, User, Mail, Phone, MapPin, Briefcase, Calendar } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface UserProfileProps {
  onEditClick: () => void;
  profile?: any;
}

const UserProfile: React.FC<UserProfileProps> = ({ onEditClick, profile }) => {
  const user = profile || {
    full_name: "",
    interested_role: "",
    experience: 0,
    email: "",
    phone: "",
    address: ""
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
            <AvatarImage src="https://github.com/shadcn.png" alt={user.full_name} />
            <AvatarFallback className="text-lg">
              {user.full_name ? user.full_name.split(' ').map((n: string) => n[0]).join('') : ""}
            </AvatarFallback>
          </Avatar>

          <div className="text-center sm:text-left">
            <h3 className="text-xl font-semibold">{user.full_name || "-"}</h3>
            <p className="text-gray-600 dark:text-gray-300">{user.interested_role || "-"}</p>
            <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">{user.experience ? `${user.experience} yrs exp` : "-"}</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-start gap-2">
            <Mail className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Email</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.email || "-"}</p>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <Phone className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Phone</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.phone || "-"}</p>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <MapPin className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Address</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.address || "-"}</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default UserProfile;
