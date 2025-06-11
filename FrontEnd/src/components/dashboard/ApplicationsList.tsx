
import React, { useState } from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// Mock data for the applications
const initialApplications = [
  {
    id: 101,
    title: "UX/UI Designer",
    company: "Creative Designs",
    appliedDate: "2023-06-15",
    status: "Interview",
    response: true
  },
  {
    id: 102,
    title: "React Native Developer",
    company: "MobileApps Inc.",
    appliedDate: "2023-06-10",
    status: "Applied",
    response: false
  },
  {
    id: 103,
    title: "Frontend Developer",
    company: "WebTech Solutions",
    appliedDate: "2023-06-05",
    status: "Rejected",
    response: true
  },
  {
    id: 104,
    title: "JavaScript Engineer",
    company: "CodeMasters",
    appliedDate: "2023-06-01",
    status: "Applied",
    response: false
  },
];

const ApplicationsList: React.FC = () => {
  const [applications] = useState(initialApplications);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Applications</CardTitle>
        <CardDescription>
          Track the status of all your job applications
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-gray-700 dark:text-gray-300 uppercase bg-gray-100 dark:bg-slate-800">
              <tr>
                <th className="px-6 py-3">Position</th>
                <th className="px-6 py-3">Company</th>
                <th className="px-6 py-3">Applied Date</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {applications.map(app => (
                <tr key={app.id} className="border-b dark:border-gray-700">
                  <td className="px-6 py-4 font-medium">{app.title}</td>
                  <td className="px-6 py-4">{app.company}</td>
                  <td className="px-6 py-4">{app.appliedDate}</td>
                  <td className="px-6 py-4">
                    <Badge
                      className={
                        app.status === "Interview" 
                          ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300" 
                          : app.status === "Rejected"
                          ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
                          : "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
                      }
                    >
                      {app.status}
                    </Badge>
                  </td>
                  <td className="px-6 py-4">
                    <Button variant="ghost" size="sm">
                      View Details
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
};

export default ApplicationsList;
