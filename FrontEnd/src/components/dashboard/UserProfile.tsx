
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Edit, Mail, Phone, MapPin } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface Profile {
  first_name: string | null;
  last_name: string | null;
  phone_number: string | null;
  country: string | null;
  state: string | null;
  city: string | null;
  street: string | null;
  alternate_email: string | null;
}

interface UserProfileProps {
  onEditClick: () => void;
  profile?: Profile;
}

const UserProfile: React.FC<UserProfileProps> = ({ onEditClick, profile }) => {
  const user = profile || {
    first_name: null,
    last_name: null,
    phone_number: null,
    country: null,
    state: null,
    city: null,
    street: null,
    alternate_email: null,
  };
  const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ");
  const address = [user.street, user.city, user.state, user.country]
    .filter(Boolean)
    .join(", ");

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
            <AvatarImage src="https://github.com/shadcn.png" alt={fullName} />
            <AvatarFallback className="text-lg">
              {fullName ? fullName.split(' ').map((n: string) => n[0]).join('') : ""}
            </AvatarFallback>
          </Avatar>

          <div className="text-center sm:text-left">
            <h3 className="text-xl font-semibold">{fullName || "-"}</h3>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-start gap-2">
            <Mail className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Alternate Email</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.alternate_email || "-"}</p>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <Phone className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Phone</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{user.phone_number || "-"}</p>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <MapPin className="h-5 w-5 text-gray-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Address</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{address || "-"}</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default UserProfile;
