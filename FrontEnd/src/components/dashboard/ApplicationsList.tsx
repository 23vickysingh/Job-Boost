
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
import { FileText, X } from "lucide-react";
import { useJobs } from "@/contexts/JobContext";
import { toast } from "sonner";

const ApplicationsList: React.FC = () => {
  const { applications, removeApplication } = useJobs();

  // Handler for closing an application
  const handleCloseApplication = (applicationId: number) => {
    removeApplication(applicationId);
    toast.success("Application closed successfully!");
  };

  return (
    <div className="h-full overflow-hidden flex flex-col">
      <div className="flex justify-between items-center px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-slate-800/50">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Your Applications</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">Track the status of all your job applications</p>
        </div>
      </div>
      
      {applications.length === 0 ? (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="text-center space-y-4">
            <div className="mx-auto w-24 h-24 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
              <FileText className="w-12 h-12 text-gray-400" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                No applications yet
              </h3>
              <p className="text-gray-500 dark:text-gray-400">
                Your job applications will appear here once you start applying to jobs.
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto p-6">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-gray-700 dark:text-gray-300 uppercase bg-gray-100 dark:bg-slate-800 sticky top-0">
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
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => handleCloseApplication(app.id)}
                      className="text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
                    >
                      <X className="mr-1 h-3 w-3" />
                      Close Application
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ApplicationsList;
