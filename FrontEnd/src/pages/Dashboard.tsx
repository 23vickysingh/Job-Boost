
import React from 'react';

import { useQuery } from "@tanstack/react-query";
import { fetchProfile } from "@/lib/api";

import { Link, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Briefcase, 
  FileText, 
  Settings
} from "lucide-react";
import Navbar from '@/components/Navbar';
import UserProfile from '@/components/dashboard/UserProfile';
import JobPreferences from '@/components/dashboard/job-preferences/JobPreferences';
import Internships from '@/components/dashboard/Internships';
import DashboardStats from '@/components/dashboard/DashboardStats';
import JobMatchesList from '@/components/dashboard/JobMatchesList';
import ApplicationsList from '@/components/dashboard/ApplicationsList';
import { useAuth } from "@/contexts/AuthContext";
import { JobProvider } from "@/contexts/JobContext";

const Dashboard = () => {
  const [activeTab, setActiveTab] = React.useState("matches");
  const { token } = useAuth();
  const navigate = useNavigate();
  React.useEffect(() => {
    if (!token) {
      navigate("/signin");
    }
  }, [token, navigate]);
  // Fetch the user's profile with enhanced user information
  const { data: profileResponse, error: profileError, isLoading: profileLoading } = useQuery({
    queryKey: ["profile"],
    queryFn: fetchProfile,
  });
  
  const profile = profileResponse?.data;
  
  return (
    <JobProvider>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        
        <div className="flex-1 bg-gray-50 dark:bg-slate-900 pt-6 pb-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
                <p className="text-gray-600 dark:text-gray-300">Welcome back! Here's your job search overview.</p>
              </div>
            </div>
            
            <DashboardStats profile={profile} />

            {profileLoading ? (
              <div className="bg-white dark:bg-slate-800 rounded-lg p-8 text-center mb-6">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                <p className="text-gray-500 dark:text-gray-400">Loading profile...</p>
              </div>
            ) : profileError ? (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-medium text-red-800 dark:text-red-200 mb-2">Profile Loading Error</h3>
                <p className="text-red-600 dark:text-red-300 mb-4">
                  Unable to load your profile. This might be due to:
                </p>
                <ul className="text-sm text-red-600 dark:text-red-300 list-disc list-inside space-y-1 mb-4">
                  <li>Backend server not running</li>
                  <li>Network connectivity issues</li>
                  <li>Authentication token expired</li>
                </ul>
                <p className="text-sm text-red-500 dark:text-red-400">
                  Error: {profileError?.message || 'Unknown error'}
                </p>
              </div>
            ) : (
              <UserProfile profile={profile} onEditClick={() => navigate('/update-profile')} />
            )}
            
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <Card className="overflow-hidden border border-gray-200 dark:border-gray-700 shadow-sm">
                <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4">
                  <CardTitle className="text-lg font-semibold flex items-center">
                    <Briefcase className="mr-2 h-5 w-5" />
                    Job Management
                  </CardTitle>
                  <p className="text-blue-100 text-sm mt-1">
                    Manage your job matches and applications
                  </p>
                  <div className="mt-4">
                    <TabsList className="grid w-full grid-cols-2 gap-2 bg-white/10 backdrop-blur-sm rounded-lg p-1">
                      <TabsTrigger 
                        value="matches" 
                        className="flex items-center justify-center py-2 px-4 rounded-md transition-all duration-200 text-white/80 data-[state=active]:bg-white data-[state=active]:text-blue-600 data-[state=active]:shadow-lg data-[state=active]:font-medium"
                      >
                        <Briefcase className="mr-2 h-4 w-4" />
                        <span className="hidden sm:inline">Job Matches</span>
                        <span className="sm:hidden">Matches</span>
                      </TabsTrigger>
                      <TabsTrigger 
                        value="applications" 
                        className="flex items-center justify-center py-2 px-4 rounded-md transition-all duration-200 text-white/80 data-[state=active]:bg-white data-[state=active]:text-green-600 data-[state=active]:shadow-lg data-[state=active]:font-medium"
                      >
                        <FileText className="mr-2 h-4 w-4" />
                        <span className="hidden sm:inline">Applications</span>
                        <span className="sm:hidden">Apps</span>
                      </TabsTrigger>
                    </TabsList>
                  </div>
                </CardHeader>
                <CardContent className="h-[85vh] overflow-y-auto p-0">
                  <TabsContent value="matches" className="m-0 h-full">
                    <JobMatchesList />
                  </TabsContent>
                  
                  <TabsContent value="applications" className="m-0 h-full">
                    <ApplicationsList />
                  </TabsContent>
                </CardContent>
              </Card>
            </Tabs>
          </div>
        </div>
      </div>
    </JobProvider>
  );
};

export default Dashboard;
