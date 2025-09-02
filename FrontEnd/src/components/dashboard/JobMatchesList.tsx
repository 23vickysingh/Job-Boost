
import React, { useState } from 'react';
import { 
  Card, 
  CardContent
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Plus, 
  Check, 
  Bookmark,
  ExternalLink,
  MapPin,
  Building,
  Calendar,
  Clock,
  X,
  CheckCircle
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { fetchJobMatches, updateJobMatchStatus } from "@/lib/api";
import { formatDistanceToNow, parseISO } from "date-fns";
import { useJobs, type JobMatch } from "@/contexts/JobContext";
import { toast } from "sonner";

const JobMatchesList: React.FC = () => {
  // Get job management functions from context
  const { addToApplications, removeJobMatch, isJobApplied, isJobRemoved } = useJobs();
  
  // Fetch job matches from API
  const { data: jobMatchesResponse, isLoading, error } = useQuery({
    queryKey: ["jobMatches"],
    queryFn: () => fetchJobMatches({ limit: 10 }),
  });

  const jobMatches: JobMatch[] = jobMatchesResponse?.data || [];

  const formatRelevanceScore = (score: number): string => {
    return `${Math.round(score * 100)}%`;
  };

  const formatJobPostedDate = (dateString?: string): string => {
    if (!dateString) return "Date not available";
    try {
      const date = parseISO(dateString);
      return formatDistanceToNow(date, { addSuffix: true });
    } catch {
      return "Date not available";
    }
  };

  const getEmploymentTypeColor = (type?: string): string => {
    switch (type?.toLowerCase()) {
      case 'fulltime':
      case 'full-time':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      case 'parttime':
      case 'part-time':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      case 'contract':
      case 'contractor':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300';
      case 'intern':
      case 'internship':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300';
    }
  };

  const getRelevanceColor = (score: number): string => {
    if (score >= 0.8) return 'text-green-600 dark:text-green-400 font-bold';
    if (score >= 0.6) return 'text-orange-600 dark:text-orange-400 font-semibold';
    return 'text-red-600 dark:text-red-400';
  };

  const handleApplyClick = (applyLink?: string) => {
    if (applyLink) {
      window.open(applyLink, '_blank', 'noopener,noreferrer');
    }
  };

  // Handler for moving job to applications
  const handleMoveToApplications = async (jobMatch: JobMatch) => {
    try {
      await addToApplications(jobMatch);
      toast.success("Job moved to applications successfully!");
      // Refresh the job matches to update the UI
      window.location.reload(); // Simple refresh - you could implement more sophisticated state management
    } catch (error) {
      console.error('Failed to move job to applications:', error);
      toast.error("Failed to move job to applications. Please try again.");
    }
  };

  // Handler for removing job from matches
  const handleNotInterested = async (jobMatchId: number) => {
    try {
      await updateJobMatchStatus(jobMatchId, 'not_interested');
      toast.success("Job marked as not interested");
      // Refresh the job matches to update the UI
      window.location.reload(); // Simple refresh - you could implement more sophisticated state management
    } catch (error) {
      console.error('Failed to update job status:', error);
      toast.error("Failed to update job status. Please try again.");
    }
  };

  // Show all job matches - filtering by status is now handled by the backend
  const filteredJobMatches = jobMatches;

  if (isLoading) {
    return (
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Job Matches
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {[...Array(4)].map((_, index) => (
            <Card key={index} className="animate-pulse">
              <CardContent className="p-6">
                <div className="space-y-3">
                  <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Job Matches
        </h2>
        <Card className="border-red-200 dark:border-red-800">
          <CardContent className="p-6 text-center">
            <p className="text-red-600 dark:text-red-400">
              Failed to load job matches. Please try again later.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="h-full overflow-hidden flex flex-col">
      <div className="flex justify-between items-center px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-slate-800/50">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          Job Matches ({filteredJobMatches.length})
        </h2>
      </div>
      
      {filteredJobMatches.length === 0 ? (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="text-center space-y-4">
            <div className="mx-auto w-24 h-24 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
              <Bookmark className="w-12 h-12 text-gray-400" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                No job matches yet
              </h3>
              <p className="text-gray-500 dark:text-gray-400 mb-4">
                Complete your profile and set job preferences to get personalized job matches.
              </p>
              <Button className="inline-flex items-center">
                <Plus className="mr-2 h-4 w-4" />
                Complete Profile
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {filteredJobMatches.map((match) => (
            <Card key={match.id} className="hover:shadow-lg transition-shadow duration-200">
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-1">
                      {match.job.job_title || 'Job Title Not Available'}
                    </h3>
                    <div className="flex items-center text-gray-600 dark:text-gray-300 mb-2">
                      <Building className="mr-2 h-4 w-4" />
                      <span>{match.job.employer_name || 'Company Not Available'}</span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end space-y-2">
                    <div className={`font-bold text-lg ${getRelevanceColor(match.relevance_score)}`}>
                      {formatRelevanceScore(match.relevance_score)}
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      Match Score
                    </Badge>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div className="space-y-2">
                    {match.job.job_city && (
                      <div className="flex items-center text-gray-600 dark:text-gray-300 text-sm">
                        <MapPin className="mr-2 h-4 w-4" />
                        <span>
                          {match.job.job_city}
                          {match.job.job_country && `, ${match.job.job_country}`}
                          {match.job.job_is_remote && ' (Remote)'}
                        </span>
                      </div>
                    )}
                    
                    {match.job.job_employment_type && (
                      <div className="flex items-center">
                        <Clock className="mr-2 h-4 w-4 text-gray-400" />
                        <Badge className={getEmploymentTypeColor(match.job.job_employment_type)}>
                          {match.job.job_employment_type}
                        </Badge>
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-2">
                    {match.job.job_posted_at_datetime_utc && (
                      <div className="flex items-center text-gray-600 dark:text-gray-300 text-sm">
                        <Calendar className="mr-2 h-4 w-4" />
                        <span>Posted {formatJobPostedDate(match.job.job_posted_at_datetime_utc)}</span>
                      </div>
                    )}
                    
                    {(match.job.job_min_salary || match.job.job_max_salary) && (
                      <div className="text-sm text-gray-600 dark:text-gray-300">
                        <span className="font-medium">Salary: </span>
                        {match.job.job_min_salary && match.job.job_max_salary
                          ? `${match.job.job_salary_currency || ''}${match.job.job_min_salary} - ${match.job.job_max_salary}`
                          : match.job.job_min_salary
                          ? `${match.job.job_salary_currency || ''}${match.job.job_min_salary}+`
                          : `Up to ${match.job.job_salary_currency || ''}${match.job.job_max_salary}`}
                        {match.job.job_salary_period && ` per ${match.job.job_salary_period}`}
                      </div>
                    )}
                  </div>
                </div>
                
                {match.job.job_description && (
                  <div className="mb-4">
                    <p className="text-sm text-gray-600 dark:text-gray-300 overflow-hidden" style={{
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical'
                    }}>
                      {match.job.job_description.substring(0, 200)}
                      {match.job.job_description.length > 200 && '...'}
                    </p>
                  </div>
                )}
                
                <div className="flex justify-between items-center">
                  {match.status === 'applied' ? (
                    <Button 
                      variant="outline" 
                      size="sm"
                      disabled
                      className="text-green-600 dark:text-green-400 border-green-300 dark:border-green-600 bg-green-50 dark:bg-green-900/20"
                    >
                      <CheckCircle className="mr-2 h-4 w-4" />
                      Already Applied
                    </Button>
                  ) : (
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => handleMoveToApplications(match)}
                      className="text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                    >
                      <Check className="mr-2 h-4 w-4" />
                      Move to Applications
                    </Button>
                  )}
                  
                  <div className="flex gap-2">
                    {match.status !== 'applied' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleNotInterested(match.id)}
                        className="text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
                      >
                        <X className="mr-2 h-4 w-4" />
                        Not Interested
                      </Button>
                    )}
                    <Button
                      size="sm"
                      onClick={() => handleApplyClick(match.job.job_apply_link)}
                      disabled={!match.job.job_apply_link}
                      className="bg-blue-600 hover:bg-blue-700 text-white"
                    >
                      <ExternalLink className="mr-2 h-4 w-4" />
                      Apply Now
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default JobMatchesList;
