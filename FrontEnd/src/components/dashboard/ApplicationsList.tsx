
import React, { useState, useEffect } from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { FileText, X } from "lucide-react";
import { fetchApplications, updateJobMatchStatus, deleteJobMatch } from "@/lib/api";
import { toast } from "sonner";

interface Job {
  id: number;
  job_id: string;
  job_title: string;
  employer_name: string;
  job_description?: string;
  job_city?: string;
  job_country?: string;
  job_employment_type?: string;
  job_min_salary?: number;
  job_max_salary?: number;
  job_salary_currency?: string;
}

interface Application {
  id: number;
  user_id: number;
  job_id: number;
  relevance_score: number;
  created_at: string;
  status: string;
  job: Job;  // Nested job details from the API
}

const ApplicationsList: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [error, setError] = useState<string | null>(null);
  
  // State for confirmation dialog
  const [showCloseDialog, setShowCloseDialog] = useState(false);
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);

  // Fetch applications from API
  useEffect(() => {
    const loadApplications = async () => {
      try {
        setError(null);
        // console.log('Fetching applications...');
        const response = await fetchApplications();
        // console.log('Applications response:', response);
        setApplications(response.data || []);
      } catch (err) {
        // console.error('Error fetching applications:', err);
        setError('Failed to load applications');
        toast.error('Failed to load applications');
      }
    };

    loadApplications();
  }, []);

  // Handler for closing an application
  const handleCloseApplication = (application: Application) => {
    setSelectedApplication(application);
    setShowCloseDialog(true);
  };

  // Handler for confirming close application action
  const handleConfirmCloseApplication = async () => {
    if (!selectedApplication) return;
    
    try {
      await deleteJobMatch(selectedApplication.id);
      // Remove from local state
      setApplications(prev => prev.filter(app => app.id !== selectedApplication.id));
      // toast.success("Application closed and removed successfully!");
    } catch (error) {
      // console.error('Error closing application:', error);
      toast.error("Failed to close application");
    } finally {
      setShowCloseDialog(false);
      setSelectedApplication(null);
    }
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="h-full overflow-hidden flex flex-col">
      <div className="flex justify-between items-center px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-slate-800/50">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Your Applications</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">Track the status of all your job applications</p>
        </div>
      </div>
      
      {error ? (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="text-center space-y-4">
            <div className="mx-auto w-24 h-24 bg-red-100 dark:bg-red-800 rounded-full flex items-center justify-center">
              <FileText className="w-12 h-12 text-red-600" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-red-900 dark:text-red-300 mb-2">
                Error loading applications
              </h3>
              <p className="text-red-500 dark:text-red-400">
                {error}
              </p>
            </div>
          </div>
        </div>
      ) : applications.length === 0 ? (
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
                  <td className="px-6 py-4 font-medium">{app.job.job_title}</td>
                  <td className="px-6 py-4">{app.job.employer_name}</td>
                  <td className="px-6 py-4">{formatDate(app.created_at)}</td>
                  <td className="px-6 py-4">
                    <Badge
                      className={
                        app.status === "applied"
                          ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
                          : app.status === "not_interested"
                          ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
                          : "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
                      }
                    >
                      {app.status === "applied" ? "Applied" : app.status === "not_interested" ? "Not Interested" : "Pending"}
                    </Badge>
                  </td>
                  <td className="px-6 py-4">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => handleCloseApplication(app)}
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

      {/* Close Application Confirmation Dialog */}
      <Dialog open={showCloseDialog} onOpenChange={setShowCloseDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Close Job Application</DialogTitle>
            <DialogDescription>
              Are you sure you want to close this job application? This action will remove it completely and cannot be undone.
            </DialogDescription>
          </DialogHeader>
          {selectedApplication && (
            <div className="py-4">
              <p className="font-medium">{selectedApplication.job.job_title}</p>
              <p className="text-sm text-gray-600">{selectedApplication.job.employer_name}</p>
            </div>
          )}
          <DialogFooter>
            <Button 
              variant="outline" 
              onClick={() => setShowCloseDialog(false)}
            >
              Cancel
            </Button>
            <Button 
              variant="destructive" 
              onClick={handleConfirmCloseApplication}
            >
              Close Application
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ApplicationsList;
