
import React from 'react';
import { Link } from 'react-router-dom';
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
  Settings, 
  Bookmark, 
  BarChart,
  ArrowRight 
} from "lucide-react";
import Navbar from '@/components/Navbar';
import UserProfile from '@/components/dashboard/UserProfile';
import JobPreferences from '@/components/dashboard/job-preferences/JobPreferences';
import Internships from '@/components/dashboard/Internships';
import DashboardStats from '@/components/dashboard/DashboardStats';
import JobMatchesList from '@/components/dashboard/JobMatchesList';
import ApplicationsList from '@/components/dashboard/ApplicationsList';
import AnalyticsDashboard from '@/components/dashboard/AnalyticsDashboard';

const Dashboard = () => {
  const [activeTab, setActiveTab] = React.useState("matches");
  const [isEditingProfile, setIsEditingProfile] = React.useState(false);
  
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <div className="flex-1 bg-gray-50 dark:bg-slate-900 pt-6 pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
              <p className="text-gray-600 dark:text-gray-300">Welcome back! Here's your job search overview.</p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-3">
              <Link to="/resume-upload">
                <Button variant="outline" className="flex items-center">
                  <FileText className="mr-2 h-4 w-4" />
                  Update Resume
                </Button>
              </Link>
              <Button 
                className="flex items-center"
                onClick={() => setActiveTab("preferences")}
              >
                <Settings className="mr-2 h-4 w-4" />
                Preferences
              </Button>
            </div>
          </div>
          
          <DashboardStats />
          
          <UserProfile onEditClick={() => setIsEditingProfile(true)} />
          
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="mb-6">
              <TabsTrigger value="matches" className="flex items-center">
                <Briefcase className="mr-2 h-4 w-4" />
                Job Matches
              </TabsTrigger>
              <TabsTrigger value="applications" className="flex items-center">
                <FileText className="mr-2 h-4 w-4" />
                Applications
              </TabsTrigger>
              <TabsTrigger value="internships" className="flex items-center">
                <Bookmark className="mr-2 h-4 w-4" />
                Internships
              </TabsTrigger>
              <TabsTrigger value="analytics" className="flex items-center">
                <BarChart className="mr-2 h-4 w-4" />
                Analytics
              </TabsTrigger>
              <TabsTrigger value="preferences" className="flex items-center">
                <Settings className="mr-2 h-4 w-4" />
                Preferences
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="matches" className="space-y-4">
              <JobMatchesList />
            </TabsContent>
            
            <TabsContent value="applications">
              <ApplicationsList />
            </TabsContent>
            
            <TabsContent value="internships">
              <Internships />
            </TabsContent>
            
            <TabsContent value="analytics">
              <AnalyticsDashboard />
            </TabsContent>
            
            <TabsContent value="preferences">
              <JobPreferences />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
