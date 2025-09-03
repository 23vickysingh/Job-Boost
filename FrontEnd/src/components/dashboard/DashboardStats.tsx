
import React from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { Search, Target, FileText } from "lucide-react";
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
  const { data: jobStats } = useQuery({
    queryKey: ["jobStats"],
    queryFn: fetchJobMatchStats,
  });
  
  // Get job statistics from API or use defaults
  const totalMatches = jobStats?.data?.total_matches || 0;
  const highRelevanceJobs = jobStats?.data?.high_relevance_jobs || 0;
  const recentMatches = jobStats?.data?.recent_matches || 0;
  const appliedJobs = jobStats?.data?.applied_jobs || 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
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
            {totalMatches}
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
            {highRelevanceJobs}
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
          <div className="text-2xl font-bold">
            {appliedJobs}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            <span className="text-green-500 dark:text-green-400">0</span> from last week
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardStats;
