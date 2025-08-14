
import React from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ArrowUpRight, Search, Target, FileText, User } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { fetchJobMatchStats } from "@/lib/api";

// Interface for profile data
interface Profile {
  id?: number;
  user_id?: number;
  user_email?: string;
  user_name?: string;
  query?: string;
  location?: string;
  mode_of_job?: string;
  work_experience?: string;
  employment_types?: string[];
  company_types?: string[];
  job_requirements?: string;
  resume_location?: string;
  resume_parsed?: any;
  last_updated?: string;
}

interface DashboardStatsProps {
  profile?: Profile;
}

const DashboardStats: React.FC<DashboardStatsProps> = ({ profile }) => {
  // Fetch job match statistics
  const { data: jobStats, isLoading: statsLoading } = useQuery({
    queryKey: ["jobStats"],
    queryFn: fetchJobMatchStats,
  });

  // Calculate profile strength based on available data
  const calculateProfileStrength = (): number => {
    if (!profile) return 0;
    
    let score = 0;
    const maxScore = 8;
    
    // Basic info (20% each)
    if (profile.query) score += 1;
    if (profile.location) score += 1;
    if (profile.mode_of_job) score += 1;
    if (profile.work_experience) score += 1;
    
    // Employment preferences (10% each)
    if (profile.employment_types && profile.employment_types.length > 0) score += 1;
    if (profile.company_types && profile.company_types.length > 0) score += 1;
    
    // Resume data (20%)
    if (profile.resume_parsed) score += 1;
    
    // Additional requirements (10%)
    if (profile.job_requirements) score += 1;
    
    return Math.round((score / maxScore) * 100);
  };

  const profileStrength = calculateProfileStrength();
  
  // Get job statistics from API or use defaults
  const totalMatches = jobStats?.data?.total_matches || 0;
  const highRelevanceJobs = jobStats?.data?.high_relevance_jobs || 0;
  const recentMatches = jobStats?.data?.recent_matches || 0;
  
  // Mock data for applications - would come from API in real app
  const mockApplications = 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      {/* Jobs Fetched Card - First Position */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center">
            <Search className="mr-2 h-4 w-4" />
            Jobs Matched
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {statsLoading ? (
              <div className="h-8 w-16 bg-gray-200 dark:bg-gray-700 animate-pulse rounded"></div>
            ) : (
              totalMatches
            )}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            <span className="text-blue-500 dark:text-blue-400">{recentMatches}</span> new matches today
          </p>
        </CardContent>
      </Card>
            
      {/* Jobs with High Relevance Card - Second Position */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center">
            <Target className="mr-2 h-4 w-4" />
            High Relevance Jobs
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {statsLoading ? (
              <div className="h-8 w-16 bg-gray-200 dark:bg-gray-700 animate-pulse rounded"></div>
            ) : (
              highRelevanceJobs
            )}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            80%+ match with your profile
          </p>
        </CardContent>
      </Card>
            
      {/* Applications Card - Third Position */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center">
            <FileText className="mr-2 h-4 w-4" />
            Applications
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{mockApplications}</div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            <span className="text-green-500 dark:text-green-400">0</span> from last week
          </p>
        </CardContent>
      </Card>
            
      {/* Profile Strength Card - Fourth Position */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center">
            <User className="mr-2 h-4 w-4" />
            Profile Strength
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2">
            <div className="text-2xl font-bold">{profileStrength}%</div>
            {profileStrength > 70 ? (
              <ArrowUpRight className="h-4 w-4 text-green-500 dark:text-green-400" />
            ) : (
              <ArrowUpRight className="h-4 w-4 text-orange-500 dark:text-orange-400" />
            )}
          </div>
          <Progress value={profileStrength} className="h-2 mt-2" />
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {profileStrength < 50 ? "Complete your profile" : 
             profileStrength < 80 ? "Almost there!" : "Excellent profile!"}
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardStats;
